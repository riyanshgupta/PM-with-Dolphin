from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http.response import JsonResponse, HttpResponseBadRequest
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User, Project, Task
from .forms import ProjectForm
@login_required(login_url="login")
def home(request):
    projects = Project.objects.all()
    proj = [] 
    for project in projects:
        if project.members.filter(id=(request.user.id)).exists():
            proj.append(project)
            
    return render(request, "home.html", context={"projects": proj})

@login_required(login_url="login")
def delete_project(request, pk):
    if request.method == "DELETE":
        project = get_object_or_404(Project, pk=pk)
        if project.host != request.user:
            messages.error(request, "Only the host can delete the project.")
            return redirect('home')
        else:
            project.delete()
            messages.info(request, "Project deleted successfully.")
            return redirect('home')
            return JsonResponse({"result": "Project deleted successfully"})
    return HttpResponseBadRequest("Method not allowed")

    # return JsonResponse(data={"result": "Method not allowed"})    
@login_required(login_url="login")
def update_project(request, pk):
    if request.method == "PATCH":
        project = get_object_or_404(Project, pk=pk)
        if project.host != request.user:
            messages.error(request, "Only the host can delete the project.")
            return redirect('home')
        else:
            name = request.POST.get("name")
            desc = request.POST.get("desc")
            icon = request.FILES.get("icon")
            deadline = request.POST.get("deadline")
            status = request.POST.get("status")
            if name and desc and deadline and status is None:
                messages.error(request, "Some parameters are missing")
            project.name = name
            project.desc = desc
            if icon:
                project.icon = icon
            project.deadline = deadline
            project.status = status
            project.save()
            messages.success(request, "Project updated successfully.")
            return redirect('home')
    return HttpResponseBadRequest("Method not allowed")

@login_required(login_url="login") # create project
def create_project(request):
    if request.method == "POST":
        if project.host != request.user:
            messages.error(request, "Only the host can delete the project.")
            return redirect('home')
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.host = request.user
            project.save()
            form.save_m2m()  # Save the many-to-many data for the form.
            messages.success(request, "Project created successfully.")
            return redirect('home')
        else:
            messages.error(request, "There was an error creating the project.")
            redirect('home')
    else:
        return HttpResponseBadRequest("Method not allowed")

def loginpage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password is None:
            messages.error(request, "Something is missing")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exists")
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password doesn't exits")
    return render(request, "login.html", context={"page": "login"})

def logoutUser(request):
    logout(request=request)
    return redirect('/login')



from .forms import SignUpForm

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, "Signup successful!")
            return redirect('home')
        else:
            messages.error(request, "There was an error in the signup form.")
            return redirect("signup")
    else:
        return render(request, "login.html", context={"page": "signup"})
