from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .forms import RegistrationForm, LoginForm
from .models import User
from django.contrib.auth import authenticate, login,logout
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://harsh:dubey@diet.nloju.mongodb.net/dietapi?retryWrites=true&w=majority")

def userregister(request):
	if not request.user.is_authenticated:
		if request.method == 'POST':
			fm = RegistrationForm(request.POST)
			if fm.is_valid():
				fm.save()
				return HttpResponseRedirect('/login/')
		else:
			fm = RegistrationForm()
		return render(request,'client/register.html',{'fm':fm})
	else:
		return HttpResponseRedirect('/profile/')

def userlogin(request):
	if not request.user.is_authenticated:
		if request.method == 'POST':
			fm = LoginForm(request=request,data=request.POST)
			if fm.is_valid():
				un = fm.cleaned_data['username']
				ps = fm.cleaned_data['password']
				user = authenticate(username=un, password=ps)
				if user is not None:
					login(request, user)
					return HttpResponseRedirect('/profile/')
		else:
			fm = LoginForm()
		return render(request,'client/login.html',{'fm':fm})
	else:
		return HttpResponseRedirect('/profile/')
def getdata(request):
	db = cluster["dietapi"]
	collection = db["ingredients"]
	data = collection.find()
	print(data)
	return HttpResponse(data)

def userprofile(request):
	if request.user.is_authenticated:
		data = User.objects.get(email=request.user)
		context = {'username':data.username,'email':data.email,'height':data.height,'weight':data.weight,'age':data.age,'plan':data.plan_days}
		return render(request,'client/profile.html',context)
	else:
		return HttpResponseRedirect('/login/')
	
def userlogout(request):
	if request.user.is_authenticated:
		logout(request)
	return HttpResponseRedirect('/login/')

def plans(request,days=None):
	if request.user.is_authenticated:
		if request.method=="POST":
			data = User.objects.get(email=request.user)
			data.plan_days = days
			data.save()
			return HttpResponseRedirect('/profile/')
		else:
			return render(request,'client/plans.html')
	else:
		return HttpResponseRedirect('/login/')