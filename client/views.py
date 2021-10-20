from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .forms import RegistrationForm, LoginForm
from .models import User
from django.contrib.auth import authenticate, login,logout
import pymongo, json
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://harsh:dubey@diet.nloju.mongodb.net/dietapi?retryWrites=true&w=majority")
db = cluster["dietapi"]
days = db["days"]
reci = db["recipies"]
ing = db["ingredients"]
mealplan = db["mealsplans"]
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

def userprofile(request):
	if request.user.is_authenticated:
		data = User.objects.get(email=request.user)
		if data.plan_days:
			context = {'username':data.username,'email':data.email,'height':data.height,'weight':data.weight,'age':data.age,'plan':data.plan_days,'range':range(1,data.plan_days+1)}
		else:
			context = {'username':data.username,'email':data.email,'height':data.height,'weight':data.weight,'age':data.age}
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

def getdata(request,day):
	if True:
		if request.user.is_authenticated:
			
			days_data = days.find_one({"day":day})
			if days_data is not None:
				ml_id = days_data["meals"]
				#meals part
				mealsplans= mealplan.find_one({"_id":ml_id[0]})
				if mealsplans is not None:
					bf_id = mealsplans["break_fast"]
					ms_id = mealsplans["morning_snacks"]
					lu_id = mealsplans["lunch"]
					as_id = mealsplans["afternoon_snacks"]
					di_id = mealsplans["dinner"]

					meal_data = []
					dic = {}
					meals_list = [bf_id[0],ms_id[0],lu_id[0],as_id[0],di_id[0]]
					for i in meals_list:
						ingre = []
						dic_ing = {}
						data = reci.find_one({"_id":i})
						if data is not None:
							x = data["ingredient"]
							for i in x:
								d = ing.find_one({"_id":i})
								if d is not None:
									ingre.append(d["name"])
									dic["ingred"]=ingre
									print("\n\nDIC",dic)
								else:
									if ingre == []:
										dic["ingred"]=["No Data Available"]
							data.update(dic)
							print("\n\nDATA",data)
							meal_data.append(data)
							print("\n\nmeal",meal_data)
						else:
							meal_data.append({'_id':"No Data Available",'name':"No Data Available",'desc':"No Data Available","img":"No Data Available","ingredient":"No Data Available",'__v':"No Data Available","ingred":["No Data Available"]})

					context= {"day": days_data['day'],"cost":days_data['cost'],"meal":mealsplans['name'],"bf_name":meal_data[0]["name"],"bf_desc":meal_data[0]["desc"],"ms_name":meal_data[1]["name"],"ms_desc":meal_data[1]["desc"],"lu_name":meal_data[2]["name"],"lu_desc":meal_data[2]["desc"],"as_name":meal_data[3]["name"],"as_desc":meal_data[3]["desc"],"di_name":meal_data[4]["name"],"di_desc":meal_data[4]["desc"],"bf_ingre":','.join(meal_data[0]["ingred"]),"ms_ingre":','.join(meal_data[1]["ingred"]),"lu_ingre":','.join(meal_data[2]["ingred"]),"as_ingre":','.join(meal_data[3]["ingred"]),"di_ingre":','.join(meal_data[4]["ingred"])}
					return render(request,'client/dietplans.html',context)

				else:
					context= {"day": days_data['day'],"cost":days_data['cost'],"meal":"No Data Available","bf_name":"No Data Available","bf_desc":"No Data Available","ms_name":"No Data Available","ms_desc":"No Data Available","lu_name":"No Data Available","lu_desc":"No Data Available","as_name":"No Data Available","as_desc":"No Data Available","di_name":"No Data Available","di_desc":"No Data Available","bf_ingre":"No Data Available","ms_ingre":"No Data Available","lu_ingre":"No Data Available","as_ingre":"No Data Available","di_ingre":"No Data Available"}
					return render(request,'client/dietplans.html',context)
					
			else:
				return HttpResponse("No Days Available in Table")
		else:
			return HttpResponseRedirect('/login/')
	#except:
	#	return HttpResponse("Something wrong in DB!!")