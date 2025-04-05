from rest_framework import serializers
from .models import News
from users.models import User

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ["id", "content", "photo", "video", "created_at", "created_by", "role",
                  "ward", "city_village", "district", "state", "country", "is_public"]
        read_only_fields = ["created_by", "role", "created_at"]

class NewsListSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    creator_role = serializers.CharField(source='created_by.role', read_only=True)
    creator_email = serializers.CharField(source='created_by.email', read_only=True)
    date_submitted = serializers.DateTimeField(source='created_at', format="%d %b %Y %I:%M %p")
    news_type = serializers.SerializerMethodField()
    has_media = serializers.SerializerMethodField()
    content_preview = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            'id',
            'creator_name',
            'creator_role',
            'news_type',
            'date_submitted',
            'creator_email',
            'content_preview',
            'has_media',
            'photo_url',
        ]

    def get_news_type(self, obj):
        if obj.photo and obj.video:
            return 'photo_and_video'
        elif obj.photo:
            return 'photo'
        elif obj.video:
            return 'video'
        return 'text'

    def get_has_media(self, obj):
        return bool(obj.photo or obj.video)

    def get_content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.photo.url) if request else obj.photo.url
        return None
    
class NewsDetailSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source='created_by.get_full_name')
    creator_email = serializers.CharField(source='created_by.email')
    creator_role = serializers.CharField(source='created_by.role')
    time = serializers.DateTimeField(source='created_at', format="%d %b %Y %I:%M %p")
    media = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            'id',
            'creator_name',
            'creator_email',
            'creator_role',
            'time',
            'content',
            'media',
            'photo',
            'video'
        ]

    def get_media(self, obj):
        media = {}
        if obj.photo:
            media['photo_url'] = obj.photo.url
        if obj.video:
            media['video_url'] = obj.video.url
        return media

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for updating the user's profile and including plan details, 
    along with handling the profile image.
    """
    profile_image = serializers.ImageField(required=False, allow_null=True)  # Add the profile image field

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'username',
             'profile_image'
        ]

    def validate_email(self, value):
        """
        Custom email validation to ensure uniqueness.
        """
        if User.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("This email is already taken.")
        return value

class ProfileImageUpdateSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=True)  # Make it required

    class Meta:
        model = User
        fields = ['profile_image']

    def update(self, instance, validated_data):
        """
        Replace the existing profile image with the new one if available.
        """
        # Check if the user already has a profile image and delete it if exists
        if instance.profile_image:
            instance.profile_image.delete()

        # Update the profile image with the new one
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        
        # Save the instance after the update
        instance.save()
        return instance
    

    
class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for handling password change.
    """
    old_password = serializers.CharField(required=True, write_only=True)
    new_password1 = serializers.CharField(required=True, write_only=True)
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        """
        Validate that the new passwords match and the old password is correct.
        """
        old_password = data.get('old_password')
        new_password1 = data.get('new_password1')
        new_password2 = data.get('new_password2')

        # Check if new passwords match
        if new_password1 != new_password2:
            raise serializers.ValidationError("New passwords do not match.")
        
        # Check if the old password is correct
        user = self.context.get('user')
        if not user.check_password(old_password):
            raise serializers.ValidationError("Old password is incorrect.")
        
        # Check if the new password is the same as the old password
        if old_password == new_password1:
            raise serializers.ValidationError("New password cannot be the same as the old password.")
        
        return data

