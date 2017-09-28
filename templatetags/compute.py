#from django.template.defaulttags import register
from django import template
register = template.Library()


@register.filter
def get_item(dictionary, key):
   return dictionary.get(key)
@register.filter
def percent(value, arg):
   return round(value/arg*100,2)

@register.filter
def contains(string,keyword):
   if str(string).__contains__(str(keyword)):
      return True
   else:
      return False

@register.filter(name='split')
def split(value, key):
    rst=[]
    items=value.split(key)
    for item in items:
        rst.append(str(item).lstrip().rstrip())
    """
        Returns the value turned into a list.
    """
    return rst

@register.filter(name='answered')
def answered(inid,myouts):
    if myouts is None:
        return False
    else:
        for out in myouts:
            if out.parent_id==inid:
                return True
        return False

@register.filter(name='LCalc')
def LCalc(inobj):
    picnum = 0
    if inobj.pic1 != '':
        picnum+=1
    if inobj.pic2 != '':
        picnum+=1
    if inobj.pic3 != '':
        picnum+=1
    if inobj.pic4 != '':
        picnum+=1
    if inobj.pic5 != '':
        picnum+=1
    if inobj.pic6 != '':
        picnum+=1
    return str(11-picnum)

@register.filter(name='RCalc')
def RCalc(inobj):
    picnum = 0
    if inobj.pic1 != '':
        picnum+=1
    if inobj.pic2 != '':
        picnum+=1
    if inobj.pic3 != '':
        picnum+=1
    if inobj.pic4 != '':
        picnum+=1
    if inobj.pic5 != '':
        picnum+=1
    if inobj.pic6 != '':
        picnum+=1
    return str(picnum+1)