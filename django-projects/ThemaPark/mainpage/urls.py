from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "mainpage"

urlpatterns = [

    path("",views.index, name="index"),

    path("index",views.index, name="index"),
    path("index/login/", views.login, name="login"),
    path("index/aboutus/",views.aboutus, name="aboutus"),
    path("index/seoulgrandpark/", views.seoulgrandpark, name="seoulgrandpark"),
    path("index/seoulgrandpark/congestion/", views.seoulgrandparkcongestion, name="seoulgrandparkcongestion"),
    path("index/seoulgrandpark/subway/", views.seoulgrandparksubway, name="seoulgrandparksubway"),
    path("index/seoulgrandpark/navi/", views.seoulgrandparknavi, name="seoulgrandparknavi"),
    path("index/seoulgrandpark/parking/", views.seoulgrandparkparking, name="seoulgrandparkparking"),
    path("index/seoulgrandpark/facility/", views.seoulgrandparkfacility, name="seoulgrandparkfacility"),
    path("index/seoulgrandpark/ticket/", views.seoulgrandparkticket, name="seoulgrandparkticket"),
    path("index/seoulgrandpark/weather/", views.seoulgrandparkweather, name="seoulgrandparkweather"),
    path("index/childpark/", views.childpark, name="childpark"),
    path("index/everland/", views.everland, name="everland"),
    path("index/lotteworld/", views.lotteworld, name="lotteworld"),
    path("index/registration/", views.signup, name="registration"),
    path('index/log_in/',  auth_views.LoginView.as_view(template_name='mainpage/log-in.html'), name='login'),
    path('index/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('index/everland/congestion/', views.everlandcongestion, name="congestion"),
    path('index/everland/facility/', views.everlandfacility, name="facility"),
    path('index/everland/navi/', views.everlandnavi, name="navi"),
    path('index/everland/parking/', views.everlandparking, name="parking"),
    path('index/everland/serviceoff/', views.everlandserviceoff, name="serviceoff"),
    path('index/everland/ticket/', views.everlandticket, name="ticket"),
    path('index/everland/ticket/', views.everlandticket, name="everlandparking"),
    path('index/lotteworld/congestion/', views.lotteworldcongestion, name="lotteworldcongestion"),
    path('index/lotteworld/subway/', views.lotteworldsubway, name="lotteworldcongestion"),
    path('index/lotteworld/navi/', views.lotteworldnavi, name="lotteworldnavi"),
    path('index/lotteworld/parking/', views.lotteworldparking, name="lotteworldparking"),
    path('index/lotteworld/facility/', views.lotteworldfacility, name="lotteworldfacility"),
    path('index/lotteworld/ticket/', views.lotteworldticket, name="lotteworldticket"),


]