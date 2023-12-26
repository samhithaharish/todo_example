from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import openai
import json
from django.http import HttpResponse
from django.http import HttpResponseBadRequest



# Create your views here.
def home(request):
    return render(request, 'todoapp/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todoapp/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todoapp/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'todoapp/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todoapp/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todoapp/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')
      

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required


@login_required
def createtodo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                newtodo = form.save(commit=False)
                newtodo.user = request.user
                newtodo.save()
                messages.success(request, 'Todo created successfully.')
                return redirect('currenttodos', newtodo.id)
            except Exception as e:
                messages.error(request, f'Error creating todo: {e}')
        else:
            messages.error(request, 'Invalid form data. Please correct the errors.')
    
    else:
        form = TodoForm()

    return render(request, 'todoapp/createtodo.html', {'form': form})






from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm, TodoForm
from .models import Todo
import openai
import json
from django.http import HttpResponse

api_key = "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"
# Replace the existing 'currenttodos' view with the modified version below
def process_and_save_extracted_data(user, extracted_todolist):
    try:
        json_data = json.loads(extracted_todolist)
        new_todo = Todo.objects.create(
            user=user,
            activity_name=json_data.get('activity_name', ''),
            activity_description=json_data.get('activity_description', ''),
            activity_time=json_data.get('activity_time', '')
        )
        new_todo.save()
    except json.JSONDecodeError:
        # Handle JSON decoding error
        pass


@login_required
def currenttodos(request):
    extracted_todolist = None  # Initialize the variable to store extracted data
    todos = Todo.objects.filter(user=request.user).order_by('-created')

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            text_file = request.FILES['file']

            # Read the text from the input file
            text = text_file.read().decode('utf-8')

            # Define a prompt for the OpenAI API to understand and extract relevant information
            prompt = f'''Given a text containing a list of tasks and associated details, extract the TODO list information and format it as a JSON output with the following keys:

            activity_name: The name of the activity.
            activity_description: A brief description of the activity.
            activity_time: The time at which the activity is scheduled.
            Ensure that the extracted JSON output captures each task along with its description and scheduled time.

            :\n{text}'''

            # Call the OpenAI API to extract the todo list
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=150,
                api_key=api_key
            )

            # Extract the extracted todo list from the API response
            extracted_todolist = response.choices[0].text.strip()

            # Create a new todo based on the extracted data
            # Modify this part based on the actual structure of the extracted data
            try:
                json_data = json.loads(extracted_todolist)
                if isinstance(json_data,dict):
                    activity_name = json_data.get('activity_name', '')
                    if activity_name:
            # Extract other fields from JSON data
                        activity_description = json_data.get('activity_description', '')
                        activity_time = json_data.get('activity_time', '')
                    
                    new_todo = Todo.objects.create(
                        user=request.user,
                        activity_name=json_data.get('activity_name', ''),
                        activity_description =json_data.get('activity_description', ''),
                        activity_time =json_data.get('activity_time', '')
                )
                    new_todo.save()
                else:
                    pass
            except json.JSONDecodeError:
                # Handle JSON decoding error
                pass

    else:
        form = UploadFileForm()

    return render(request, 'todoapp/currenttodos.html', {'form': form, 'extracted_todolist': extracted_todolist, 'todos': todos})












@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todoapp/completedtodos.html', {'todos':todos})


@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todoapp/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todoapp/viewtodo.html', {'todo':todo, 'form':form, 'error':'Bad info'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
    
   
# yourapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UploadFileForm
from .models import Task
import openai
import json

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            text_file = request.FILES['file']
            openai.api_key = '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'  # Replace with your actual OpenAI API key
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=text_file.read().decode('utf-8'),
                max_tokens=100
            )
            json_data = json.loads(response['choices'][0]['text'])
            Task.objects.create(title=json_data.get('title', 'No Title'), description=json_data.get('description', 'No Description'))
            messages.success(request, 'File uploaded successfully!')
            return redirect('dashboard')
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form})
# yourapp/views.py




