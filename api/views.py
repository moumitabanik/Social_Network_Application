from django.contrib.auth import get_user_model, login
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.throttling import UserRateThrottle
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .models import FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer, CustomAuthTokenSerializer
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from knox.settings import knox_settings
from django.contrib.auth.hashers import make_password

User = get_user_model()

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = request.data.get('password')
        hashed_password = make_password(password)
        serializer.validated_data['password'] = hashed_password
        user = serializer.save()
        _, token = AuthToken.objects.create(user)
        return Response({'user': UserSerializer(user).data, 'token': token}, status=status.HTTP_201_CREATED)

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = CustomAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
    
class SearchUsersView(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if '@' in query:
            return User.objects.filter(email__iexact=query)
        return User.objects.filter(first_name__icontains=query) | User.objects.filter(last_name__icontains=query)

class FriendRequestThrottle(UserRateThrottle):
    rate = '3/min'

class SendFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [FriendRequestThrottle]

    def post(self, request, *args, **kwargs):
        to_user_email = request.data.get('email')
        try:
            to_user = User.objects.get(email=to_user_email)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
            return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)
        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        return Response({'status': 'Friend request sent'}, status=status.HTTP_201_CREATED)

class RespondFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request_id = request.data.get('request_id')
        action = request.data.get('action')
        try:
            friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)
        if action == 'accept':
            friend_request.status = 'accepted'
            friend_request.save()
            request.user.friends.add(friend_request.from_user)
            friend_request.from_user.friends.add(request.user)
        elif action == 'reject':
            friend_request.status = 'rejected'
            friend_request.save()
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'Friend request {}'.format(action)}, status=status.HTTP_200_OK)

class ListFriendsView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.friends.all()

class ListPendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.received_requests.filter(status='pending')
