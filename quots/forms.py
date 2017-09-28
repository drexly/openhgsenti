#-*- coding: utf-8 -*-
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from quots.models import *


class RegistrationForm(forms.Form):

    username = forms.CharField(label='사용자 이름(ID)',min_length=8, max_length=30,help_text=("8~30자의 쉽지 않은 영문+숫자 조합입니다"))
    rname = forms.CharField(label='예금주(실명)', min_length=2, max_length=4, help_text=("2~4자의 한글실명입니다."))
    email = forms.EmailField(label='이메일',help_text=('회원정보 수정시 필요한 이메일 주소입니다.'))
    password1 = forms.CharField(label='비밀번호(PW)',widget=forms.PasswordInput(),help_text=("8~30자 입니다."),min_length=8,max_length=30)
    password2 = forms.CharField(label='비밀번호 재입력',widget=forms.PasswordInput())
    phone = forms.CharField(
        label=u'휴대전화',
        help_text=('01X-YYYY-ZZZZ 형식으로 숫자와 하이픈으로만 기입하세요.'),
    )
    content = forms.CharField(label=u'사용 목적', min_length=1, max_length=200, widget=forms.Textarea,
                              help_text=("사용 목적을 알려주세요"))
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if re.search(r'[가-힣]+', username):
            raise forms.ValidationError('아이디에 잘못된 문자가 들어가 있습니다. 한글 불가 합니다.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('이미 등록된 이름입니다. 다른 이름을 쓰세요')

    def clean_phone(self):
        phraw=self.cleaned_data['phone']
        if not str(phraw).__contains__('-'):
            raise forms.ValidationError('휴대전화번호에 하이픈이 없습니다.-로 구분해주세요.')
        else:
            comp=str(phraw).split('-')
            if len(comp) is not 3:
                raise forms.ValidationError('올바른 휴대전화번호 형식이 아닙니다.')
            else:
                for num in comp:
                    try:
                        int(num)
                    except:
                        raise forms.ValidationError('휴대전화번호에 문자가 있습니다.')

    def clean_rname(self):
        nameraw=self.cleaned_data['rname']
        if re.search(r'^[A-Za-z0-9_-]*$', nameraw):
            raise forms.ValidationError('이름은 순한글로만 입력하셔야 합니다.')
        else:
            return nameraw

    def clean_content(self):
        content=self.cleaned_data['content']
        if content is None:
            raise forms.ValidationError('사용 목적을 정확히 입력하세요')
        else:
            return content