from base.models import Account, Pin, Comment, Like, FollowHandle, SavedPin, ReportPin, Seen
from django.contrib import admin


admin.site.register(Account)
admin.site.register(Pin)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(FollowHandle)
admin.site.register(SavedPin)
admin.site.register(ReportPin)
admin.site.register(Seen)

