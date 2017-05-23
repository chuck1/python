from django.shortcuts import render

import tasks

import markdown
#import subprocess
#import logging

#logger = logging.getLogger(__name__)

# Create your views here.

def index(request):
    """
    cmd = '/home/chuck/git/chuck1/c-testing/external/opencv/test0/a.out'
    cmd = 'webcam'

    dst = '/home/chuck/git/chuck1/python/test/django/mysite/static/wiki/webcam/image.jpg'
    #dst = '/home/chuck/image.jpg'

    p = subprocess.Popen([cmd, dst], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = p.communicate()
    
    #if(err)
    #raise(object)

    logger.warning(cmd)
    logger.warning(out)
    logger.warning(err)
    """

    #tasks.test.apply_async((), expires=1)

    context = {}
    return render(request, 'wiki/index.html', context)

def page(request, page):

	context = {}

	filename = '/home/chuck/git/desktop_server_public/wiki/' + page + '.md'
	
	try:
		with open(filename, 'r') as f:
			text = f.read()
	except:
		context['text'] = repr(filename) + ' not found'
	else:
		html = markdown.markdown(text, extensions=['markdown.extensions.tables'])

		context['text'] = html

	return render(request, 'wiki/page.html', context)

