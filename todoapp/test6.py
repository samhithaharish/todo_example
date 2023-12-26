api_key = "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"

@login_required
def currenttodos(request):
    extracted_todolist = None  # Initialize the variable to store extracted data

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

    else:
        form = UploadFileForm()

    return render(request, 'todoapp/currenttodos.html', {'form': form, 'extracted_todolist': extracted_todolist})







def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todoapp/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todoapp/createtodo.html', {'form':TodoForm(), 'error':'Bad data passed in. Try again.'})
        




        {% extends "todoapp/base.html" %}

{% block content %}
    <div class="row justify-content-center mt-5">
        <div class="col-md-5">
            <h2>New Todo</h2>
        </div>
    </div>
    <div class="row justify-content-center mt-5">
        <div class="col-md-5">
            {% if error %}
                <div class="alert alert-danger" role="alert">
                    {{ error }}
                </div>
            {% endif %}
            <form method="POST">
                {% csrf_token %}
                <div class="form-group">
                    <label for="title">Title</label>
                    <input type="text" name="title" class="form-control" id="title" required>
                </div>
                <div class="form-group">
                    <label for="memo">Memo</label>
                    <textarea name="memo" class="form-control" id="memo" ></textarea>
                </div>
                <div class="form-group form-check">
                    <input type="checkbox" name="important" class="form-check-input" id="important">
                    <label class="form-check-label" for="important">Important</label>
                </div>
                <button type="submit" class="btn btn-primary">Save</button>
            </form>
        </div>
    </div>
{% endblock %} 








api_key = "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"
@login_required
def currenttodos(request):
    extracted_todolist = None  # Initialize the variable to store extracted data

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

    else:
        form = UploadFileForm()

    return render(request, 'todoapp/currenttodos.html', {'form': form, 'extracted_todolist': extracted_todolist})



@login_required
def currenttodos(request):
    extracted_todolist = None

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            text_file = request.FILES['file']
            text = text_file.read().decode('utf-8')
            prompt = f'''Given a text containing a list of tasks and associated details, extract the TODO list information and format it as a JSON output with the following keys:

activity_name: The name of the activity.
activity_description: A brief description of the activity.
activity_time: The time at which the activity is scheduled.
Ensure that the extracted JSON output captures each task along with its description and scheduled time.

:\n{text}'''

            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=150,
                api_key=api_key
            )

            extracted_todolist = response.choices[0].text.strip()

            # Save the new todo item
            try:
                todo_data = json.loads(extracted_todolist)
                newtodo = Todo.objects.create(
                    user=request.user,
                    activity_name=todo_data.get('activity_name', 'No Name'),
                    activity_description=todo_data.get('activity_description', 'No Description'),
                    activity_time=todo_data.get('activity_time', None)
                )
                newtodo.save()
            except json.JSONDecodeError:
                return HttpResponse('Error decoding JSON data from OpenAI API response.', status=500)

    else:
        form = UploadFileForm()

    # Retrieve manually created todos and display them along with extracted tasks
    manual_todos = Todo.objects.filter(user=request.user, extracted=False)
    all_todos = Todo.objects.filter(user=request.user)

    return render(request, 'todoapp/currenttodos.html', {'form': form, 'extracted_todolist': extracted_todolist, 'manual_todos': manual_todos, 'all_todos': all_todos})



rendering function
                        title = activity_name'''=json_data.get('activity_name', ''),'''
                        memo = activity_description '''=json_data.get('activity_description', ''),'''
                        datacomppleted = activity_time '''=json_data.get('activity_time', '')'''