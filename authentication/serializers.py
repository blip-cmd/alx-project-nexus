"""
Serializers for authentication app.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text="Password must be at least 8 characters long."
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text="Confirm your password."
    )
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=False, max_length=30, allow_blank=True)
    last_name = serializers.CharField(required=False, max_length=30, allow_blank=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_confirm')

    def validate_username(self, value):
        """
        Validate username is unique.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def validate_email(self, value):
        """
        Validate email is unique.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate(self, attrs):
        """
        Validate passwords match and meet requirements.
        """
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError("Passwords do not match.")

        # Validate password strength
        validate_password(password)

        return attrs

    def create(self, validated_data):
        """
        Create a new user with encrypted password.
        """
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    def validate(self, attrs):
        """
        Validate user credentials.
        """
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            
            if not user:
                raise serializers.ValidationError('Invalid credentials.')
            
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include username and password.')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer with additional user data.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add user information to response
        data.update({
            'user': {
                'id': self.user.id,
                'username': self.user.username,
                'email': self.user.email,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'date_joined': self.user.date_joined,
            }
        })
        
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile management.
    """
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login')
        read_only_fields = ('id', 'username', 'date_joined', 'last_login')

    def validate_email(self, value):
        """
        Validate email is unique (excluding current user).
        """
        user = self.instance
        if User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for password change.
    """
    old_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )
    new_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )
    new_password_confirm = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    def validate_old_password(self, value):
        """
        Validate old password is correct.
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, attrs):
        """
        Validate new passwords match and meet requirements.
        """
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')

        if new_password != new_password_confirm:
            raise serializers.ValidationError("New passwords do not match.")

        # Validate password strength
        validate_password(new_password)

        return attrs

    def save(self):
        """
        Save the new password.
        """
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for password reset request.
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Validate email exists in system.
        """
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email address.")
        return value


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for password reset confirmation.
    """
    new_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )
    new_password_confirm = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    def validate(self, attrs):
        """
        Validate new passwords match and meet requirements.
        """
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')

        if new_password != new_password_confirm:
            raise serializers.ValidationError("Passwords do not match.")

        # Validate password strength
        validate_password(new_password)

        return attrs
