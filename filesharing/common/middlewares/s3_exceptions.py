from botocore.exceptions import ClientError, BotoCoreError
from rest_framework.response import Response
from rest_framework import status

class S3ExeptionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except (ClientError, BotoCoreError):
            return Response(data={
                'error':'The storage service is not working yet. try again in the next few hours.'
                }, status=status.HTTP_504_GATEWAY_TIMEOUT)