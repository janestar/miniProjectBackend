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
from math import *
import random
import decimal,datetime


class DecimalJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalJSONEncoder, self).default(o)


class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def haversine(Lat_A, Lng_A, Lat_B, Lng_B):
    if Lat_A == Lat_B and Lng_A == Lng_B:
       return 0
    ra = 6378.140  # 赤道半径 (km)
    rb = 6356.755  # 极半径 (km)
    flatten = (ra - rb) / ra  # 地球扁率
    rad_lat_A = radians(Lat_A)
    rad_lng_A = radians(Lng_A)
    rad_lat_B = radians(Lat_B)
    rad_lng_B = radians(Lng_B)
    pA = atan(rb / ra * tan(rad_lat_A))
    pB = atan(rb / ra * tan(rad_lat_B))
    xx = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(rad_lng_A - rad_lng_B))
    c1 = (sin(xx) - xx) * (sin(pA) + sin(pB)) ** 2 / cos(xx / 2) ** 2
    c2 = (sin(xx) + xx) * (sin(pA) - sin(pB)) ** 2 / sin(xx / 2) ** 2
    dr = flatten / 8 * (c1 - c2)
    distance = ra * (xx + dr)
    return '%.2f' % distance


def randomAlgorithm(pos):
    #longandlat =  pos.split(",")
    rows = BottleInfo.objects.filter().count()
    print("rows is %d"%rows)

    while True:
        randnum = random.randint(0,rows-1)
        bottleobj = BottleInfo.objects.all()[randnum]
        if bottleobj.bottleStatus != '1':
            return bottleobj
    return None

def randomChooseBottleId(userid):
      user_info_set =  UserInfo.objects.filter(qqId=userid)
      for user_info in user_info_set:
          pos = user_info.userPostion
          bottleobj = randomAlgorithm(pos)
          # userlongandlat = pos.split(",")
          # bottlelongandlat = bottleobj.pos.split(",")
          # dis= haversine(userlongandlat[0],userlongandlat[1],bottlelongandlat[0],bottlelongandlat[1])
          return bottleobj

def getlongandlat(userid,botid):
    user_info_set = UserInfo.objects.filter(qqId=userid)
    bottle_info_set = BottleInfo.objects.filter(bottleId=botid)
    user_pos =''
    bottle_pos = ''
    for user_info in user_info_set:
         user_pos = user_info.userPostion.split(',')
    for bottle_info in bottle_info_set:
         bottle_pos = bottle_info.bottlePostion.split(',')
    dist = haversine(float(user_pos[0]),float(user_pos[1]),float(bottle_pos[0]),float(bottle_pos[1]))
    return dist

def getBottle(request):
    bottle_list = []
    if(request.method=='POST'):
        print("into getBottle succeed")
        form = bottleForm(request.POST)
        if form.is_valid():
           action = form.cleaned_data['action']
           uid = form.cleaned_data['uid']
           print("action is%s"%(action))
           if(action == "get"):
               print("uid is %s"%uid)
               bottleobj = randomChooseBottleId(uid)
               bottleobj_id = bottleobj.bottleId
               print("bottleobj_id is %s"%bottleobj_id)
               #bottle_info = BottleInfo.objects.filter(bottleId=bottleobj_id)
               #for bottle in bottle_info:
               #    bottle_list.append(bottle.randomChooseBottle())
               bottle_info_dict = bottleobj.randomChooseBottle()
               dist_res = getlongandlat(uid,bottleobj_id)
               dist_dict = {"dist":dist_res}
               bottle_info_dict.update(dist_dict)
               bottle_list.append(bottle_info_dict)
               for b_list in bottle_list:
                   print("b_list is %s"%b_list)
           else:
               randomBottle = dict()
               bottleId = form.cleaned_data['bottleId']
               bottlestat = form.cleaned_data['bottleStatus']
               user_info_set =  UserInfo.objects.filter(qqId=uid)
               print("user_info is herer")
               for user_info in user_info_set:
                    ret = WishList.objects.get_or_create(wish_bottleId=bottleId,wishUserInfo=user_info,bottleStatus=bottlestat)
              	    if ret[1] == True:
              	   	 randomBottle["action"] = "reset"
              	   	 randomBottle["resetStatus"] = "0"
              	   	 randomBottle["message"] = "succeed"
                    else:
              		 randomBottle["action"] = "reset"
              		 randomBottle["resetStatus"] = "1"
              		 randomBottle["message"] = "record already exist"
                    bottle_list.append(randomBottle)
        else:
            print("form is not valid")
    return HttpResponse(json.dumps(bottle_list, ensure_ascii=False,cls=MyEncoder))






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

def report(request):
    if(request.method=='POST'):
        data = json.loads(request.body)
        uid = data['uid']
        bottleId = data['bottleId']
        reports = ReportList.objects.filter(report_bottleId=bottleId, qqId=uid)
        reportStatus = dict()
        if reports:
            reportStatus['ret']='1'
            reportStatus['ret_msg']='你已举报过'
        else:
            report=ReportList()
            report.report_bottleId = bottleId
            report.qqId = UserInfo.objects.get(qqId=uid)
            report.save()
            reportStatus['ret']='0'
            reportStatus['ret_msg']='ok'
        return HttpResponse(json.dumps(reportStatus, ensure_ascii=False))

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
                                                                                           

