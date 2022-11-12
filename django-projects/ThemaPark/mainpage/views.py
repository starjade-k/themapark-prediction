
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from mainpage.forms import UserForm
from mainpage.models import *
from datetime import datetime


# Create your views here.
def index(request):
    if request.method == 'GET':
        try:
            date = request.GET['date']
            entrance = PreEntrance.objects.filter(std_date=date).order_by('std_date', 'theme_name')
            context = {'entrance': entrance}
            return render(request, "mainpage/index.html", context)
        except:
            date = datetime.today().strftime('%Y-%m-%d')
            entrance = PreEntrance.objects.filter(std_date=date).order_by('std_date', 'theme_name')
            context = {'entrance': entrance}
            return render(request, "mainpage/index.html", context)

def aboutus(request):
    return render(request, "mainpage/aboutus.html")

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

# ㅡㅡㅡㅡㅡ 롯데월드 ㅡㅡㅡㅡㅡ
def lotteworldcongestion(request):
    if not request.user.is_authenticated:
        return render(request,"mainpage/log-in.html")
    time = ThemeparkTime.objects.filter(theme_name='롯데월드').order_by('std_date')
    pre_ent = PreEntrance.objects.filter(theme_name='롯데월드').order_by('std_date')
    data = zip(time, pre_ent)   
    context = {'data': data}
    return render(request, "mainpage/lotteworld_congestion.html", context)

def lotteworldnavi(request):
    prenavi = PreNavi.objects.filter(theme_name='롯데월드').order_by('std_date')
    context = {'prenavi': prenavi}
    return render(request, "mainpage/lotteworld_navi.html", context)

def lotteworldparking(request):
    return render(request, "mainpage/lotteworld_parking.html")

def lotteworldfacility(request):
    return render(request, "mainpage/lotteworld_facility.html")

def lotteworldticket(request):
    return render(request, "mainpage/lotteworld_ticket.html")

def lotteworldserviceoff(request):
    today = datetime.now().date()
    holfac = ThemeparkHolfac.objects.filter(theme_name='롯데월드', std_date=today)
    context = {'holfac': holfac}
    return render(request, "mainpage/lotteworld_serviceoff.html", context)

def lotteworldweather(request):
    weather = PreAirWeather.objects.filter(theme_name=str('롯데월드')).order_by('std_date')
    context = {'weather':weather}
    return render(request, "mainpage/lotteworld_weather.html", context)

# ㅡㅡㅡㅡㅡ 에버랜드 ㅡㅡㅡㅡㅡ
def everlandcongestion(request):
    if not request.user.is_authenticated:
        return render(request,"mainpage/log-in.html")
    time = ThemeparkTime.objects.filter(theme_name='에버랜드').order_by('std_date')
    pre_ent = PreEntrance.objects.filter(theme_name='에버랜드').order_by('std_date')
    data = zip(time, pre_ent)   
    context = {'data': data}
    return render(request, "mainpage/everland_congestion.html", context)

def everlandfacility(request):
    return render(request, "mainpage/everland_facility.html")

def everlandnavi(request):
    prenavi = PreNavi.objects.filter(theme_name='에버랜드').order_by('std_date')
    context = {'prenavi': prenavi}
    return render(request, "mainpage/everland_navi.html", context)

def everlandparking(request):
    return render(request, "mainpage/everland_parking.html")

def everlandserviceoff(request):
    today = datetime.now().date()
    holfac = ThemeparkHolfac.objects.filter(theme_name='에버랜드', std_date=today)
    context = {'holfac': holfac}
    return render(request, "mainpage/everland_serviceoff.html", context)

def everlandticket(request):
    return render(request, "mainpage/everland_ticket.html")

def everlandweather(request):
    weather = PreAirWeather.objects.filter(theme_name=str('에버랜드')).order_by('std_date')
    context = {'weather':weather}
    return render(request, "mainpage/everland_weather.html", context)

# ㅡㅡㅡㅡㅡ 서울대공원 ㅡㅡㅡㅡㅡ
def seoulgrandparkcongestion(request):
    if not request.user.is_authenticated:
        return render(request,"mainpage/log-in.html")
    time = ThemeparkTime.objects.filter(theme_name='서울대공원').order_by('std_date')
    pre_ent = PreEntrance.objects.filter(theme_name='서울대공원').order_by('std_date')
    pre_event = PreEvent.objects.filter(theme_name='서울대공원').order_by('std_date')
    data = zip(time, pre_ent, pre_event)   
    context = {'data': data}
    return render(request, "mainpage/seoulgrandpark_congestion.html", context)

def seoulgrandparknavi(request):
    prenavi = PreNavi.objects.filter(theme_name='서울대공원').order_by('std_date')
    context = {'prenavi': prenavi}
    return render(request, "mainpage/seoulgrandpark_navi.html", context)

def seoulgrandparkparking(request):
    return render(request, "mainpage/seoulgrandpark_parking.html")

def seoulgrandparkfacility(request):
    return render(request, "mainpage/seoulgrandpark_facility.html")

def seoulgrandparkticket(request):
    return render(request, "mainpage/seoulgrandpark_ticket.html")

def seoulgrandparkweather(request):
    weather = PreAirWeather.objects.filter(theme_name=str('서울대공원')).order_by('std_date')
    context = {'weather':weather}
    return render(request, "mainpage/seoulgrandpark_weather.html", context)


# ㅡㅡㅡㅡㅡ 어린이대공원 ㅡㅡㅡㅡㅡ
def childparkcongestion(request):
    if not request.user.is_authenticated:
        return render(request,"mainpage/log-in.html")
    time = ThemeparkTime.objects.filter(theme_name='서울어린이대공원').order_by('std_date')
    pre_ent = PreEntrance.objects.filter(theme_name='서울어린이대공원').order_by('std_date')
    pre_event = PreEvent.objects.filter(theme_name='서울어린이대공원').order_by('std_date')
    data = zip(time, pre_ent, pre_event)   
    context = {'data': data}
    return render(request, "mainpage/childrenpark_congestion.html", context)

def childparknavi(request):
    prenavi = PreNavi.objects.filter(theme_name='서울어린이대공원').order_by('std_date')
    context = {'prenavi': prenavi}
    return render(request, "mainpage/childrenpark_navi.html", context)

def childparkparking(request):
    return render(request, "mainpage/childrenpark_parking.html")

def childparkfacility(request):
    return render(request, "mainpage/childrenpark_facility.html")

def childparkticket(request):
    return render(request, "mainpage/childrenpark_ticket.html")

def childparkserviceoff(request):
    return render(request, "mainpage/childrenpark_serviceoff.html")

def childparkweather(request):
    weather = PreAirWeather.objects.filter(theme_name=str('서울어린이대공원')).order_by('std_date')
    context = {'weather':weather}
    return render(request, "mainpage/childrenpark_weather.html", context)


# def seoulgrandpark(request):
#     entrance = PreEntrance.objects.filter(theme_name='서울대공원').order_by('std_date')
#     context = {'entrance': entrance}
#     return render(request, "mainpage/base_seoulgrandpark.html", context)


# def childpark(request):
#     entrance = PreEntrance.objects.filter(theme_name='서울어린이대공원').order_by('std_date')
#     context = {'entrance': entrance}
#     return render(request, "mainpage/base_childrenpark.html", context)
    

# def everland(request):
#     entrance = PreEntrance.objects.filter(theme_name='에버랜드').order_by('std_date')
#     context = {'entrance': entrance}
#     return render(request, "mainpage/everland.html", context)

# def lotteworld(request):
#     entrance = PreEntrance.objects.filter(theme_name='롯데월드').order_by('std_date')
#     context = {'entrance': entrance}
#     return render(request, "mainpage/lotteworld.html", context)

#def login(request):
#    return render(request, "mainpage/log-in.html")














