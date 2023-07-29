from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from WebApp.forms import YoutubeForm
from .models import Module, Registration, Student
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
    course = Group.objects.get(id=course_id)
    modules = Module.objects.filter(groups=course)
    return render(request, 'WebApp/list_modules.html', {'modules': modules, 'course': course})

@login_required
def registermod(request, module_id):
    module = Module.objects.get(id=module_id)
    student = request.user.student
    registration = Registration(student=student, module=module)
    registration.save()
    return redirect('module_detail', module_id=module_id)

@login_required
def unregister(request, registration_id):
    registration = Registration.objects.get(id=registration_id)
    registration.delete()
    return redirect('module_detail', module_id=registration.module.id)
def courses(request):
    courses = Group.objects.all()
    return render(request, 'WebApp/courses.html', {'courses': courses})

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

from django.shortcuts import render, redirect, get_object_or_404
from .forms import ModuleRegistrationForm, ModuleUnregistrationForm

@login_required
def module_detail(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    student = Student.objects.filter(user_id=request.user.id).first()
    registration_form = ModuleRegistrationForm(initial={'module': module})
    unregistration_form = ModuleUnregistrationForm(initial={'module': module})
    registered_students = Registration.objects.filter(module=module)
    print(student)

    if not student:
        return render(request, 'WebApp/module_detail.html', {
            'module': module,
            'is_registered': False,
            'registration_form': registration_form,
            'unregistration_form': unregistration_form,
            'registered_students': registered_students,
            'is_students':False
        })

    # Check if the student is registered for the module
    is_registered = Registration.objects.filter(student=student, module=module).exists()
    # Handle Module Registration
    if request.method == 'POST':
        if 'register' in request.POST:
            registration_form = ModuleRegistrationForm(request.POST)
            if registration_form.is_valid():
                if not is_registered:
                    registration = registration_form.save(commit=False)
                    registration.student = student
                    registration.module = module
                    registration.save()
                    is_registered=True

        elif 'unregister' in request.POST:
            unregistration_form = ModuleUnregistrationForm(request.POST)
            if unregistration_form.is_valid():
                is_registered = False
                # Find the registration entry and delete it
                registration_entry = Registration.objects.filter(student=student, module=module)
                registration_entry.delete()

        return render(request, 'WebApp/module_detail.html', {
            'module': module,
            'is_registered': is_registered,
            'registration_form': registration_form,
            'unregistration_form': unregistration_form,
            'registered_students': registered_students,
            'is_students': True
        })

    return render(request, 'WebApp/module_detail.html', {
        'module': module,
        'is_registered': is_registered,
        'registration_form': registration_form,
        'unregistration_form': unregistration_form,
        'registered_students': registered_students,
        'is_students': True
    })