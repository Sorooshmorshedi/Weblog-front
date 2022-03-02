from base.models import Account, Pin, Like, Comment, SavedPin, ReportPin, FollowHandle, Seen
from django.contrib.auth.models import User
from rest_framework import serializers

class AccountSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    class Meta:
        model = Account
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    class Meta:
        model = User
        fields = '__all__'


class PinSerializer(serializers.ModelSerializer):
    pro_pic = serializers.ImageField(source='account.profile_picture', read_only=True)
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    user_name = serializers.CharField(source='account.user_name', read_only=True)

    class Meta:
        model = Pin
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    pro_pic = serializers.ImageField(source='account.profile_picture', read_only=True)
    user_name = serializers.CharField(source='account.user_name', read_only=True)
    class Meta:
        model = Like
        fields = '__all__'

    def validate(self, data):
        data_account = data.get('account')
        data_pin = data.get('pin')
        if Like.objects.filter(account=data_account, pin=data_pin):
            raise serializers.ValidationError('you cant like a post twice')
        return super(LikeSerializer, self).validate(data)


class CommentSerializer(serializers.ModelSerializer):
    pro_pic = serializers.ImageField(source='account.profile_picture', read_only=True)
    user_name = serializers.CharField(source='account.user_name', read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'

class SavedPinSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedPin
        fields = '__all__'

    def validate(self, data):
        data_account = data.get('account')
        data_pin = data.get('pin')
        if SavedPin.objects.filter(account=data_account, pin=data_pin):
            raise serializers.ValidationError('you already save this pin')
        return super(SavedPinSerializer, self).validate(data)

class ReportedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportPin
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    follower_pic = serializers.ImageField(source='follower_account.profile_picture', read_only=True)
    following_pic = serializers.ImageField(source='following_account.profile_picture', read_only=True)
    following_user = serializers.CharField(source='following_account.user_name', read_only=True)
    follower_user = serializers.CharField(source='follower_account.user_name', read_only=True)
    class Meta:
        model = FollowHandle
        fields = '__all__'

    def validate(self, data):
        data_following = data.get('following_account')
        data_follower = data.get('follower_account')
        if data_follower == data_following:
            raise serializers.ValidationError('you cant follow yourself')
        if FollowHandle.objects.filter(follower_account=data_follower,
                                       following_account=data_following):
            raise serializers.ValidationError('you already follow this user')
        return super(FollowSerializer, self).validate(data)


class SeenSerializer(serializers.ModelSerializer):
    following_user = serializers.CharField(source='following_account.user_name', read_only=True)
    follower_user = serializers.CharField(source='follower_account.user_name', read_only=True)
    class Meta:
        model = Seen
        fields = '__all__'

    def validate(self, data):
        data_pin= data.get('pin')
        data_account = data.get('account')
        if Seen.objects.filter(account=data_account, pin=data_pin):
            raise serializers.ValidationError('seen already is avalible')
        return super(SeenSerializer, self).validate(data)
