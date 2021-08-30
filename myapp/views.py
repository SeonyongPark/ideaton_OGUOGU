from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone
from .models import News,Hreviews,Mreviews,diagnosis
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth

# 뉴스 
def home(request):
    news=News.objects.all()
    return render(request,'home.html',{'news':news})

def news_detail(request,id):
    dnews=get_object_or_404(News,pk=id)
    return render(request,'news_detail.html',{'dnews':dnews})

def news_register(request):
    return render(request,'news_register.html')

def news_create(request):
    new_news=News()
    new_news.title=request.POST['title']
    new_news.writer=request.POST['writer']
    new_news.body=request.POST['body']
    new_news.date=timezone.now()
    new_news.link=request.POST['link']
    new_news.image=request.FILES['image']
    new_news.save()
    return redirect('news_detail',new_news.id)

# 병원 리뷰
def hospital_review(request):
    hreview=Hreviews.objects.all()
    return render(request,'hospital_review.html',{'hreview':hreview})

def hreview_detail(request,id):
    hreview=get_object_or_404(Hreviews,pk=id)
    return render(request,'hreview_detail.html',{'hreview':hreview})

def hreview_register(request):
    return render(request,'hreview_register.html')

def hreview_create(request):
    new_hreview=Hreviews()
    new_hreview.hospital=request.POST['hospital']
    new_hreview.nickname=request.POST['nickname']
    new_hreview.body=request.POST['body']
    new_hreview.date=timezone.now()
    new_hreview.image=request.FILES['image']
    new_hreview.save()
    return redirect('hreview_detail',new_hreview.id)

# 약품 리뷰
def medicine_review(request):
    mreview=Mreviews.objects.all()
    return render(request,'medicine_review.html',{'mreview':mreview})

def mreview_detail(request,id):
    mreview=get_object_or_404(Mreviews,pk=id)
    return render(request,'mreview_detail.html',{'mreview':mreview})

def mreview_register(request):
    return render(request,'mreview_register.html')

def mreview_create(request):
    new_mreview=Mreviews()
    new_mreview.medicine=request.POST['medicine']
    new_mreview.nickname=request.POST['nickname']
    new_mreview.body=request.POST['body']
    new_mreview.date=timezone.now()
    new_mreview.part=request.POST['part']
    new_mreview.image=request.FILES['image']
    new_mreview.save()
    return redirect('mreview_detail',new_mreview.id)



# def hreview(request):
#     return render(request,'hospital_review.html')

# def mreview(request):
#     return render(request,'medicine_review.html')
def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

# def medicine_search(request):
#     return render(request, 'medicine_search.html')

def search_page(request):
    return render(request, 'search_page.html')

    from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
#form에서 했던 것과 같이 form 양식을 import
from django.contrib.auth import authenticate, login, logout

#렌더링 요청은 get, create 등 데이터베이스와 관련된 요청은 post방식으로 처리됨->if문으로
def login_view(request):
    if request.method == 'POST':
        username = request.POST["Username"]
        password = request.POST["Password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': "username or passowrd is incorrect"})
    else:
        return render(request, 'login.html')


def logout_view(request):
    auth.logout(request)
    return redirect('home')

def search_hospital(request):
    hList=Hreviews.objects.order_by('-id')
    q=request.GET.get('q','')

    if q:
        hsearch=hList.filter(hospital__icontains=q)
        return render(request,'hreview_search.html',{'hsearch':hsearch})
    else:
        return render(request,'hreview_search.html')

def search_medicine(request):
    mList=Mreviews.objects.order_by('-id')
    q=request.GET.get('q','')

    if q:
        msearch=mList.filter(medicine__icontains=q)
        return render(request,'mreview_search.html',{'msearch':msearch})
    else:
        return render(request,'mreview_search.html')

def button_search_medicine(request):
    mList=Mreviews.objects.order_by('-id')
    q=request.GET['part']

    if q:
        msearch=mList.filter(part__icontains=q)
        return render(request,'mreview_search.html',{'msearch':msearch})
    else:
        return render(request,'mreview_search.html')

def search_home(request):
    pList=News.objects.order_by('-id')
    q=request.GET['link']

    if q:
        psearch=pList.filter(link__icontains=q)
        return render(request,'home_search.html',{'psearch':psearch})
    else:
        return render(request,'home_search.html')


def search_page(request):         
    result_list = []
    if request.method == 'POST':
        search = request.POST["search_text"]
        search_list = search.split(",")
        dia = diagnosis.objects.all()

        for dia in dia:
            T_F = []
            for word in search_list:
                if word in dia.symptom:
                    T_F.append(1)
                else:
                    T_F.append(0)
            
            if all(T_F):
                result_list.append(dia)
                dia.symptom = dia.symptom.replace("|", "\n")
                dia.symptom = dia.symptom[1:len(dia.symptom)]
                

                
                for i in range(dia.cause.count("#")):
                    #dia.cause.insert(dia.cause.find("#"), "\n")
                    num = dia.cause.find("#")
                    dia.cause = dia.cause[0:num] + "\n\n" + dia.cause[num+1:len(dia.cause)]
                
                dia.cause = dia.cause[2:len(dia.cause)]
                #dia.cause = dia.cause.replace("#", "\n")
                dia.treat = dia.treat.replace("#", "\n\n")
                dia.treat = dia.treat[2:len(dia.treat)]
                dia.prevent = dia.prevent.replace("#", "\n")
                dia.prevent = dia.prevent[1:len(dia.treat)]
                dia.advice = dia.advice.replace("#", "\n")
                dia.advice = dia.advice[1:len(dia.treat)]

        print(result_list)
    
    return render(request, 'search_page.html', {'search_page' : result_list})
    