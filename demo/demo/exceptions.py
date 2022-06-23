import json
from enum import Enum

from django.http import Http404
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException, NotFound

from .renderer import CentralizedResponseRenderer

CODE_OFFSET = 10000


class ErrorWrapper:
    def __init__(self, code, message):
        self.code = code
        self.message = message


class ErrorEnum(Enum):
    BAD_REQUEST = \
        ErrorWrapper(4000000, 'Bad request')
    INVALID_PAYLOAD = \
        ErrorWrapper(4000001, 'Invalid request payload')
    PHONE_IS_NOT_VERIFIED = \
        ErrorWrapper(4000002, 'Mobile phone number is not verified')
    HAS_VERIFIED = \
        ErrorWrapper(4000003, 'User has verified')
    IS_NOT_ACTIVE = \
        ErrorWrapper(4000004, 'User is not active')
    EMAIL_IS_EXISTS = \
        ErrorWrapper(4000005, 'Email name already exists')
    CREDENTIAL_MISSING = \
        ErrorWrapper(4000006, 'Please provide credential')
    MOBILE_NUMBER_EXISTED = \
        ErrorWrapper(4000007, 'Mobile phone number already exists')
    REQUEST_REJECTED = \
        ErrorWrapper(4000008, 'The request has been rejected by server')
    COUNTRY_MISSING = \
        ErrorWrapper(4000009, 'Please provide country information')
    NON_EXIST_ADDRESS = \
        ErrorWrapper(4000010, 'Country or town not exist')
    PHONE_IS_VERIFIED = \
        ErrorWrapper(4000011, 'The phone number has been verified, please login')
    VALIDATION_EXPIRED = \
        ErrorWrapper(4000012, 'The validation period has expired')
    WRONG_VALIDATION_CODE = \
        ErrorWrapper(4000013, 'Wrong validation code')
    EMAIL_HAS_VALIDATED = \
        ErrorWrapper(4000014, 'Email has been validated')
    PROFILE_HAS_VALIDATED = \
        ErrorWrapper(4000015, 'Profile info has been validated or under review')
    ALL_FIELD_NEED_FILLED = \
        ErrorWrapper(4000016, 'All profile info need to filled')
    THIRD_PARTY_ACCOUNT_IS_EXISTS = \
        ErrorWrapper(4000017, 'Third party account is exists')
    NEED_TO_SET_PASSWORD = \
        ErrorWrapper(4000018, 'Need to set password before remove all third-party')
    INVALID_START_TIME_OF_RENTAL = \
        ErrorWrapper(4000019, 'Start datetime have to later than current datetime')
    ILLEGAL_DATETIME_UNIT_OF_RENTAL = \
        ErrorWrapper(4000020, 'Time for rental should be unit of hour')
    ILLEGAL_TIME_FOR_RENTAL = \
        ErrorWrapper(4000021, 'Time for rental is out of limit or under limit')
    PAYMENT_FAILED = \
        ErrorWrapper(4000022, 'The payment failed')
    QUERY_PAYMENT_STATUS_FAILED = \
        ErrorWrapper(4000023, 'Query payment status failed')
    USERNAME_IS_EXISTS = \
        ErrorWrapper(4000024, 'Username is existed')
    LOGIN_REQUIRED = \
        ErrorWrapper(4010001, 'Login required')
    INVALID_TOKEN = \
        ErrorWrapper(4010002, 'Invalid token')
    INVALID_SIGNATURE = \
        ErrorWrapper(4010005, 'Invalid signature')
    ILLEGAL_NEW_PASSWORD = \
        ErrorWrapper(4010006, 'Illegal new password')
    WRONG_PASSWORD = \
        ErrorWrapper(4010007, 'Wrong password')
    REQUIRE_ORIGINAL_PASSWORD = \
        ErrorWrapper(4010008, 'Require original password')
    FORBIDDEN = \
        ErrorWrapper(4030000, 'Forbidden')
    AUTHENTICATE_FAILED = \
        ErrorWrapper(4030001, 'Username or password incorrect')
    INSUFFICIENT_PERMISSIONS = \
        ErrorWrapper(4030003, 'Insufficient permissions')
    NOT_AVAILABLE_VEHICLES = \
        ErrorWrapper(4030004, 'There are not any available vehicles now')
    PROHIBITED_ORDER = \
        ErrorWrapper(4030005, 'The requested order is not accessible')
    NOT_FOUND = \
        ErrorWrapper(4040000, 'Not found')
    PHONE_NOT_FOUND = \
        ErrorWrapper(4040001, 'Phone number not found')
    USER_NOT_REGISTERED = \
        ErrorWrapper(4040002, 'The user is not registered')
    CONFLICT = \
        ErrorWrapper(4090000, 'Conflict')
    MAX_ATTEMPTS = \
        ErrorWrapper(4290001, 'Maximum number of failed attempts has been reached')
    INTERNAL_SERVER_ERROR = \
        ErrorWrapper(5000000, 'Internal server error')
    FAIL_TO_SEND_MAIL = \
        ErrorWrapper(5000001, 'Fail to send email')
    FAIL_TO_GET_UPLOADED_URL = \
        ErrorWrapper(5000002, 'Fail to get uploaded url')
    FAIL_TO_SEND_SMS = \
        ErrorWrapper(5000003, 'Failed to send sms')
    ESTIMATE_PRICE_FAILED = \
        ErrorWrapper(5000004, 'Estimate price failed')
    CODE_EXCHANGE_FAILED = \
        ErrorWrapper(5000005, 'Failed to exchange OAuth code for tokens')


class BadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = None
    default_code = ErrorEnum.BAD_REQUEST


class Conflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = None
    default_code = ErrorEnum.CONFLICT


def get_first_error_code(codes):
    if isinstance(codes, list):
        return get_first_error_code(codes[0]) if any(codes) else None
    elif isinstance(codes, dict):
        if not any(codes):
            return None
        return get_first_error_code(next(iter(codes.values())))
    return codes


def handler(exc, context):
    error_detail = getattr(exc, 'detail', exc)
    try:
        error_detail = json.loads(json.dumps(error_detail))
    except TypeError:
        error_detail = str(error_detail)

    def check_if_is_useful_detail(detail):
        return any(detail) and (not detail == 'None')

    def pick_code_message(detail, err_enum):
        error = err_enum.value
        is_readable_detail = \
            isinstance(detail, str) and check_if_is_useful_detail(detail)
        return error.code, detail if is_readable_detail else error.message

    if isinstance(exc, APIException):
        first_code = get_first_error_code(exc.get_codes())
        if isinstance(first_code, ErrorEnum):
            error = first_code.value
            error_code = error.code
            error_message = error.message
        else:
            error_code = exc.status_code * CODE_OFFSET
            error_message = error_detail \
                if isinstance(error_detail, str) else exc.default_detail
    elif isinstance(exc, Http404):
        error_code, error_message = \
            pick_code_message(error_detail, ErrorEnum.NOT_FOUND)
    elif isinstance(exc, PermissionDenied):
        error_code, error_message = \
            pick_code_message(error_detail, ErrorEnum.FORBIDDEN)
    else:
        if isinstance(exc, ObjectDoesNotExist):
            exc = NotFound()
            error_code, error_message = \
                pick_code_message(error_detail, ErrorEnum.NOT_FOUND)
        else:
            exc = APIException()
            error_code, error_message = \
                pick_code_message(
                    error_detail, ErrorEnum.INTERNAL_SERVER_ERROR)

    if error_detail == error_message or not check_if_is_useful_detail(error_detail):
        error_detail = None

    request = context['request']
    response = exception_handler(exc, context)
    payload = {
        'error': {
            'code': error_code,
            'message': error_message,
            'detail': error_detail
        }
    }

    response.data = payload
    # add needed attributes for CentralizedResponseRenderer
    response.accepted_renderer = CentralizedResponseRenderer()
    response.accepted_media_type = "application/json"
    response.renderer_context = {'request': request}
    response.render()
    return response
