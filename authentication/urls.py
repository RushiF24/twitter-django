from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = SimpleRouter()
router.register('users', views.UserViewset, basename='users')

# urlpatterns = router.urls

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('forgotpassword/', views.ResetPasswordRequestView.as_view(), name='forgot_password'),
    path('resetpassword/<str:token>', views.ResetPasswordView.as_view(), name='reset_password'),

    path('topusers', views.TopUsersView.as_view(), name='top_users')
] + router.urls
    