import django.shortcuts

# Create your views here.

import climb.forms
import climb.models

def index(request):
    return django.shortcuts.render(request, 'climb/index.html', {})

def location_list(request):
    return django.shortcuts.render(
            request,
            'climb/location_list.html',
            {'locations':climb.models.Location.objects.all()})

def area_list(request):
    return django.shortcuts.render(
            request,
            'climb/area_list.html',
            {'areas':climb.models.Area.objects.all()})

def wall_list(request):
    return django.shortcuts.render(
            request,
            'climb/wall_list.html',
            {'walls':climb.models.Wall.objects.all()})

def route_list(request):
    return django.shortcuts.render(
            request,
            'climb/route_list.html',
            {'routes':climb.models.Route.objects.all()})

def route_create(request):
    if request.method == 'POST':
        form = climb.forms.route_create(request.POST)
        if form.is_valid():
            r = climb.models.Route()
            r.name     = form.cleaned_data['name']
            r.location = form.cleaned_data['location']
            r.area     = form.cleaned_data['area']
            r.wall     = form.cleaned_data['wall']
            r.save()

            return django.shortcuts.HttpResponseRedirect('/django/admin/climb/')
    else:
        form = climb.forms.route_create()

    return django.shortcuts.render(request, 'climb/route_create.html', {'form':form})

def pitch_list(request):
    return django.shortcuts.render(
            request,
            'climb/pitch_list.html',
            {'pitches':climb.models.Pitch.objects.all()})

    
    
def set_qs_0(form, a, b, c):
    #def set_qs_0(form, name_0, model0, name0, model_1, i, q):

    #print name_0, model0, name0, model_1, i

    if not b:
        c.q = c.model.objects.all()
        return None

    #i = form[name0].value()

    if not b.v:
        c.q = c.model.objects.none()
        c.v = None
        return None
    
    m0 = b.model.objects.get(pk=b.v)
    
    print "m0 = ",m0.id,m0.name
    
    if b:
        #if not (m0 in form.fields[name_0].queryset):
        if not (m0 in b.q):
            print "mismatch"
            c.q = c.model.objects.none()
            return None
    
    c.q = c.model.objects.filter(**{b.name:m0})

    if len(c.q) == 1:
        c.v = c.q[0].id

    

class myfield():
    def __init__(self, name, model):
        self.name = name
        self.model = model

def climb_create(request):
    if request.method == 'POST':
        form = climb.forms.climb_create(request.POST)
        if form.is_valid():
            c = climb.models.Climb()
            c.date  = form.date
            c.pitch = form.pitch
            c.save()

            return django.shortcuts.HttpResponseRedirect('/django/admin/climb/')
    else:
        form = climb.forms.climb_create()

    p=[
            None,
            None,
            myfield('location', climb.models.Location),
            myfield('area', climb.models.Area),
            myfield('wall', climb.models.Wall),
            myfield('route', climb.models.Route),
            myfield('pitch', climb.models.Pitch)]
    
    names = list(a.name for a in p[2:])
   
    for a in p[2:]:
        a.v = form[a.name].value()

    for ind in range(len(p))[2:]:

        print "ind",ind

        # temp is the queryset for field at ind

        temp = set_qs_0(
                form,
                p[ind-2],
                p[ind-1],
                p[ind-0]
                )
        
        #print a[1],b[1],c[1]
        print "quertyset ="
        print "\n".join("  {0} {1}".format(o.id,o.name) for o in p[ind].q)

    ini = dict([ (a.name, a.v) for a in p[2:] ])

    print ini

    form1 = climb.forms.climb_create(initial=ini)

    for a in p[2:]:
        form1.fields[a.name].queryset = a.q

    return django.shortcuts.render(request, 'climb/climb_create.html', {'form':form1})



