from django.shortcuts import render,HttpResponse,redirect, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import *
from django.core.paginator import  PageNotAnInteger, EmptyPage, Paginator# Create your views here.
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from .forms import *
from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.db.models import Count








def home(request):
    author = Author.objects.all()
    total_author = author.count()
    
    course = Course.objects.all()
    total_course = course.count()
    enrollments = Enrollment.objects.filter(approved=True)
    total_enrolled_students = enrollments.count()
    courses = Course.objects.order_by('-created_date')[:9]
    context = {
        'total_enrolled_students':total_enrolled_students,
        'total_course': total_course,
        'total_author': total_author,
        'courses': courses,
    }
    return render(request, 'home.html', context)


def courses(request):
    course = Course.objects.all()
    total_course = course.count()
    queryset = Course.objects.order_by('-created_date')
    page = request.GET.get('page',1)
    paginator = Paginator(queryset,9)
    try:
        courses = paginator.page(page)
    except EmptyPage:
        courses = paginator.page(1)
    except PageNotAnInteger:
        courses = paginator.page(1)
        return redirect('home')

#   end pagination

    context = {
        'courses': courses,
        'paginator': paginator,   
        'total_course':total_course,   
    }
    return render (request, 'courses.html', context)

@login_required(login_url='login')
def course_details(request, slug):   
    course = Course.objects.get(slug=slug)
    enrollments = Enrollment.objects.filter(user=request.user, course=course)
    total_enroll = Enrollment.objects.filter(course=course)
    total_enrolled_students = total_enroll.count()
    related_courses = Course.objects.filter(category=course.category).exclude(slug=slug)[:5]
    context = {
        'course': course,
        'enrollments': enrollments,
        'total_enrolled_students':total_enrolled_students,
        'related_courses':related_courses,
    }
    
    return render(request, 'course_details.html', context)

@login_required(login_url='login')
def dashboard(request):
    user_enrollments = Enrollment.objects.filter(user=request.user, approved=True)
    return render(request, 'dashboard.html', {'user_enrollments': user_enrollments})




# views.py

@login_required(login_url='login')
def enroll(request, slug):
    course = Course.objects.get(slug=slug)

    if request.method == 'POST':
        form = EnrollmentForm(request.POST, request.FILES)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.user = request.user
            enrollment.course = course  # Set the course before saving the enrollment
            enrollment.course_price = course.price  # Set the course price
            enrollment.save()
            messages.success(request, 'Enrollment request submitted. Please wait for approval.')
            return redirect('course_details', slug=slug)
    else:
        form = EnrollmentForm()

    return render(request, 'enroll.html', {'course': course, 'form': form})


@login_required(login_url='login')
def course_playlist(request, course_slug):
    # Get the course using the provided slug
    course = get_object_or_404(Course, slug=course_slug)

    # Check if the user is enrolled in the specified course
    if Enrollment.objects.filter(user=request.user, course=course, approved=True).exists():
        # User is enrolled and approved, render the playlist page
        return render(request, 'playlist.html', {'course': course})
    else:
        # User is not enrolled or not approved, redirect them to another page or show an error message
        return redirect('courses')  # Redirect to the courses page or another appropriate page



def search_courses(request):
    search_key = request.GET.get('search', None)
    courses = Course.objects.filter(
        Q(title__icontains=search_key) |
        Q(price__icontains=search_key) |     
        Q(skill_level__icontains=search_key) |
        Q(language__icontains=search_key) |
        Q(category__title__icontains=search_key) |
        Q(author__name__icontains=search_key)
    )
    
    # Get the count of search results
    search_results_count = courses.count()

    context = {
        "courses": courses,
        "search_key": search_key,
        "search_results_count": search_results_count,
    }
    return render(request, 'search_result.html', context)




#wish list view
@login_required(login_url='login')
def add_to_wishlist(request, slug):
    course = get_object_or_404(Course, slug=slug)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)    
    wishlist.courses.add(course)
    messages.success(request, "You saved this Course in your account ")
    return redirect('wishlist')

@login_required(login_url='login')
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)        
    return render(request, 'wishlist.html', {'wishlist': wishlist})


@login_required(login_url='login')
def remove_from_wishlist(request, slug):
    course = get_object_or_404(Course, slug=slug)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist.remove_from_wishlist(course)   
    messages.error(request, "Deleted Saved Course") 
    return redirect('wishlist')
#wish list view 



def category_courses(request, category_slug):
    # Retrieve the category based on the provided slug
    category = get_object_or_404(Category, slug=category_slug)

    # Retrieve all courses associated with the category
    courses = Course.objects.filter(category=category)

    context = {
        "category": category,
        "courses": courses,
    }

    return render(request, 'category_courses.html', context)




def author_list(request):
    authors = Author.objects.annotate(total_courses=Count('course_author'))
    author_count = authors.count()

    context = {
        'authors': authors,
        'author_count': author_count,
    }

    return render(request, 'author_list.html', context)


def author_details(request, author_slug):
    author = get_object_or_404(Author, slug=author_slug)
    courses = author.course_author.all()
    context = {
        'author': author,
        'courses': courses,
        
    }

    return render(request, 'author_details.html', context)


def teams(request):
    teams = Team.objects.all()
    context = {
        "teams":teams
    }
    return render(request, 'about.html', context)

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Contact Form submitted successfully")
            return redirect('contact')
        else:
            messages.error(request, "Something wrong to send message")
    else:
        form = ContactForm()
    context = {
        "form": form,
    }  
    return render(request, 'contact.html', context)


def handler404(request, exception):
    return render(request, '404.html', status=404)

