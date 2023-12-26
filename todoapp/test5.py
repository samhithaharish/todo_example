api_key = "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"

@login_required
def currenttodos(request):
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

            # Write the extracted data to a JSON file
            with open('output.json', 'w') as json_file:
                json.dump(extracted_todolist, json_file, indent=4)

            return HttpResponse("Todo list extracted successfully and saved to output.json.")
    else:
        form = UploadFileForm()

    return render(request, 'todoapp/currenttodos.html', {'form': form})
    #return render(request, 'currenttodos.html', {'form':form,'json_data': extracted_todolist}) 





{% extends "todoapp/base.html" %}

{% block content %}
    <div class="row justify-content-center mt-5">
        <div class="col-md-10">
            {% if todos %}
                 <h1>{{ todos.count }} Current Todo{{ todos.count|pluralize }}</h1>
            {% else %}
                           <h1>Current Todos</h1>
            {% endif %}
        </div>
    </div>
    <div class="row justify-content-center mt-5">
        <div class="col-md-10">
        {% if todos %}
            <div class="list-group">
                {% for todo in todos %}
                    <a href="{% url 'viewtodo' todo.id %}" class="list-group-item list-group-item-action{% if todo.important %} list-group-item-danger{% endif %}"><b>{{ todo.title }}</b>{% if todo.memo %} - {{ todo.memo|truncatechars:30 }}{% endif %}</a>
                {% endfor %}
            </div>
        {% else %}
            <div class="text-center">
                <h2>Looks like you don't have any todos! Nice work.</h2>
            <br>
            <a role="button" class="btn btn-primary" href="{% url 'createtodo' %}">New Todo</a>
            </div>
        {% endif %}
        </div>
    </div>
<!-- yourapp/templates/upload_file.html -->
{% if extracted_todolist %}
    <p>Extracted Todo List:</p>
    <pre>{{ extracted_todolist }}</pre>
{% endif %}

<!-- Your form rendering code goes here -->





<form action="{% url 'currenttodos' %}" method="post" enctype="multipart/form-data">
        {% csrf_token %}     
        <input type="file" name="file" required>
            <button type="submit">Upload</button>
        </form>


       

    

{% endblock %}

