from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import CASCADE
from datetime import datetime
from django.contrib.auth.models import User, AbstractUser



class Account(models.Model):
    HIM = 'he'
    HER = 'she'
    THEY = 'they'

    PRONOUNS = (
        (HIM, 'he/him'),
        (HER, 'she/her'),
        (THEY, 'they/them')
    )
    user = models.OneToOneField(User, on_delete=CASCADE, related_name="account", blank=True,
                                null=True)
    token = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    Pronouns = models.CharField(max_length=4, choices=PRONOUNS, default=HIM, null=True, blank=True)
    business_account = models.BooleanField(default=False)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    website = models.URLField(max_length=100, null=True, blank=True)
    short_bio = models.TextField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(default='', upload_to='store_image/', null=True, blank=True)
    user_name = models.CharField(max_length=20, unique=True, validators=[RegexValidator (regex='^[a-zA-Z0-9]+$',message='username must be english')])
    followers = models.IntegerField(default=0, blank=True, null=True)
    following = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.user_name

    @staticmethod
    def createtoken():
        import random
        token = ''
        for i in range(0, 18):
            token += str(random.randint(0, 9))
            token += random.choice(['ac', 'bb', 'aa', 'gh', 'ou', 'fg'])
        return token

    def save(self, *args, **kwargs):
        self.token = self.createtoken()
        super().save(*args, **kwargs)


class FollowHandle(models.Model):
    following_account = models.ForeignKey(Account, on_delete=CASCADE, related_name="followings_account")
    follower_account = models.ForeignKey(Account, on_delete=CASCADE, related_name="followers_account")

    def save(self, *args, **kwargs):
        pro_following = Account.objects.get(pk=self.following_account.id)
        pro_follower = Account.objects.get(pk=self.follower_account.id)
        profile_followers = FollowHandle.objects.filter(following_account=self.following_account).count()
        profile_following = FollowHandle.objects.filter(follower_account=self.follower_account).count()
        pro_follower.following = profile_following + 1
        pro_following.followers = profile_followers + 1
        pro_following.save()
        pro_follower.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return "{} follow {}".format(self.follower_account, self.following_account)


class Pin(models.Model):
    account = models.ForeignKey(Account, on_delete=CASCADE, related_name="pin")
    title = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='store_image/', null=True, blank=True)
    video = models.FileField(upload_to='store_image/', null=True, blank=True)
    about_text = models.TextField(max_length=500, null=True, blank=True)
    alt_text = models.TextField(max_length=500, null=True, blank=True)
    creation_date = models.DateTimeField(null=True, blank=True)
    destination_link = models.URLField(max_length=100, null=True, blank=True)
    likes_count = models.IntegerField(null=True, blank=True)
    comments_count = models.IntegerField(null=True, blank=True)
    seens_count = models.IntegerField(null=True, blank=True)

    class Meta():
        ordering = ['-pk', ]

    def save(self, *args, **kwargs):
        if not self.id:
            self.creation_date = datetime.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return "{} by {}".format(self.title, self.account.user_name)


class Like(models.Model):
    pin = models.ForeignKey(Pin, on_delete=CASCADE, related_name="Like")
    account = models.ForeignKey(Account, on_delete=CASCADE, related_name="liked_account")
    like_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        pin_likes = Like.objects.filter(pin=self.pin).count()
        pin = self.pin
        pin.likes_count = pin_likes + 1
        pin.save()
        self.like_date = datetime.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return "{} liked {}".format(self.account.user_name, self.pin.title)


class Comment(models.Model):
    pin = models.ForeignKey(Pin, on_delete=CASCADE, related_name="comment", blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=CASCADE, related_name="account")
    comment_text = models.TextField(max_length=255)
    comment_date = models.DateTimeField(default=datetime.now())
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name="replies", blank=True, null=True)


    def save(self, *args, **kwargs):
        if self.pin :
            pin = self.pin
            pin_comments = Comment.objects.filter(pin=self.pin).count()
            pin.comments_count = pin_comments + 1
        if not self.comment_date:
            self.comment_date = datetime.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return "{} comment {}".format(self.account.user_name, self.comment_text[:10])


class SavedPin(models.Model):
    account = models.ForeignKey(Account, on_delete=CASCADE, related_name="saved_pin")
    pin = models.ForeignKey(Pin, on_delete=CASCADE, related_name="save_pin")

    def __str__(self):
        return "{} saved by {}".format(self.pin.title, self.account.user_name)


class ReportPin(models.Model):
    reporter_account = models.ForeignKey(Account, on_delete=CASCADE, related_name="reporter")
    reported_pin = models.ForeignKey(Pin, on_delete=CASCADE, related_name="reported_pin")

class Seen(models.Model):
    account = models.ForeignKey(Account, on_delete=CASCADE, related_name="seen")
    pin = models.ForeignKey(Pin, on_delete=CASCADE, related_name="seen_pin")

    def __str__(self):
        return "{} seen by {}".format(self.pin, self.account.user_name)

    def save(self, *args, **kwargs):
        if Seen.objects.filter(account=self.account, pin=self.pin):
            raise ValidationError('seen is saved once')
        mypin = Pin.objects.get(pk=self.pin_id)
        if mypin.seens_count :
            mypin.seens_count += 1
        else:
            mypin.seens_count = 1
        mypin.save()
        super().save(*args, **kwargs)
