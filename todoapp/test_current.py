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





createtodo


def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todoapp/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            print("im here")
            '''return redirect('currenttodos',newtodo.id)'''
        except ValueError:
            return render(request, 'todoapp/createtodo.html', {'form':TodoForm(), 'error':'Bad data passed in. Try again.'})
        except Exception as e:
            # Handle other exceptions and return an appropriate response
            return HttpResponseBadRequest(f"Error: {str(e)}")




