from base.views import AccountApiView, AccountDetail, PinDetail, LikeApiView, \
    CommentApiView, CommentDetail, PinApiView, FollowApiView, SavedApiView, ReportApiView, \
    ReportDetail, AccPinsApi, AccSavedsApi, PinLikesApi, PinCommentsApi, GetFollower, GetFollowing, \
    dislikeApiView, UnFollowApi, UnSaveApi, GetUsers, SeenView, CommentReplays, SeenHandle, GetNewPost, GetOldPost, \
    SearchAccount, LikedById, FollowedById
from django.urls import path
app_name = 'base'
urlpatterns = [
    path('api/account', AccountApiView.as_view(), name='accountApi'),
    path('api/account/<str:pk>/', AccountDetail.as_view(), name='accountDetail'),
    path('api/search/<str:pk>/', SearchAccount.as_view(), name='SearchApi'),

    path('api/pin/', PinApiView.as_view(), name='pinApi'),
    path('api/pin/<int:pk>/', PinDetail.as_view(), name='pinDetail'),

    path('api/like/', LikeApiView.as_view(), name='likeApi'),
    path('api/dislike/<int:pk>/<int:accid>/', dislikeApiView.as_view(), name='dislike'),
    path('api/pin/likes/<int:pk>/', PinLikesApi.as_view(), name='allPinLikes'),

    path('api/comment/', CommentApiView.as_view(), name='commentApi'),
    path('api/comment/<int:pk>/', CommentDetail.as_view(), name='comentdetail'),
    path('api/pin/comments/<int:pk>/', PinCommentsApi.as_view(), name='allpincomments'),
    path('api/comment/replay/<int:pk>/', CommentReplays.as_view(), name='replays'),

    path('api/follow/',FollowApiView.as_view(), name='followApi'),
    path('api/unfollow/<int:pk>/<int:accid>/', UnFollowApi.as_view(), name='unfollow'),
    path('api/profile/follower/<str:pk>/', GetFollower.as_view(), name='getFollower'),
    path('api/profile/following/<str:pk>/', GetFollowing.as_view(), name='getFollowing'),

    path('api/saved/', SavedApiView.as_view(), name='savedApi'),
    path('api/unsave/<int:pk>/<int:accid>/', UnSaveApi.as_view(), name='unsave'),

    path('api/reported/', ReportApiView.as_view(), name='reportedApi'),
    path('api/reported/<int:pk>/', ReportDetail.as_view(), name='reportedDetail'),

    path('api/account/pins/<str:pk>/', AccPinsApi.as_view(), name='accAllPins'),
    path('api/account/saved/<str:pk>/', AccSavedsApi.as_view(), name='accAllSaved'),

    path('api/users', GetUsers.as_view(), name='logincheck'),

    path('api/seen', SeenView.as_view(), name='seen'),
    path('api/seened/<str:pk>/', SeenHandle.as_view(), name='seenhandle'),
    path('api/newpin/<str:pk>/', GetNewPost.as_view(), name='newpost'),
    path('api/oldpin/<str:pk>/', GetOldPost.as_view(), name='oldpost'),

    path('api/liked/<int:pk>/<int:accid>/', LikedById.as_view(), name='likedbyid'),
    path('api/followed/<int:pk>/<int:accid>/', FollowedById.as_view(), name='likedbyid'),

]
