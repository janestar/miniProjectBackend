# -*-coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
#import simplejson
import json
from miniDevApp.models import BottleInfo
from miniDevApp.models import WishList
from miniDevApp.models import UserInfo
from miniDevApp.bottleform import bottleForm
from miniDevApp.models import ReportList
from django import forms

class BottleForm(forms.Form):
    #bottleId = forms.BigAutoField()
    bottleId = forms.IntegerField()
    uid = forms.CharField()
    bottleName = forms.CharField()
    bottleStatus = forms.IntegerField()
    bottlePrice = forms.DecimalField()
    bottleInfo = forms.CharField()
    bottleImageUrl = forms.FileField()
    sendTimestamp = forms.DateField()

# Create your views here.
def getItemList(request):
    type = request.GET['type']
    if type == '1':
        bottles = BottleInfo.objects.filter(bottleUserInfo="427290210")
        bottle_list = []
        for bottle in bottles:
            bottle_list.append(bottle.getDict())
        return HttpResponse(json.dumps({"itemList":bottle_list}, ensure_ascii=False))        
    if type == '2':
        wishes = WishList.objects.filter(wishUserInfo="427290210")
        bottle_list = []
        for wish in wishes:
            bottle = BottleInfo.objects.get(bottleId=wish.wish_bottleId)
            bottle_info = bottle.getDict()
            bottle_info["itemStatus"] = wish.bottleStatus
            bottle_list.append(bottle_info)
        return HttpResponse(json.dumps({"itemList":bottle_list}, ensure_ascii=False))


def getItemDetail(request):
    itemId = request.GET['itemId']
    bottle_info = BottleInfo.objects.filter(bottleId=itemId)
    bottle_list = []
    for bottle in bottle_info:
        bottle_list.append(bottle.getDict())
    return HttpResponse(json.dumps(bottle_list, ensure_ascii=False))



def confirmBargain(request):

    itemId = request.POST['itemId']
    bottle_info = BottleInfo.objects.filter(bottleId=itemId)
    for bottle in bottle_info:
        bottle.bottleStatus = 1
        bottle.save()
    #print bottle_info[0].bottleStatus
    #bottle_info[0].bottleStatus = 1
    #bottle_info[0].save()
    #print bottle_info[0].bottleStatus
    #DICT = {‘ret’:'0', 'ret_msg':'确认成功'}
    bargainStatus = dict()
    bargainStatus['ret']='0'
    bargainStatus['ret_msg']='你好'
    response= HttpResponse(json.dumps(bargainStatus, ensure_ascii=False))
    response['Access-Ctrol-Allow-Origin']='*'
    return response

def cancelBargain(request):
    itemId = request.POST['itemId']
    bottle_info = BottleInfo.objects.filter(bottleId=itemId)
    bottle_info.bottleStatus = -1
    bottle_info.save()
   # DICT = {‘ret’:'0', 'ret_msg':'删除成功'}
    bargainStatus = dict()
    bargainStatus['ret']='0'
    bargainStatus['ret_msg']='ok'
    return HttpResponse(json.dumps(bargainStatus, ensure_ascii=False))


def getBottle(request):
    if(request.method=='POST'):
        form = bottleForm(request.POST)
        if form.is_valid():
           action = form.cleaned_data['action']
           uid = form.cleaned_data['uid']
           bottleId = form.cleaned_data['bottleId']
           bottleStatus = form.cleaned_data['bottleStatus']
           bottle_list = []
           if(action == "get"):
               bottle_info = BottleInfo.objects.filter(bottleId=111)
               for bottle in bottle_info:
                   bottle_list.append(bottle.randomChooseBottle(action))
           else:
               randomBottle = dict()
               randomBottle["action"] = "get"
               randomBottle["resetStatus"] = "1"
               randomBottle["message"] = "ok"
               bottle_list.append(randomBottle)
           return HttpResponse(json.dumps(bottle_list, ensure_ascii=False))


def updateUserInfo(request):
    if(request.method=='POST'):
        data = json.loads(request.body)
        uid = data['uid']
        #user = null
        users = UserInfo.objects.filter(qqId=uid)
        if not users:
            user = UserInfo()
        else:
            user = users[0]
        user.qqId = data['uid']
        user.phoneNumber = data['phoneNumber']
        user.userAddress = data['userAddress']
        user.userPostion = data['userPosition']
        user.userImageUrl = data['userImageUrl']
        user.userNickName = data['userNickName']
        user.save()
        
        updateStatus = dict()
        updateStatus['ret']='0'
        updateStatus['ret_msg']='ok'
    return HttpResponse(json.dumps(updateStatus, ensure_ascii=False)) 


## 验证函数，非API
def matchAuthCode(code):
    '''return True or False'''
    return True

def getUserInfo(request):
    if(request.method=='POST'):
        data = json.loads(request.body)
        uid = data['uid']
        code = data['authCode']
        info = dict()
        if matchAuthCode(code):
            info = UserInfo.objects.get(qqId=uid).getDict()
            bottles = BottleInfo.objects.filter(bottleUserInfo=uid)
            wishes = WishList.objects.filter(wishUserInfo=uid)
            info["throwBottleNum"] = len(bottles)
            info["gettingBottleNum"] = len(wishes)
        return HttpResponse(json.dumps(info, ensure_ascii=False));
# 抛瓶子
def throwBottle(request):
    bf = BottleForm(request.POST,request.FILES)
    if bf.is_valid():
        #bottle = BottleInfo()
        #bootle.bottleId = bf.cleaned_data['bottleId']
        #uid = uf.cleaned_data['uid']
        #bottle.bottleName = bf.cleaned_data['bottleName']
        #bottle.bottleStatus = bf.cleaned_data['bottleStatus']
        #bottle.bottlePrice = bf.cleaned_data["bottlePrice"]
        #bottle.bottleInfo = bf.cleaned_data['bottleInfo']
        #bottle.bottleImageUrl = bf.cleaned_data['bottleImage']
        #bottle.sendTimestamp = bf.cleaned_data['sendTimestamp']
        Id = bf.cleaned_data['bottleId']
        uid = bf.cleaned_data['uid']
        UserInfo = UserInfo.objects.get(qqId = uid)
        Name = bf.cleaned_data['bottleName']
        Status = bf.cleaned_data['bottleStatus']
        Price = bf.cleaned_data["bottlePrice"]
        Info = bf.cleaned_data['bottleInfo']
        ImageUrl = bf.cleaned_data['bottleImage']
        SendTimestamp = bf.cleaned_data['sendTimestamp']
        bottle = BottleInfo(bottleId = Id, bottleUserInfo = UserInfo, bottleName = Name, bootleStatus = Status, bootlePrice = Price, bottleInfo = Info, bottleImageUrl = ImageUrl, sendTimeStamp = SendTimeStamp)
        bottle.save()
        throwBottleStatus = dict()
        throwBottleStatus['ret']='0'
        throwBottleStatus['ret_msg']='ok'
        return HttpResponse(json.dumps(throwBottleStatus, ensure_ascii=False))
                                                                                           
