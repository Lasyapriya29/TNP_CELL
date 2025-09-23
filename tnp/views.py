# Merged changes to the `placements` view to include filtering of placement details based on company name if provided in POST requests.

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Studentdetails, Placements
# Create your views here.
def index(request):
    stu_details = Studentdetails.objects.all()
    return render(request, 'index.html', {'stu_details': stu_details})

def about(request):
    return render(request, 'about.html')

def training(request):
    return render(request, 'training.html')

def placements(request):
    # Fetch all placement and student details
    place_det = Placements.objects.all()
    stu_details = Studentdetails.objects.all()

    # Check if the request method is POST
    if request.method == 'POST':
        # Get the company name from the POST request
        comp = request.POST.get('comp')

        # If a company name is provided, filter placement details for that company
        if comp:
            filtered_place_det = place_det.filter(company_name__icontains=comp)  # Assuming 'company_name' is a field in Placements model
        else:
            filtered_place_det = place_det  # If no company name is provided, use all placement details

        # Render the template with filtered data
        return render(request, 'placements.html', {
            'place_det': filtered_place_det,
            'stu_details': stu_details,
            'comp': comp
        })

    # Render the template with all data for GET requests
    return render(request, 'placements.html', {
        'place_det': place_det,
        'stu_details': stu_details
    })
    
def contact(request):
    return render(request, 'contact.html')

def register(request):
    if request.method == 'POST':
        roll_number = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email exists')
                return redirect('register')
            elif Studentdetails.objects.filter(roll_number=roll_number).exists() == False:
                messages.info(request, 'Your details are not found')
                return redirect('register')
            else:
                user = User.objects.create_user(username=roll_number, email=email, password=password)
                user.save();
                return redirect('login')
        else:
            messages.info(request, 'Passwords not same')
            return redirect('register')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        roll_number = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(password=password,username=roll_number)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Info Invalid')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')