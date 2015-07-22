from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import django.contrib.auth
from django.http import HttpResponse, HttpResponseRedirect
from django.forms.util import ErrorList
from django.core.context_processors import csrf
from django.contrib.auth import authenticate
import django.utils.datastructures
import django.core.files.base

import os
import re
import json
import copy

import jobdata.forms
import jobdata.html
import myjson

def clean(s):
    s = s.replace('.','_')
    s = s.replace('@','_')
    return s

def form_signup(request):

    if request.method == 'POST':
        form = jobdata.forms.signup(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            pw1 = form.cleaned_data['pw1']
            pw2 = form.cleaned_data['pw2']
    
            try:
                user = User.objects.create_user(
                    username,
                    email,
                    pw1)
            except:
                errors = form._errors.setdefault("username", ErrorList())
                errors.append(u"username not unique")

                return render(request, 'jobdata/form_signup.html', {'form':form})
           
            return HttpResponse("signup success")
    else:
        form = jobdata.forms.signup()
    
    return render(request, 'jobdata/form_signup.html', {'form':form})

def form_login(request):
    #rint "views.form_login"

    redirect = request.POST['redirect']
    redirect_url = request.POST['redirect_url']

    if request.method == 'POST':
        form = jobdata.forms.login(request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Redirect to a redirect page.
                    return my_render(request, redirect, redirect_url, None)
                else:
                    return HttpResponse("disabled account")
                    # Return a 'disabled account' error message
            else:
                return HttpResponse("invalid login")
                # Return an 'invalid login' error message.
    else:
         form = jobdata.forms.login()
   
    c = {
            'redirect':redirect,
            'redirect_url':redirect_url,
            'form':form,
            }

    return render(request, 'jobdata/form_login.html', c)

def my_render(request, redirect, redirect_url, user):
    #rint "views.my_render", redirect

    if redirect == 'jobdata:json_editor':
        return json_editor(request)

    c = {
            'redirect':redirect,
            'redirect_url':redirect_url,
            }
    
    return render(request, redirect_url, c)

def logout(request):
    #rint "views.logout"
    
    django.contrib.auth.logout(request)
   
    # Redirect to a success page
    #rint request.user
    #rint request.user.is_authenticated()

    redirect     = request.POST['redirect']
    redirect_url = request.POST['redirect_url']
    
    c = {
            'redirect':redirect,
            'redirect_url':redirect_url,
            }
   
    return my_render(request, redirect, redirect_url, None)


def json_editor(request):
    #rint "views.json_editor"
 
    user = request.user

    # authenticate user
    r = auth_check(request, 'json_editor')
    if r is not None:
        return r

    person = jobdata.models.Person.objects.get(user=user)

    try:
        j_str = request.POST['json']
        person.file_write(j_str)
    except django.utils.datastructures.MultiValueDictKeyError:
        #j_str = person.file_read()
        pass

    person.validate_json()

    j_str = person.file_read()

    c = {
            'json'        :j_str,
            'redirect'    :'jobdata:json_editor',
            'redirect_url':'jobdata/json_editor.html',
            }
    
    return render(request, 'jobdata/json_editor.html', c)

def auth_check(request, page):
    #rint "views.auth_check", page
    
    user = request.user
    if request.user.is_authenticated():
        return None

    #rint "auth failed"

    c = {
            'form':jobdata.forms.login(),
            'redirect':"jobdata:{}".format(page),
            'redirect_url':"jobdata/{}.html".format(page),
            }

    return render(request, "jobdata/form_login.html", c)

import python_resume



def json_render(request):
    #rint "views.json_render"
 
    user = request.user

    # authenticate user
    r = auth_check(request, 'json_render')
    if r is not None:
        return r

    person = jobdata.models.Person.objects.get(user=user)

    f = person.file
    
    if f:
        j = f.read()
    else:
        j = "{}"

    if request.method == 'POST':
        form = jobdata.forms.json_render(request.POST)
        if form.is_valid():
            version  = form.cleaned_data['version']

            g = python_resume.Generator(
                    version=version,
                    )

            g.load_json(j)
            g.filt(version)

            j = g.info
    else:
        form = jobdata.forms.json_render()

    c = {
            'form':form,
            'json':j,
            'redirect':'jobdata:json_render',
            'redirect_url':'jobdata/json_render.html',
            }
    
    return render(request, 'jobdata/json_render.html', c)

def document_render(request, document_id):
    #rint "views.document_render", request.method
    
    document = jobdata.models.Document.objects.get(pk=document_id)
    user = request.user
    
    # authenticate user
    r = auth_check(request, 'document_render')
    if r is not None:
        return r

    # options
    if request.method == 'POST':
        document.options = request.POST['options']
        document.save()

    options_json = document.get_options_json()

    # get user data
    person = jobdata.models.Person.objects.get(user=user)
    person.validate_json()
    j = person.file_read_json()
    
    # generate json selector in order to get paths list
    def json_html_filter(x):
        if isinstance(x, dict):
            if x.has_key('version'):
                s0 = set(x['version'])
                s1 = set(options_json['version'])
                res = s0.issubset(s1)
                #rint "comparing {} {} {}".format(s0,s1,res)
                if not s0.issubset(s1):
                    return False
        return True

    _,paths = jobdata.html.json_to_html(j, document.id, json_html_filter)
    
    #rint "\n".join(
    #        ["paths"]+list("    {} {}".format(p,myjson.get_element(j,p + ['_selector'])) for p in paths))



    # extract values from json_html
    if request.method == 'POST':
        for k,v in request.POST.items():
            m = re.match("^selector_(.*)$", k)
            if m:
                #s = m.group(1).split(',')
                s = myjson.path_str_to_list(m.group(1))

                # remove element from paths list
                paths.remove(s)

                sel = myjson.get_element(j,s + ['_selector'])

                #rint "   ",s,sel[str(document.id)],v
                sel[str(document.id)] = True
                #rint "   ",s,sel[str(document.id)],v

        # remaining path are unchecked
        #rint "remaining paths"
        for p in paths:
            #rint "   ",p
            o = myjson.get_element(j,p)
            sel = o['_selector']
            sel[str(document.id)] = False

        # write json
        person.file_write_json(j)

    # filter json based on version so that json_html
    # doesnt have unessesary elements
    #python_resume.filter_json(j, options_json['version'])

    # json filter out elements without selectors
    j_selector = copy.deepcopy(j)

    def temp_test(x):
        if isinstance(x, dict):
            #rint "temp_test"
            if x.has_key(u'_selector'):
                #rint "TRUE"
                return True
        return False
   
    myjson.filt_test(j_selector, temp_test)

    # generate json selector again
    #json_html,_ = jobdata.html.json_to_html(j_selector, document.id)
    json_html,_ = jobdata.html.json_to_html(j, document.id, json_html_filter)

    # render document
    g = python_resume.Generator(
            version=options_json['version'],
            order=options_json['order'])
    
    if document.position:
        g.company  = document.position.company.name
        g.position = document.position.name

    g.load_json(j)
    g.filt(options_json['version'], document.id)

    h,t = os.path.splitext(document.template.path)

    # save to file
    html = g.render_text(name = h, fmt = t)

    #rint "write to", repr(document.filename())
    
    document.file_write_str(html)

    # response
    c = {
            'document': document,
            'json_html':json_html,
            }

    return render(request, 'jobdata/document_render.html', c)

def document_view(request, document_id):
    document = jobdata.models.Document.objects.get(pk=document_id)
    user = request.user
    
    # authenticate user
    r = auth_check(request, 'document_render')
    if r is not None:
        return r

    options_json = document.get_options_json()
    
    # get user data
    person = jobdata.models.Person.objects.get(user=user)
    person.validate_json()
    j = person.file_read_json()
    
    # render document
    g = python_resume.Generator(
            version=options_json['version'],
            order=options_json['order'])
    
    if document.position:
        g.company  = document.position.company.name
        g.position = document.position.name

    g.load_json(j)
    g.filt(options_json['version'], document.id)

    h,t = os.path.splitext(document.template.path)
    html = g.render_text(name=h,fmt=t)
    
    # response
    c = {'html':html}
    return render(request, 'jobdata/blank.html', c)
    

def document_list(request):
    
    documents = jobdata.models.Document.objects.all()
    
    def srt(x):
        if x.position:
            return x.position.company
        return x.template.path

    documents = sorted(documents, key=srt)
    
    c = {'documents':documents}
    
    return render(request, 'jobdata/document_list.html', c)
    
def company(request, company_id):
    company = jobdata.models.Company.objects.get(pk=company_id)
    c = {'company':company}
    return render(request, 'jobdata/company.html', c)

def position(request, position_id):
    position = jobdata.models.Position.objects.get(pk=position_id)
    c = {'position':position}
    return render(request, 'jobdata/position.html', c)


