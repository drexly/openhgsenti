# -*- coding: utf8 -*-

#from __future__ import unicode_literals
from elasticsearch import Elasticsearch
import numpy as np
from collections import Counter
from django.shortcuts import render,get_object_or_404
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from quots.forms import *
from django.contrib.auth import authenticate, login
from quots.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from urllib.parse import unquote
import json
from ipware.ip import get_ip
from django.utils import timezone
import pytz

def softmax(x):
    return (10-(np.exp(x) / np.sum(np.exp(x), axis=0)))/10

def gnrfreq(s):
    ordered=sorted(sorted(Counter(s.split()).most_common(), key=lambda pair: pair[0], reverse=False), key=lambda pair: pair[1],
           reverse=True)
    sumofv=0
    for k,v in ordered:
        sumofv+=v
    if sumofv is 100:
        return ordered
    else:
        inpercent=[]
        for k, v in ordered:
            inpercent.append((k,round((v/sumofv)*100,2)))
        return inpercent

def essearch(keyword):
    context = {}
    es = Elasticsearch("210.94.194.82:9200")
    res = es.search(index="mov", sort={"good": "desc"}, size=100, doc_type="cmt",
                    body={"query": {"match": {"cmt": keyword}}})
    resdic = {}
    resavg = []
    gnrstr = ""
    for elem in res['hits']['hits']:
        for gnr in elem['_source']['gnr']:
            gnrstr += (gnr + " ")
        # find mids containing keyword
        #submid = es.search(index="mov", sort={"good": "desc"}, size=100, doc_type="cmt",
        #                   body={"query": {"match": {"mid": elem['_source']['mid']}}})

        submid = es.search(index="mov", sort={"good": "desc"}, size=100, doc_type="cmt", \
                           body={"query":
                               {
                                   "bool":
                                       {
                                           "should": {
                                               "term": {
                                                   "rid":
                                                       elem['_source']['rid']
                                               }
                                           },
                                           "filter":
                                               {
                                                   "term":
                                                       {
                                                           "mid":
                                                               elem['_source']['mid']
                                                       }
                                               },
                                       }
                               }
                           }
                           )

        gbdif = []

        for subelem in submid['hits']['hits']:
            gbdif.append(-(subelem['_source']['good'] - subelem['_source']['bad']))

        if np.max(gbdif) > 0:
            gbdif = gbdif - np.max(gbdif)

        rates = softmax(gbdif)

        for ind, resubelem in enumerate(submid['hits']['hits']):
            if resubelem['_source']['rid'] == elem['_source']['rid']:
                starval = rates[ind] * elem['_source']['star']
                resdic[elem['_source']['rid']] = [starval, elem['_source']['cmt']]
                resavg.append(starval)

    context['proof'] = resdic
    context['gnr'] = gnrfreq(gnrstr)
    if len(resavg) > 0:
        context['avg'] = np.average(resavg)
    else:
        context['avg'] = -1
    context['key']=keyword
    return context


def search(request):
    ip = get_ip(request)
    if request.method == 'POST':
        usr = User.objects.filter(username=request.user)
        ip = get_ip(request)
        rst = essearch(request.POST['keyword'])
        intent=None
        gnr = ""
        for i, (k, v) in enumerate(rst['gnr']):
            if i is 3:
                break
            else:
                gnr += (k + "|")
        if len(usr) is 1:
                try:
                    intent=str(usr[0].last_name).split('|')[1]
                except:
                    pass
                obj = Searchedkey(usr=usr[0],
                                  ipaddr=str(ip),
                                  content=request.POST['keyword'],
                                  star=rst['avg'],
                                  gnrs=gnr,
                                  isapi=False,
                                  update=datetime.datetime.now(tz=pytz.UTC),
                                  intent=intent
                                  )
                obj.save()
        else:
            obj = Searchedkey(usr=None,
                              ipaddr=str(ip),
                              content=request.POST['keyword'],
                              star=rst['avg'],
                              gnrs=gnr,
                              isapi=False,
                              update=datetime.datetime.now(tz=pytz.UTC),
                              intent=intent
                              )
            obj.save()
        return render(request, 'search.html', rst)


def index(request):
    context = {}
    return render(request, 'index.html', context)



def apicall(request):
    context = {}
    return render(request, 'apicall.html', context)

def jsonapi(request,userid,keyword):
    usr=User.objects.filter(username=userid)
    ip = get_ip(request)
    intent=None
    if len(usr) is 1:
        rst=essearch(keyword)
        gnr=""
        try:
            intent = str(usr[0].last_name).split('|')[1]
        except:
            pass
        for i,(k,v) in enumerate(rst['gnr']):
            if i is 3:
                break
            else:
                gnr+=(k+"|")
        js = json.dumps(rst, ensure_ascii=False)

        obj = Searchedkey(usr=usr[0],
                      ipaddr=str(ip),
                      content=keyword,
                      star=rst['avg'],
                      gnrs=gnr,
                      isapi=True,
                      update=datetime.datetime.now(),
                        intent=intent
                          )
        obj.save()
        return HttpResponse(js, content_type=u"application/json; charset=utf-8", status=200)
    else:
        rst={"err":"오픈한글감성사전에 등록된 유저가 아닙니다"}
        js = json.dumps(rst, ensure_ascii=False)
        return HttpResponse(js, content_type=u"application/json; charset=utf-8", status=500)





def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            meta=str(form.cleaned_data['phone']) + '|' + str(form.cleaned_data['content'])
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password1'],
                                            email=form.cleaned_data['email'], first_name=form.cleaned_data['rname'],
                                            last_name=meta
                                           )

            login(request,user)

            return HttpResponseRedirect('/')
        else:
            context={'form': form}
            return render(request, 'registration/register.html',context)
    form = RegistrationForm()
    context={'form': form}
    return render(request, 'registration/register.html',context)