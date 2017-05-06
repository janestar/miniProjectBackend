# -*-coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import simplejson
from miniDevApp.models import BottleInfo
#from django.views.decorators.csrf import ensure_csrf_cookie
#from django.views.decorators.csrf import csrf_exempt
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



#@ensure_csrf_cookie
#@csrf_exempt
def confirmBargain(request):
    if(request.method=="POST"):
        '''
        itemId = request.POST['itemId']
        print("test2 confirmBargain")
        bottle_info = BottleInfo.objects.filter(bottleId=itemId)
        bottle_info.bottleStatus = 1
        bottle_info.save()
        #DICT = {‘ret’:'0', 'ret_msg':'确认成功'}
        '''
        #itemId = request.POST.get("itemId")
        #print("test2 confirmBargain %s" %itemId)
        #bottle_info = BottleInfo.objects.filter(bottleId=itemId)
        #print(request.body)

    bargainStatus = dict()
    bargainStatus['ret']='0'
    bargainStatus['ret_msg']='确认成功'
    return HttpResponse(simplejson.dumps(bargainStatus, ensure_ascii=False))

#@ensure_csrf_cookie
#@csrf_exempt
def cancelBargain(request):
    itemId = request.POST['itemId']
    bottle_info = BottleInfo.objects.filter(bottleId=itemId)
    bottle_info.bottleStatus = -1
    bottle_info.save()
   # DICT = {‘ret’:'0', 'ret_msg':'删除成功'}
    bargainStatus = dict()
    bargainStatus['ret']='0'
    bargainStatus['ret_msg']='删除成功'
    return HttpResponse(simplejson.dumps(bargainStatus, ensure_ascii=False))
