from rest_framework import status
from rest_framework.response import Response


def SuccessResponse(data={}):
    data.update({
        'success': True,
    })
    return Response(data, status=status.HTTP_200_OK)


def ErrorResponse(errors):
    if type(errors) == list:
        e = {}
        for error in errors:
            e.update(error)
        errors = e

    custom_errors = []
    for field, messages in errors.items():
        for message in messages:
            if field == 'non_field_errors':
                custom_errors.append({'message': message})
            else:
                custom_errors.append({'field': field, 'message': message})
    data = {
        'success': False,
        'errors': custom_errors,
    }
    return Response(data, status.HTTP_400_BAD_REQUEST)