# -*-coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
#import simplejson
import json
from miniDevApp.models import BottleInfo
from miniDevApp.models import WishList
from miniDevApp.bottleform import bottleForm
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





