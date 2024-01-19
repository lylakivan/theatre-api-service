from django.urls import path

from user.views import CreateUser, CreateTokenView, ManageUserView


urlpatterns = [
    path("register/", CreateUser.as_view(), name="register"),
    path("token/", CreateTokenView.as_view(), name="token"),
    path("me/", ManageUserView.as_view(), name="manage"),

]

app_name = "user"
