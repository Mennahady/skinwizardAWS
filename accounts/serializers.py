from rest_framework import serializers
from .models import User, PatientProfile, DoctorProfile, PharmacyProfile

# -----------------------
# Patient Registration
# -----------------------
class PatientRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password', 'first_name', 'last_name']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')

        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')

        user = User.objects.create_user(
            role='patient',
            password=password,
            **validated_data
        )

        PatientProfile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name
        )

        return user

# -----------------------
# Doctor Registration
# -----------------------
class DoctorRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    id_number = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password', 'first_name', 'last_name', 'id_number']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')

        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        id_number = validated_data.pop('id_number')

        user = User.objects.create_user(
            role='doctor',
            password=password,
            **validated_data
        )

        DoctorProfile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            id_number=id_number
        )

        return user

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
