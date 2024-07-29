from django.urls import path
from .views import NotificationCreateView, NotificationListView

urlpatterns = [
    path('notifications', NotificationCreateView.as_view(), name='user-notification'),
    path('allnotifications', NotificationListView.as_view(), name='user-all-notification'),
]