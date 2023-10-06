from django.urls import path

from . import views

app_name = "api"

urlpatterns = [
    path("", views.IndexView.as_view()  , name="index"),
    path("register-user", views.UserRegisterView.as_view()  , name="register"),
    path("apply-loan", views.LoanView.as_view()  , name="loan"),
    path("get-statement", views.StatementsView.as_view()  , name="getstatement"),
    path("make-payment", views.PayView.as_view()  , name="payment"),
]