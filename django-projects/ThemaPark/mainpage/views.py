
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from mainpage.forms import UserForm
from mainpage.models import *


# Create your views here.

def lotteworldcongestion(request):
    return render(request, "mainpage/lotteworld_congestion.html")

def lotteworldsubway(request):
    return render(request, "mainpage/lotteworld_subway.html")

def lotteworldnavi(request):
    return render(request, "mainpage/lotteworld_navi.html")

def lotteworldparking(request):
    return render(request, "mainpage/lotteworld_parking.html")

def lotteworldfacility(request):
    return render(request, "mainpage/lotteworld_facility.html")

def lotteworldticket(request):
    return render(request, "mainpage/lotteworld_ticket.html")

def everlandcongestion(request):
    return render(request, "mainpage/everland_congestion.html")

def everlandfacility(request):
    return render(request, "mainpage/everland_facility.html")

def everlandnavi(request):
    return render(request, "mainpage/everland_navi.html")

def everlandparking(request):
    return render(request, "mainpage/everland_parking.html")

def everlandserviceoff(request):
    return render(request, "mainpage/everland_serviceoff.html")

def everlandticket(request):
    return render(request, "mainpage/everland_ticket.html")

def index(request):
#사용자가 선택한 날짜가 찍히도록 print문 안에
    #inlineFormInputGroup
    #print(inlineFormInputGroup)
    return render(request, "mainpage/index.html")



def aboutus(request):
    return render(request, "mainpage/aboutus.html")


def seoulgrandpark(request):
    entrance = PreEntrance.objects.filter(theme_name='서울대공원')
    context = {'entrance': entrance}
    return render(request, "mainpage/seoulgrandpark.html", context)



def childpark(request):
    return render(request, "mainpage/childpark.html")

def everland(request):
    return render(request, "mainpage/everland.html")

def lotteworld(request):
    return render(request, "mainpage/lotteworld.html")

#def login(request):
#    return render(request, "mainpage/log-in.html")

def registration(request):
    return render(request, "mainpage/registration.html")


# 회원 가입
def signup(request):
    # signup 으로 POST 요청이 왔을 때, 새로운 유저를 만드는 절차를 밟는다.
    if request.method == 'POST':
        form = UserForm(request.POST)
        # password와 confirm에 입력된 값이 같다면
        if form.is_valid():
            form.save()
            raw_username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=raw_username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'mainpage/registration.html', {'form': form})


# 로그인
def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password1)
        if user is not None:
            auth_login(request, user)
            return render(request, '/',)
        else:
            messages.info(request , 'invalid credentials')
            return render(request, 'mainpage/log-in.html')
    else:
        return render(request, 'mainpage/log-in.html')


# 로그 아웃
def logout(request):
    # logout으로 POST 요청이 들어왔을 때, 로그아웃 절차를 밟는다.
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/')

    # logout으로 GET 요청이 들어왔을 때, 로그인 화면을 띄워준다.
    return render(request, '/')

def seoulgrandparkcongestion(request):
    return render(request, "mainpage/seoulgrandpark_congestion.html")

def seoulgrandparksubway(request):
    return render(request, "mainpage/seoulgrandpark_subway.html")

def seoulgrandparknavi(request):
    return render(request, "mainpage/seoulgrandpark_navi.html")

def seoulgrandparkparking(request):
    return render(request, "mainpage/seoulgrandpark_parking.html")

def seoulgrandparkfacility(request):
    return render(request, "mainpage/seoulgrandpark_facility.html")

def seoulgrandparkticket(request):
    return render(request, "mainpage/seoulgrandpark_ticket.html")

def seoulgrandparkweather(request):
    return render(request, "mainpage/seoulgrandpark_weather.html")
