# -*-coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import simplejson
from miniDevApp.models import BottleInfo

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
