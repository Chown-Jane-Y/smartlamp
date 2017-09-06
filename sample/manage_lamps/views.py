# -*- coding: utf-8 -*-

import copy
import uuid

from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from api.message import MessageError
from manage_hubs.models import Hubs
from manage_files.models import Files
from utils.hub_handler.space_handler import RGWSpaceHandler as RGWbox_Space


# OK
def create_file(uploader, the_file, directory, file_type, bucket, user=None, group=None):
    if directory is None:
        the_directory = None
    else:
        the_directory = Files.objects.get(pk=directory)
    if Files.objects.filter(name=the_file.name, type=file_type, directory=the_directory).exists():
        return False
    the_file_object = Files(
        name=the_file.name,
        size=the_file.size,
        type=file_type,
        is_file=True,
        directory=the_directory,
        account=user,
        group=group,
        bucket=bucket,
        uploader=uploader)
    the_file_object.save()
    the_file_object.uuid = "file-" + str(the_file_object.id) + "-" + str(uuid.uuid1()) + "-end"
    the_file_object.save()
    return the_file_object


# OK
def delete_files(the_file):
    if the_file.is_leaf is True:
        delete_file(the_file)
    else:
        all_files_in = Files.objects.filter(directory=the_file, type=the_file.type)
        for file_item in all_files_in:
            delete_files(file_item)
        the_file.delete()
    return True


# OK
def delete_file(the_file):
    (user, group) = (the_file.account, the_file.group)
    if user is not None:
        bucket = Hubs.objects.get(account=user)
        (access_key, secret_key) = (bucket.s3_access_key, bucket.s3_secret_key)
    elif group is not None:
        bucket = Hubs.objects.get(group=group)
        (access_key, secret_key) = (bucket.s3_access_key, bucket.s3_secret_key)
    else:
        return_message = MessageError(code=3002, message="No User and Group")
        return Response(return_message.data(), status=status.HTTP_200_OK)
    space = RGWbox_Space(access_key=access_key, secret_key=secret_key)
    if space.single_object_delete(bucket_name=bucket.name, object_name=the_file.uuid):
        the_file.delete()
        return True
    else:
        raise ValidationError("File Delete Failed!")


# OK
def disable_files(the_file):
    if the_file.is_file is True:
        the_file.is_deleted = True
        the_file.save()
        all_share_file = Files.objects.filter(origin=the_file)
        for file_item in all_share_file:
            file_item.is_deleted = True
            file_item.save()
    else:
        all_files_in = Files.objects.filter(directory=the_file, type=the_file.type)
        for file_item in all_files_in:
            disable_files(file_item)
        the_file.is_deleted = True
        the_file.save()
        all_share_file = Files.objects.filter(origin=the_file)
        for file_item in all_share_file:
            file_item.is_deleted = True
            file_item.save()
    return True


# OK
def enable_files(the_file):
    if the_file.is_file is True:
        the_file.is_deleted = False
        the_file.save()
        all_share_file = Files.objects.filter(origin=the_file)
        for file_item in all_share_file:
            file_item.is_deleted = False
            file_item.save()
    else:
        all_files_in = Files.objects.filter(directory=the_file, type=the_file.type)
        for file_item in all_files_in:
            disable_files(file_item)
        the_file.is_deleted = False
        the_file.save()
        all_share_file = Files.objects.filter(origin=the_file)
        for file_item in all_share_file:
            file_item.is_deleted = False
            file_item.save()
    return True


def copy_file(bucket, the_file, destination_directory):
    new_file = copy.deepcopy(the_file)
    new_file.id = None
    new_file.directory = destination_directory
    new_file.save()
    new_file.uuid = "file-" + str(new_file.id) + "-" + str(uuid.uuid1()) + "-end"
    new_file.save()
    space = RGWbox_Space(
        access_key=bucket.s3_access_key,
        secret_key=bucket.s3_secret_key)
    if space.single_object_copy(bucket, the_file.uuid, new_file.uuid):
        return True
    else:
        new_file.delete()
        raise ValidationError("RGW File Copy Failed!")


def copy_folder(the_file, destination_directory):
    new_file = copy.deepcopy(the_file)
    new_file.id = None
    if destination_directory is None:
        new_file.level = 1
        new_file.level_tree = '0'
        new_file.path_tree = '/'
        new_file.directory = None
    else:
        new_file.level = destination_directory.level + 1
        new_file.level_tree = destination_directory.level_tree + '-' + str(destination_directory.id)
        new_file.path_tree = destination_directory.path_tree + destination_directory.name + '/'
        new_file.directory = destination_directory
    new_file.save()
    return new_file


def copy_files(bucket, the_file, destination_directory):
    if the_file.is_file is True:
        copy_file(bucket, the_file, destination_directory)
    else:
        new_folder = copy_folder(the_file, destination_directory)
        step_files = Files.objects.filter(directory=the_file, type=the_file.type)
        for file_item in step_files:
            copy_files(bucket, file_item, new_folder)
    return True
