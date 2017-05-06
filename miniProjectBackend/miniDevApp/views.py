# -*-coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import simplejson
from miniDevApp.models import BottleInfo
from miniDevApp.models import WishList
from miniDevApp.models import UserInfo
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
        return HttpResponse(simplejson.dumps({"itemList":bottle_list}, ensure_ascii=False))        



def getItemDetail(request):
    itemId = request.GET['itemId']
    bottle_info = BottleInfo.objects.filter(bottleId=itemId)
    bottle_list = []
    for bottle in bottle_info:
        bottle_list.append(bottle.getDict())
    return HttpResponse(simplejson.dumps(bottle_list, ensure_ascii=False))
def confirmBargain(request):
    itemId = request.POST['itemId']
    bottle_info = BottleInfo.objects.filter(bottleId=itemId)
    bottle_info.bottleStatus = 1
    bottle_info.save()
    DICT = {‘ret’:'0', 'ret_msg':'确认成功'}
    return HttpResponse(simplejson.dumps(DICT, ensure_ascii=False))
def cancelBargain(request):
    itemId = request.POST['itemId']
    bottle_info = BottleInfo.objects.filter(bottleId=itemId)
    bottle_info.bottleStatus = -1
    bottle_info.save()
    DICT = {‘ret’:'0', 'ret_msg':'删除成功'}
    return HttpResponse(simplejson.dumps(DICT, ensure_ascii=False))


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
                                                                                                   
