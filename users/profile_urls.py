from django.urls import path
from .views import (
    UserProfileView,
    UserUpdateView,
    UserDeleteView,
)

urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("profile/update/", UserUpdateView.as_view(), name="update_profile"),
    path("delete/", UserDeleteView.as_view(), name="delete_account"),
]
