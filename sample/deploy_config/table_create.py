# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # __author__ = "athrun"
# # __date__ = "2017/7/21"
# import os
#
# from django.contrib.auth.hashers import make_password
# from rest_framework import status
# from rest_framework.response import Response
#
# from manage_files.models import Bucket
# from manage_users.models import Account, Group
# from utils.hub_handler.admin_handler import RGWAdminHandler as RGWbox
# from utils.hub_handler.space_handler import RGWSpaceHandler as RGWbox_Space
#
#
# def table_create():
#     clean_count = 0
#     try:
#         Account.objects.get(username='admin')
#         clean_count = clean_count + 1
#     except Account.DoesNotExist:
#         print '\033[1;31;40m[table Account:admin DoesNotExist !]\033[0m'
#
#     try:
#         Group.objects.get(name='admin')
#         clean_count = clean_count + 1
#     except Group.DoesNotExist:
#         print '\033[1;31;40m[table Group:admin DoesNotExist !]\033[0m'
#
#     try:
#         Group.objects.get(name='group_admin')
#         clean_count = clean_count + 1
#     except Group.DoesNotExist:
#         print '\033[1;31;40m[table Group:group_admin DoesNotExist !]\033[0m'
#
#     try:
#         Group.objects.get(name='user')
#         clean_count = clean_count + 1
#     except Group.DoesNotExist:
#         print '\033[1;31;40m[table Group:user DoesNotExist !]\033[0m'
#
#     if clean_count < 4:
#         print 'Some necessary table DoesNotExist or wrong'
#         clean_allow = raw_input('Start creating tables?(y/n)')
#         if clean_allow == 'y':
#             admins = Group(name="admin")
#             admins.save()
#             group_admins = Group(name="group_admin")
#             group_admins.save()
#             rgwbox = RGWbox()
#             keys = rgwbox.create_user('group-user')
#             if keys is None:
#                 errors_info = {"detail": "Create Fail!"}
#                 return Response(errors_info, status=status.HTTP_400_BAD_REQUEST)
#             access_key, secret_key = keys
#             users = Group(name="user", s3_access_key=access_key, s3_secret_key=secret_key)
#             users.save()
#             space_bucket = RGWbox_Space(access_key=users.s3_access_key,
#                                         secret_key=users.s3_secret_key)
#             if space_bucket.bucket_create(bucket_name='group-' + users.name + '-bucket'):
#                 Bucket(
#                     name=('group-' + users.name + '-bucket'),
#                     group=users
#                 ).save()
#             else:
#                 return_message = {
#                     "code": 3010,
#                     "message": "RGW Bucket Create Denied!",
#                     "success": False,
#                     "data": None
#                 }
#                 rgwbox.remove_user('group-' + users.name)
#                 users.delete()
#                 return Response(return_message, status=status.HTTP_400_BAD_REQUEST)
#             rgwbox = RGWbox()
#             keys = rgwbox.create_user('user-admin')
#             if keys is None:
#                 errors_info = {"detail": "Create Fail!"}
#                 return Response(errors_info, status=status.HTTP_400_BAD_REQUEST)
#             access_key, secret_key = keys
#             admin = Account(
#                 username="admin",
#                 password=make_password("admin"),
#                 email="admin@example.com",
#                 s3_access_key=access_key,
#                 s3_secret_key=secret_key,
#                 role='admin'
#             )
#             admin.save()
#             space_bucket = RGWbox_Space(access_key=admin.s3_access_key, secret_key=admin.s3_secret_key)
#             if space_bucket.bucket_create(bucket_name='user-' + admin.username + '-bucket'):
#                 Bucket(
#                     name=('user-' + admin.username + '-bucket'),
#                     account=admin
#                 ).save()
#             else:
#                 return_message = {
#                     "code": 3010,
#                     "message": "RGW Bucket Create Denied!",
#                     "success": False,
#                     "data": None
#                 }
#                 rgwbox.remove_user('user-' + admin.username)
#                 admin.delete()
#                 return Response(return_message, status=status.HTTP_400_BAD_REQUEST)
#             admin.groups.add(users, admins)
#             admin.admin_groups.add(users, admins)
#             admin.creator_account = admin
#             admin.save()
#         else:
#             os._exit(1)
