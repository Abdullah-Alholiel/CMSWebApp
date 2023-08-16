from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookForm, ModuleRegistrationForm, ModuleUnregistrationForm
from WebApp.forms import YoutubeForm
from .models import Course, Module, Registration, Student, StudentGroup
from django.contrib.auth.models import Group
from youtubesearchpython import VideosSearch
from requests import get
import requests
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Home page view
def home(request):
    user = request.user
    template_name = "home.html"
    courses = StudentGroup.objects.all()
    modules = Module.objects.all() 
    api_key = 'b18758d6289ebcfc5d2a847e86d253e5'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={},{}&units=metric&appid={}'
    
    cities = ['London', 'Sheffield', 'Liverpool', 'Manchester']

    weather_data = []

    for city in cities:
        try:
            city_weather = requests.get(url.format(city, 'UK', api_key)).json()
            weather = {
                'city': city_weather['name'],
                'temperature': city_weather['main']['temp'],
                'description': city_weather['weather'][0]['description']
            }
            weather_data.append(weather)
        except Exception as e:
            print(f"Error fetching weather data for {city}: {str(e)}")

    context = {"user": user, 'courses': courses,'modules': modules, 'weather_data': weather_data}
    return render(request, template_name, context)

def about_us(request):
    courses = StudentGroup.objects.all()
    return render(request, 'about.html', {'courses': courses})


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
        courses = StudentGroup.objects.all()
        return render(request, 'contact.html', {'courses': courses})


def course_list_modules(request, course_id):
    course = StudentGroup.objects.get(id=course_id)
    modules = Module.objects.filter(groups=course)
    courses = StudentGroup.objects.all()
    return render(request, 'list_modules.html', {'modules': modules, 'course': course, 'courses': courses})


@login_required
def registermod(request, module_id):
    module = Module.objects.get(id=module_id)
    student = Student.objects.filter(user=request.user).first()
    registration = Registration.objects.filter(student=student, module=module).first()
    if registration:
        return redirect('module_detail', module_id=module_id)
    registration = Registration(student=student, module=module)
    registration.save()
    return redirect('module_detail', module_id=module_id)

@login_required
def unregister(request, registration_id):
    registration = Registration.objects.get(id=registration_id)
    registration.delete()
    return redirect('module_detail', module_id=registration.module.id)


def courses(request):
    student = Student.objects.filter(user = request.user).first()
    course = Course.objects.filter(student=student).first()
    modules = course.group.modules.all()
    courses = StudentGroup.objects.all()
   # import pdb; pdb.set_trace()
    return render(request, 'courses.html', {'modules': modules, 'courses': courses})


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
        return render(request, 'youtube.html', context)
    else: 
        courses = StudentGroup.objects.all()
        form = YoutubeForm()
    context = {'form': form, 'courses': courses}
    return render(request, "youtube.html", context)

def book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():  # Ensure the form data is valid
            text = form.cleaned_data['text']  # Use cleaned_data to get the value from the form
            url = f"https://www.googleapis.com/books/v1/volumes?q={text}"
            r = requests.get(url)
            if r.status_code == 200:
                answer = r.json()
                result_list = []
                for item in answer.get('items', [])[:10]:
                    volume_info = item.get('volumeInfo', {})
                    result_dict = {
                        'title': volume_info.get('title'),
                        'subtitle': volume_info.get('subtitle', ''),
                        'description': volume_info.get('description', ''),
                        'count': volume_info.get('pageCount', 0),
                        'categories': volume_info.get('categories', []),
                        'rating': volume_info.get('averageRating', 0),
                        'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', ''),
                        'preview': volume_info.get('previewLink', ''),
                    }
                    result_list.append(result_dict)
                context = {
                    'form': form,
                    'results': result_list
                }
                return render(request, 'book.html', context)
            else:
                context = {
                    'form': form,
                    'error_message': f"Error: Unable to fetch data from the API. Status Code: {r.status_code}"
                }
        else:
            context = {
                'form': form,
                'error_message': "Error: Invalid form data. Please provide a valid search query."
            }
    else: 
        courses = StudentGroup.objects.all()
        form = BookForm()
        context = {'form': form, 'courses': courses}
    return render(request, "book.html", context)

class PostListView(ListView):
    model = Student
    template_name = 'template/module_detail.html'
    context_object_name = 'registered_students'
    paginate_by = 1
    

def module_detail(request, module_code):
    module = get_object_or_404(Module, code=module_code)
    student = Student.objects.filter(user_id=request.user.id).first()
    registration_form = ModuleRegistrationForm(initial={'module': module})
    unregistration_form = ModuleUnregistrationForm(initial={'module': module})
    registered_students = Registration.objects.filter(module=module)

    paginator = Paginator(registered_students, 2)  # Show 1 student per page for demo

    page = request.GET.get('page')
    try:
        students_page = paginator.page(page)
    except PageNotAnInteger:
        students_page = paginator.page(1)
    except EmptyPage:
        students_page = paginator.page(paginator.num_pages)

    if not student:
        is_students = False
        is_registered = False
    else:
        is_students = True
        is_registered = Registration.objects.filter(student=student, module=module).exists()

    if request.method == 'POST':
        if 'register' in request.POST:
            registration_form = ModuleRegistrationForm(request.POST)
            if registration_form.is_valid() and not is_registered:
                registration = registration_form.save(commit=False)
                registration.student = student
                registration.module = module
                registration.save()
                is_registered = True
        elif 'unregister' in request.POST:
            unregistration_form = ModuleUnregistrationForm(request.POST)
            if unregistration_form.is_valid():
                is_registered = False
                registration_entry = Registration.objects.filter(student=student, module=module)
                registration_entry.delete()

    return render(request, 'module_detail.html', {
        'module': module,
        'is_registered': is_registered,
        'registration_form': registration_form,
        'unregistration_form': unregistration_form,
        'registered_students': students_page,  # Note: Pass the paginated object here
        'is_students': is_students
    })