from django.shortcuts import render

import lit.models

# Create your views here.

def index(request):
    return django.http.HttpResponse(request, "Hello")

def bib(request):

    pubs = lit.models.Publication.objects.all()
    
    print(pubs)
    
    def process(pubs):
        for pub in pubs:
            s = pub.bib
            s = s.replace('\r\n', '</br>\r\n')
            yield s
    
    with open('/home/chuck/git/thesis/src/bibtex/mybib2.bib', 'w') as f:
        for pub in pubs:
            s = pub.bib
            s = s.replace('\r\n', '\n')
            s += '\n'
            f.write(s)
    
    context = {'bibs': process(pubs)}

    return render(request, 'lit/bib.bib', context)

