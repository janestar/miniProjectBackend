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
