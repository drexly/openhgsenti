# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import *



class searchedAdmin(admin.ModelAdmin):
    fieldsets=[('사용자',{'fields':['usr']}),('isAPI',{'fields':['isapi']}),('IP주소',{'fields':['ipaddr']}),('검색내용',{'fields':['content']}),('검색의도',{'fields':['intent']}),('결과평점',{'fields':['star']}),('장르Top3',{'fields':['gnrs']}),('검색일시',{'fields':['update']})]
    list_display = ['usr','ipaddr','isapi','content','intent','star','gnrs','update']
    list_filter = ['usr','ipaddr','isapi','content','intent','update']
    search_fields =['usr','ipaddr','isapi','content','intent','update','gnrs']
    readonly_fields= ['usr','ipaddr','isapi','content','intent','star','gnrs','update']

admin.site.register(Searchedkey,searchedAdmin)




