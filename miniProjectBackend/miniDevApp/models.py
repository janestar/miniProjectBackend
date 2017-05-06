# -*- coding:utf-8 -*-
from django.db import models

# Create your models here.
class UserInfo(models.Model):
    qqId = models.CharField(max_length=50,primary_key=True)
    phoneNumber = models.CharField(max_length=20)
    userAddress = models.CharField(max_length=100)
    userPostion = models.CharField(max_length=100)
    userImageUrl = models.CharField(max_length=100)
    userNickName = models.CharField(max_length=20)
    def __str__(self):
        return self.userNickName
    def getDict(self):
        info = dict()
        info["qqId"] = self.qqId
        info["phoneNumber"] = self.phoneNumber
        info["userAddress"] = self.userAddress
        info["userPostion"] = self.userPostion
        info["userImageUrl"] = self.userImageUrl
        info["userNickName"] = self.userNickName
        return info

class BottleInfo(models.Model):
    bottleId = models.BigAutoField(default=1, primary_key=True)
    bottleUserInfo = models.ForeignKey(UserInfo,on_delete=models.PROTECT)
    bottleName = models.CharField(max_length=30)
    bottleStatus = models.IntegerField()
    bottlePrice = models.DecimalField(max_digits=10,decimal_places=2)
    bottleInfo = models.CharField(max_length=100)
    bottleImageUrl = models.CharField(max_length=100)
    sendTimestamp = models.DateField(auto_now= True)
    def __str__(self):
        return self.bottleId
    def getDict(self):
        info = dict()
        info["itemId"] = self.bottleId
        info["itemName"] = self.bottleName
        info["itemDesc"] = self.bottleInfo
        info["imgUrl"] = self.bottleImageUrl
        info["itemStatus"] = self.bottleStatus
        return info
    def randomChooseBottle(self):

        randomBottle = dict()
        randomBottle["action"]="get"
        randomBottle["resetStatus"]="1"
        randomBottle["message"]="ok"
        randomBottle["bottleId"]="123"
        randomBottle["bottleName"]="test"
        randomBottle["bottlePrice"]="10"
        randomBottle["bottleInfo"]="test111"
        randomBottle["bottleImage"]="test/test.jpg"
        randomBottle["sendTimestamp"]="12:13:14"
        return randomBottle




class WishList(models.Model):
    wish_bottleId = models.BigAutoField(default=1, primary_key=True)
    wishUserInfo = models.ForeignKey(UserInfo, on_delete=models.PROTECT)
    bottleStatus = models.IntegerField()
    def __str__(self):
        return self.wish_bottleId

class ReportList(models.Model):
    report_bottleId = models.BigAutoField(default=1, primary_key=True)
    qqId = models.ForeignKey(UserInfo, on_delete=models.PROTECT)
    def __str__(self):
        return self.report_bottleId




