from .serializers import UserSerializer, ResetPasswordRequestSerializer, ResetPasswordConfirmSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User, Otp
from .tasks import send_notification_email


class UserRegisterView(APIView):
    """
    Create a new user.
    """
    serializer_class = UserSerializer

    def post(self, request):
        ser_data = UserSerializer(data=request.data)

        if ser_data.is_valid():
            for field in ['email', 'username', 'first_name']:
                if field in ser_data.validated_data and isinstance(ser_data.validated_data[field], str):
                    ser_data.validated_data[field] = ser_data.validated_data[field].strip()

            ser_data.create(ser_data.validated_data)

            return Response(data={
                'message':'User created successfully.',
                'user': ser_data.data
            },status=status.HTTP_201_CREATED)
        
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ResetPasswordRequest(APIView):
    """
    A request to reset password.
    Take a registered email and send an One-Time Password Code to user's email.
    """
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        ser_data = ResetPasswordRequestSerializer(data=request.data)
        if ser_data.is_valid():
            user = User.objects.filter(email=ser_data.validated_data['email']).first()

            if user:
                # Before saving data at DB, pre_save signal at ./signals.py deletes any
                # rows related to this user in the OTP model.
                otp_instace = Otp.objects.create(user=user)
                send_notification_email.delay(email=user.email, code=otp_instace.otp_code)
            else:
                send_notification_email.delay(email=ser_data.validated_data['email'])

            return Response(data={
                'message':'If this email is registered, you will receive an email with instructions to reset your password.'
            }, status=status.HTTP_202_ACCEPTED)
        
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordConfirm(APIView):
    """
    Confirm the reset password request.
    Takes 3 fields. Code sent to user's email and user's email and new password
    """
    serializer_class = ResetPasswordConfirmSerializer

    def patch(self, request):
        ser_data = ResetPasswordConfirmSerializer(data=request.data)

        if ser_data.is_valid():
            user = User.objects.filter(email=ser_data.validated_data['email']).first()
            otp_user = Otp.objects.filter(user=user, otp_code=ser_data.validated_data['code']).first()

            if otp_user:
                if not otp_user.is_expired:
                    ser_data.update(user, ser_data.validated_data)
                    return Response(data={'message':'User Password changed successfuly.'}, status=status.HTTP_200_OK)
                else:
                    otp_user.delete()
                    return Response(data={'error':'Code is expired.'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(data={'error':'Code or email is wrong.'}, status=status.HTTP_404_NOT_FOUND)
            
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
