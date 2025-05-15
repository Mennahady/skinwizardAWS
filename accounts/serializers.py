from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings

from accounts.models import PharmacyProfile
from patient_form.models import Patient

User = get_user_model()

class DoctorRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label='Confirm password'
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'first_name', 'last_name', 'id_number')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'id_number': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        validated_data['user_type'] = 'DOCTOR'
        
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class PatientRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label='Confirm password'
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        validated_data['user_type'] = 'PATIENT'
        
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        # Create patient profile
        Patient.objects.create(
            user=user,
            name=f"{user.first_name} {user.last_name}"
        )

        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email address does not exist.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        
        # Generate token and uid
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Create reset email
        subject = "Password Reset Requested"
        message = f"""
Hello,

You have requested to reset your password. Here are your password reset details:

UID: {uid}
Token: {token}

To reset your password, use these details in the password reset confirmation endpoint.

If you did not request this reset, please ignore this email.

Best regards,
SkinWizard Team
        """
        
        # Send email
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        
        # Return both success message and the tokens
        return {
            "success": "Password reset email has been sent.",
            "uid": uid,
            "token": token
        }

class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    token = serializers.CharField(required=True)
    uidb64 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        try:
            uid = urlsafe_base64_decode(attrs['uidb64']).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({"uidb64": "Invalid user ID"})
        
        if not default_token_generator.check_token(user, attrs['token']):
            raise serializers.ValidationError({"token": "Invalid or expired token"})
        
        attrs['user'] = user
        return attrs

    def save(self):
        password = self.validated_data['password']
        user = self.validated_data['user']
        user.set_password(password)
        user.save()
        return user

class CustomUserDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for returning the user details to dj-rest-auth
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'user_type')
        read_only_fields = ('email', 'user_type')

# -----------------------
# Pharmacy Registration
# -----------------------
class PharmacyRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    pharmacy_name = serializers.CharField()
    address = serializers.CharField()
    license = serializers.ImageField()

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password', 'pharmacy_name', 'address', 'license']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')

        pharmacy_name = validated_data.pop('pharmacy_name')
        address = validated_data.pop('address')
        license = validated_data.pop('license')

        user = User.objects.create_user(
            role='pharmacy',
            password=password,
            **validated_data
        )

        PharmacyProfile.objects.create(
            user=user,
            pharmacy_name=pharmacy_name,
            address=address,
            license=license
        )

        return user 