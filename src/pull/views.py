from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from pull.models import Person_D
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required

import numpy as np 
import pandas as pd 
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from pandas import get_dummies

# Create your views here.
def mainpage(request):
    return render(request,'mainpage.html')

def registration(request):
    username=request.POST.get("login")
    email=request.POST.get("email")
    password=request.POST.get("password")
    if User.objects.filter(username=username):
        print("Уже зарегистрирован")
        request.session["message"]="Пользователь уже зарегистрирован"
        return HttpResponseRedirect('/',request) 
    user = User.objects.create_user(username=username,email=email,password=password)
    print(user)
    user.save()
    request.session["message"]="Вы успешно зарегистрированы!"
    return HttpResponseRedirect('/')

def predict(request):
    sym_dis_data=pd.read_csv("/src/Mmodels/dataset.csv")
    sym_des_data=pd.read_csv("/src/Mmodels/symptom_Description.csv")
    y=sym_dis_data.Disease
    sym_features=["Symptom_1","Symptom_2","Symptom_3","Symptom_4","Symptom_5","Symptom_6","Symptom_7","Symptom_8","Symptom_9","Symptom_10","Symptom_11","Symptom_12","Symptom_13","Symptom_14","Symptom_15","Symptom_16","Symptom_17"]
    X=sym_dis_data[sym_features]
    X=pd.get_dummies(X)
    y=pd.get_dummies(y)
    train_X , valid_X , train_y , valid_y = train_test_split(X,y,random_state=0)
    model=DecisionTreeRegressor(random_state=1)
    model.fit(train_X,train_y)
    X_final_data=request.session["Active"]
    X_final_data=pd.get_dummies(X_final_data)
    X_final=pd.DataFrame(columns=X.columns,data=X_final_data)
    X_final=X_final.fillna(0)
    predict1=model.predict(X_final)
    count=0
    count_v=0
    value=0
    for i in predict1[0] :
        count+=1
        if i>value:
            value=i
            count_v=count
    disease_l=sym_dis_data.Disease.unique()
    print(predict1[0])
    print(disease_l[count_v])
    request.session["Diagnose"]=disease_l[count_v]
    request.session["Diagnose_Desc"]=(sym_des_data.loc[sym_des_data.Disease==disease_l[count_v]]).to_string()
    User_b=request.user.username
    Disease_b=disease_l[count_v]
    if (Person_D.objects.filter(User=User_b,Disease=Disease_b)):
        "Затычка"
    else :
        P_d=Person_D(User=User_b,Disease=Disease_b)
        P_d.save()
    return HttpResponseRedirect('/home/')

def diagnose_p(request):
    return render(request,'diagnose_page.html')

def sympthom_c(request):
    s_state=request.session["S_state"]
    s_state+=1
    request.session["S_state"]=s_state
    sym_dis_data=pd.read_csv("/src/Mmodels/dataset.csv")
    sym_list=sym_dis_data["Symptom_"+str(request.session["S_state"]+1)].unique()
    request.session["sympthons"]=sym_list.tolist()
    sym=request.GET.get("sympthom")
    print(sym)
    sy_list=request.session["sympthons"]
    if sym in sy_list:
        sy_list.remove(" "+sym)
    request.session["sympthons"]=sy_list
    print(request.session["S_state"])
    a_list=request.session["Active"]
    a_list.append("Symptom_"+str(request.session["S_state"])+"_ "+sym)
    request.session["Active"]=a_list
    print(request.session["sympthons"])
    print(request.session["Active"])
    return HttpResponseRedirect('/diagnose/')

def logining(request):
    username=request.POST.get("login")
    password=request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request,user)
        return  HttpResponseRedirect('/home',request)
    request.session["message"]="Пользователь не найден"
    return HttpResponseRedirect('/',request)

def logouting(request):
    logout(request)
    return HttpResponseRedirect('/',request)

def precaution(request):
    precaution_data=pd.read_csv("/src/Mmodels/symptom_precaution.csv")
    p_d_f=precaution_data[precaution_data.Disease.isin(request.session["P_d"])]
    request.session["p_d_f"]=p_d_f.values.tolist()
    print(request.session["p_d_f"])
    return render(request,'precaution.html')

def recovered(request):
    dis_d=request.GET.get["Dis_rec"]
    print("На удаление")
    print(dis_d)
    Person_D.objects.filter(User=request.user.username,Disease=dis_d).delete()
    return HttpResponseRedirect('/home',request)

@login_required
def home(request):
    sym_dis_data=pd.read_csv("/src/Mmodels/dataset.csv")
    sym_list=sym_dis_data.Symptom_1.unique()
    sym_list=sym_list.tolist()
    
    P_list=[]
    for i in Person_D.objects.filter(User=request.user.username):
        P_list.append(i.Disease)
    request.session["P_d"]=P_list
    request.session["sympthons"]=sym_list
    request.session["Active"]=[]
    request.session["S_state"]=0
    print(sym_list)
    return render(request,'index.html')