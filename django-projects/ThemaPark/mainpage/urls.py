from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "mainpage"

urlpatterns = [

    path("",views.index, name="index"),

    path("index",views.index, name="index"),
    path("index/aboutus/",views.aboutus, name="aboutus"),
    path("index/registration/", views.signup, name="registration"),
    path('index/login/',  auth_views.LoginView.as_view(template_name='mainpage/log-in.html'), name='login'),
    path('index/logout/', auth_views.LogoutView.as_view(), name='logout'),

    # path("seoulgrandpark/", views.seoulgrandpark, name="seoulgrandpark"),
    # path("childpark/", views.childpark, name="childpark"),
    # path("everland/", views.everland, name="everland"),
    # path("lotteworld/", views.lotteworld, name="lotteworld"),

    path("seoulgrandpark/congestion/", views.seoulgrandparkcongestion, name="seoulgrandparkcongestion"),
    path("seoulgrandpark/navi/", views.seoulgrandparknavi, name="seoulgrandparknavi"),
    path("seoulgrandpark/parking/", views.seoulgrandparkparking, name="seoulgrandparkparking"),
    path("seoulgrandpark/facility/", views.seoulgrandparkfacility, name="seoulgrandparkfacility"),
    path("seoulgrandpark/ticket/", views.seoulgrandparkticket, name="seoulgrandparkticket"),
    path("seoulgrandpark/weather/", views.seoulgrandparkweather, name="seoulgrandparkweather"),

    path('everland/congestion/', views.everlandcongestion, name="congestion"),
    path('everland/facility/', views.everlandfacility, name="facility"),
    path('everland/navi/', views.everlandnavi, name="navi"),
    path('everland/parking/', views.everlandparking, name="parking"),
    path('everland/serviceoff/', views.everlandserviceoff, name="serviceoff"),
    path('everland/ticket/', views.everlandticket, name="ticket"),
    path('everland/weather/', views.everlandweather, name="childparksubway"),

    path('lotteworld/congestion/', views.lotteworldcongestion, name="lotteworldcongestion"),
    path('lotteworld/navi/', views.lotteworldnavi, name="lotteworldnavi"),
    path('lotteworld/parking/', views.lotteworldparking, name="lotteworldparking"),
    path('lotteworld/facility/', views.lotteworldfacility, name="lotteworldfacility"),
    path('lotteworld/ticket/', views.lotteworldticket, name="lotteworldticket"),
    path('lotteworld/serviceoff/', views.lotteworldserviceoff, name="lotteworldserviceoff"),
    path('lotteworld/weather/', views.lotteworldweather, name="childparksubway"),

    path('childpark/congestion/', views.childparkcongestion, name="childparkcongestion"),
    path('childpark/navi/', views.childparknavi, name="childparknavi"),
    path('childpark/parking/', views.childparkparking, name="childparkparking"),
    path('childpark/facility/', views.childparkfacility, name="childparkfacility"),
    path('childpark/ticket/', views.childparkticket, name="childparkticket"),
    path('childpark/serviceoff/', views.childparkserviceoff, name="childparkserviceoff"),
    path('childpark/weather/', views.childparkweather, name="childparksubway"),


]