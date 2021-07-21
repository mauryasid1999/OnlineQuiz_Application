from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth import login,logout,authenticate
from .forms import *
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def home(request):

    if request.method=="POST":
        questions=QuestionModel.objects.all()

        score=0
        wrong=0
        correct=0
        total=0

        for q in questions:
           
            total=total+1
            if q.ans == request.POST.get(q.question):
                score=score+10
                correct=correct+1
            else:
                wrong=wrong+1

        percent=score/(total*10) * 100

        context={
            'score':score,
            'total':total,
            'correct':correct,
            'percent':percent,
            'wrong':wrong,
            'time':request.POST.get('timer')
        }

        return render(request,'result.html',context)




    else:

        questions=QuestionModel.objects.all()

        context={
        'questions':questions
        }

        return render(request,'home.html',context);


def registerpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form=createuserform()
        if request.method=='POST':
            form=createuserform(request.POST)
            if form.is_valid():
                user=form.save()
                return redirect('login')

        context={
            'form':form
        }
        return render(request,'register.html',context)

def loginpage(request):

    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method=="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')

            user=authenticate(request,username=username,password=password)

            if user is not None:
                login(request,user)
                return redirect('/')

        return render(request,'login.html') 

def logoutpage(request):
    logout(request)
    return redirect('/')           

def addquestion(request):
    if request.user.is_staff:
        form=addquestionform()

        if(request.method=='POST'):
            form=addquestionform(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('/')

        context={
            'form':form
        }        
        return render(request,'addquestion.html',context)
    else:
        return redirect('home')    

