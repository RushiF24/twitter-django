from rest_framework import generics
from .serializers import NotificationCreateSerializer, NotificationListSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Notification

# Create your views here.
class NotificationCreateView(generics.CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationCreateSerializer
    permission_classes = (IsAuthenticated, )

class NotificationListView(generics.ListAPIView):
    # queryset = Notification.objects.all()
    serializer_class = NotificationListSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, is_read=False)
    

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "status": True,
                "message": "Notification retrived Successfully",
                "status_code": status.HTTP_200_OK,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK
        )

class NotificationUpdateView(generics.UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationCreateSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, is_read=False)
        
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)