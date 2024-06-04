from django.urls import path
from .views import SignUpView, LoginAPI, SearchUsersView, SendFriendRequestView, RespondFriendRequestView, ListFriendsView, ListPendingFriendRequestsView
from knox import views as knox_views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginAPI.as_view(), name='knox_login'),
    path('search/', SearchUsersView.as_view(), name='search-users'),
    path('friend-request/send/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-request/respond/', RespondFriendRequestView.as_view(), name='respond-friend-request'),
    path('friends/', ListFriendsView.as_view(), name='list-friends'),
    path('friend-requests/pending/', ListPendingFriendRequestsView.as_view(), name='list-pending-friend-requests'),
]
