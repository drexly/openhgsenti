import os,django,sys
#from quots.models import Inner
from django.contrib.auth.models import User
from quots.forms import *
from quots.models import *
from mysite import settings
from django.shortcuts import render,get_object_or_404

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
settings.configure()
django.setup()
def showinfo():
    allpr = In.objects.filter(orderer=get_object_or_404(Inner, username='inner0002'), type='pr', done=0)
    print(allpr)

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

    from django.core.management import execute_from_command_line

    showinfo()
    execute_from_command_line(sys.argv)