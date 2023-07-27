from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from WebApp.forms import YoutubeForm
from .models import Module, Registration
from django.contrib.auth.models import Group
from youtubesearchpython import VideosSearch

def home(request):
    courses = Group.objects.all()
    return render(request, 'WebApp/home.html', {'courses': courses})

def about_us(request):
    return render(request, 'WebApp/about.html')

def contact(request):
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        # TODO: Send email using the provided information
        return redirect('contact')
    else:
        return render(request, 'WebApp/contact.html')

def list_modules(request, course_id):
    course = Group.objects.get(pk=course_id)
    modules = Module.objects.filter(course=course)
    return render(request, 'WebApp/list_modules.html', {'modules': modules, 'course_id': course_id})

@login_required
def registermod(request, module_id):
    module = Module.objects.get(id=module_id)
    student = request.user.student
    registration = Registration(student=student, module=module)
    registration.save()
    return redirect('list_modules')

@login_required
def unregister(request, registration_id):
    registration = Registration.objects.get(id=registration_id)
    registration.delete()
    return redirect('list_modules')

def youtube(request):
    if request.method == 'POST':
        form = YoutubeForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit = 5)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel' : i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published':i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
                result_dict['description'] = desc
            result_list.append(result_dict)
        context = {
            'form': form,
            'results': result_list
        }
        return render(request, 'WebApp/youtube.html', context)
    else: 
        form = YoutubeForm()
    context = {'form': form}
    return render(request, "WebApp/youtube.html", context)
