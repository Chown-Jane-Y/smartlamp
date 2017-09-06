import datetime
import hashlib
import hmac
import logging
import requests

logger = logging.getLogger('django')


class HubHandler:
    # ************* REQUEST VALUES *************
    method = 'GET'
    region = 'us-east-1'
    service = 'execute-zapi_old'
    host = '192.10.11.61:7480'
    endpoint = 'http://192.10.11.61:7480'
    # request_parameters = 'Action=DescribeRegions&Version=2013-10-15'
    request_parameters = ''
    access_key = 'admin-access'
    secret_key = 'admin-secret'

    # Key derivation functions.
    @staticmethod
    def _sign(key, msg):
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

    @staticmethod
    def _getSignatureKey(key, dateStamp, regionName, serviceName):
        kDate = HubHandler._sign(('AWS4' + key).encode('utf-8'), dateStamp)
        kRegion = HubHandler._sign(kDate, regionName)
        kService = HubHandler._sign(kRegion, serviceName)
        kSigning = HubHandler._sign(kService, 'aws4_request')
        return kSigning

    def __init__(self):
        # ************* REQUEST VALUES *************
        self.method = 'GET'
        self.region = 'us-east-1'
        self.service = 'execute-zapi_old'
        self.host = '192.10.11.61:7480'
        self.endpoint = 'http://192.10.11.61:7480'
        # request_parameters = 'Action=DescribeRegions&Version=2013-10-15'
        self.request_parameters = ''
        self.access_key = 'admin-access'
        self.secret_key = 'admin-secret'
    
    @classmethod
    def test(cls):
        if cls.access_key is None or cls.secret_key is None:
            raise Exception('No access key is available.')

        # Create a date for headers and the credential string
        t = datetime.datetime.utcnow()
        amzdate = t.strftime('%Y%m%dT%H%M%SZ')
        datestamp = t.strftime('%Y%m%d')  # Date w/o time, used in credential scope

        # ************* TASK 1: CREATE A CANONICAL REQUEST *************
        # http://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html

        # Step 1 is to define the verb (GET, POST, etc.)--already done.

        # Step 2: Create canonical URI--the part of the URI from domain to query
        # string (use '/' if no path)
        canonical_uri = '/'

        # Step 3: Create the canonical query string. In this example (a GET request),
        # request parameters are in the query string. Query string values must
        # be URL-encoded (manage_files=%20). The parameters must be sorted by name.
        # For this example, the query string is pre-formatted in the request_parameters variable.
        canonical_querystring = cls.request_parameters

        # Step 4: Create the canonical headers and signed headers. Header names
        # must be trimmed and lowercase, and sorted in code point order from
        # low to high. Note that there is a trailing \n.
        canonical_headers = 'host:' + cls.host + '\n' + 'x-amz-date:' + amzdate + '\n'

        # Step 5: Create the list of signed headers. This lists the headers
        # in the canonical_headers list, delimited with ";" and in alpha order.
        # Note: The request can include any headers; canonical_headers and
        # signed_headers lists those that you want to be included in the
        # hash of the request. "Host" and "x-amz-date" are always required.
        signed_headers = 'host;x-amz-date'

        # Step 6: Create payload hash (hash of the request body content). For GET
        # requests, the payload is an empty string ("").
        payload_hash = hashlib.sha256("".encode("utf8")).hexdigest()

        # Step 7: Combine elements to create create canonical request
        canonical_request = cls.method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
        print('\n' + canonical_request)

        # ************* TASK 2: CREATE THE STRING TO SIGN*************
        # Match the algorithm to the hashing algorithm you use, either SHA-1 or
        # SHA-256 (recommended)
        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = datestamp + '/' + cls.region + '/' + cls.service + '/' + 'aws4_request'
        string_to_sign = algorithm + '\n' + amzdate + '\n' + credential_scope + '\n' + hashlib.sha256(
            canonical_request.encode("utf8")).hexdigest()
        print('\n' + string_to_sign)

        # ************* TASK 3: CALCULATE THE SIGNATURE *************
        # Create the signing key using the function defined above.
        signing_key = HubHandler._getSignatureKey(cls.secret_key, datestamp, cls.region, cls.service)

        # Sign the string_to_sign using the signing_key
        signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

        # ************* TASK 4: ADD SIGNING INFORMATION TO THE REQUEST *************
        # The signing information can be either in a query string value or in
        # a header named Authorization. This code shows how to use a header.
        # Create authorization header and add to request headers
        authorization_header = algorithm + ' ' \
                               + 'Credential=' + cls.access_key + '/' + credential_scope + ', ' \
                               + 'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature

        # The request can include any headers, but MUST include "host", "x-amz-date",
        # and (for this scenario) "Authorization". "host" and "x-amz-date" must
        # be included in the canonical_headers and signed_headers, as noted
        # earlier. Order here is not significant.
        # Python note: The 'host' header is added automatically by the Python 'requests' library.
        headers = {'x-amz-date': amzdate, 'Authorization': authorization_header}

        # ************* SEND THE REQUEST *************
        request_url = cls.endpoint + '?' + canonical_querystring

        logger.debug('\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++')
        logger.debug('\nRequest URL = ' + request_url)
        r = requests.get(request_url, headers=headers)

        logger.debug('\nRESPONSE++++++++++++++++++++++++++++++++++++')
        logger.debug('\nResponse code: %d\n' % r.status_code)
        logger.debug(r.text)

