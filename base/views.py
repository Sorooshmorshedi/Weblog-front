from base.models import Account, Pin, Like, Comment, FollowHandle, SavedPin, ReportPin, Seen
from base.serializers import AccountSerializer, PinSerializer, LikeSerializer, CommentSerializer, \
    FollowSerializer, SavedPinSerializer, ReportedSerializer, UserSerializer, SeenSerializer
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, Http404

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication, BasicAuthentication


#GET should be removed befor deploying
class AccountApiView(APIView):
    def get(self, request):
        query = Account.objects.all()
        serializers = AccountSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountDetail(APIView):
    def get_object(self, pk):
        try:
            return Account.objects.filter(token=pk)
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = AccountSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = Account.objects.filter(token=pk).first()
        serializer = AccountSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SearchAccount(APIView):
    def get_object(self, pk):
        return Account.objects.filter(Q(user_name__contains=pk) |
                                      Q(first_name__contains=pk) |
                                      Q(last_name__contains=pk))

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = AccountSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

class PinApiView(APIView):
    def get(self, request):
        query = Pin.objects.all()
        serializers = PinSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request, foramt=None):
        serializer = PinSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PinDetail(APIView):
    def get_object(self, pk):
        try:
            return Pin.objects.filter(pk=pk)
        except Pin.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = PinSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = PinSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LikeApiView(APIView):
    def post(self, request):
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class dislikeApiView(APIView):
    def get_object(self, pk, accid):
        try:
            acc = Account.objects.get(pk=accid)
            likepin = Pin.objects.get(pk=pk)
            return Like.objects.get(pin=likepin,account=acc)
        except Like.DoesNotExist:
            raise Http404
    def delete(self, request, pk, accid):
        mypin = Pin.objects.get(pk=pk)
        mypin.likes_count -= 1
        mypin.save()
        query = self.get_object(pk, accid)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PinLikesApi(APIView):
    def get_object(self, pk):
        try:
            mypin = Pin.objects.get(pk=pk)
            return Like.objects.filter(pin=mypin)
        except Like.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = LikeSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)


class CommentApiView(APIView):
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):
    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = CommentSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        mycomment= self.get_object(pk)
        try:
            if mycomment.pin != None:
                mypin = Pin.objects.get(pk=mycomment.pin.id)
                mypin.comments_count -= 1
                mypin.save()
        except:
            pass
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PinCommentsApi(APIView):
    def get_object(self, pk):
        try:
            mypin = Pin.objects.get(pk=pk)
            return Comment.objects.filter(pin=mypin)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = CommentSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

class CommentReplays(APIView):
    def get_object(self, pk):
        try:
            cm = Comment.objects.get(pk=pk)
            return Comment.objects.filter(reply=cm)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = CommentSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)



class FollowApiView(APIView):
    def post(self, request):
        serializer = FollowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UnFollowApi(APIView):
    def get_object(self, pk, accid):
        try:
            follower_acc = Account.objects.get(pk=pk)
            following_acc = Account.objects.get(pk=accid)
            return FollowHandle.objects.get(following_account=following_acc, follower_account=follower_acc)
        except FollowHandle.DoesNotExist:
            raise Http404

    def delete(self, request, pk, accid):
        follower = Account.objects.get(pk=accid)
        following = Account.objects.get(pk=pk)
        follower.followers-= 1
        following.following -= 1
        following.save()
        follower.save()
        query = self.get_object(pk, accid)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SavedApiView(APIView):
    def post(self, request):
        serializer = SavedPinSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnSaveApi(APIView):
    def get_object(self, pk, accid):
        try:
            myaccount = Account.objects.get(pk=accid)
            mypin = Pin.objects.get(pk=pk)
            return SavedPin.objects.get(account=myaccount, pin=mypin)
        except FollowHandle.DoesNotExist:
            raise Http404
    def get(self, request, pk, accid):
        query = self.get_object(pk, accid)
        serializers = SavedPinSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, accid):
        query = self.get_object(pk, accid)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReportApiView(APIView):
    def get(self, request):
        query = ReportPin.objects.all()
        serializers = ReportedSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ReportedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportDetail(APIView):
    def get_object(self, pk):
        try:
            return ReportPin.objects.get(pk=pk)
        except ReportPin.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = ReportedSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = ReportedSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AccPinsApi(APIView):
    def get_object(self, pk):
        try:
            acc = Account.objects.get(token=pk)
            return Pin.objects.filter(account=acc)
        except Pin.DoesNotExist or Account.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = PinSerializer(query, many=True, context={"request":request})
        return Response(serializers.data, status=status.HTTP_200_OK)


class AccSavedsApi(APIView):
    def get_object(self, pk):
        try:
            acc = Account.objects.get(token=pk)
            saved = SavedPin.objects.filter(account=acc)
            pin_ids=[]
            for save in saved:
                pin_ids.append(save.pin_id)
            return Pin.objects.filter(id__in=pin_ids)
        except Pin.DoesNotExist or Account.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = PinSerializer(query, many=True, context={"request":request})
        return Response(serializers.data, status=status.HTTP_200_OK)



class GetFollower(APIView):
    def get_object(self, pk):
        try:
            acc = Account.objects.get(token=pk)
            return FollowHandle.objects.filter(following_account=acc)
        except FollowHandle.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = FollowSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)


class GetFollowing(APIView):
    def get_object(self, pk):
        try:
            acc = Account.objects.get(token=pk)
            return FollowHandle.objects.filter(follower_account=acc)
        except FollowHandle.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = FollowSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)


class SeenView(APIView):
    def get(self, request):
        query = Seen.objects.all()
        serializers = SeenSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SeenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetUsers(APIView):
    def get(self, request):
        query = User.objects.all()
        serializers = UserSerializer(query, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class SeenHandle(APIView):

    def get(self, request, pk):
        account = Account.objects.get(token=pk)
        for pin in Pin.objects.all():
            try:
                seen = Seen.objects.create(account=account,pin=pin)
                seen.save()
            except:
                pass
        return Response('seen',status=status.HTTP_200_OK)

class GetNewPost(APIView):
    def get_object(self, pk):
        acc = Account.objects.get(token=pk)
        seens = Seen.objects.filter(account=acc)
        id =[]
        for seen in seens:
            id.append(seen.pin.id)
        return Pin.objects.exclude(id__in=id)

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = PinSerializer(query, many=True,context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

class GetOldPost(APIView):
    def get_object(self, pk):
        acc = Account.objects.get(token=pk)
        seens = Seen.objects.filter(account=acc)
        id =[]
        for seen in seens:
            id.append(seen.pin.id)
        return Pin.objects.filter(id__in=id)

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = PinSerializer(query, many=True,context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

class LikedById(APIView):
    def get(self, request, pk, accid):
        pin = Pin.objects.get(pk=pk)
        account = Account.objects.get(pk=accid)
        if Like.objects.filter(pin=pin,account=account):
            return Response({'liked': 1}, status=status.HTTP_200_OK)
        else:
            return Response({'liked': 0}, status=status.HTTP_404_NOT_FOUND)

class FollowedById(APIView):
    def get(self, request, pk, accid):
        account1 = Account.objects.get(pk=pk)
        account2 = Account.objects.get(pk=accid)
        if FollowHandle.objects.filter(following_account=pin,follower_account=account):
            return Response({'followed': 1}, status=status.HTTP_200_OK)
        else:
            return Response({'followed': 0}, status=status.HTTP_404_NOT_FOUND)
