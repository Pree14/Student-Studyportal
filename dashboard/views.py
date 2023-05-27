from django.shortcuts import render, redirect
from django. contrib import messages
from . forms import *
from django.views import generic
from youtubesearchpython import VideosSearch
import requests 
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')

@login_required
def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
        messages.success(request,f"Notes added from {request.user.username} successfully.")
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user) # when the user name is given it will return all the notes
    context = {'notes':notes,'form':form}
    return render(request,'dashboard/notes.html',context)

@login_required
def delete_note(request,pk=None):     # to save on db
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

class NotesDetailView(generic.DetailView):
    model = Notes    

@login_required
def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid(): # to check all the info is valid or not
            try:
                finished == request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False  # is thier is any struggle in finished is remain false
            homeworks = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished,
            )
            homeworks.save()
            messages.success(request ,f'Homework added from {request.user.username}!!!')
    else:
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {
        'homeworks':homework,
        'homeworks_done':homework_done,
        'form':form,
        }
    return render(request, 'dashboard/homework.html',context)

@login_required
def update_homework(request,pk=None):  # to save the input on db
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')

@login_required
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")

def youtube(request):  # if u hit the search button
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input':text,
                'title':i['title'],  # i means this is the result record                
                'duration':i['duration'],                
                'thumbnail':i['thumbnails'][0]['url'],  # this is the way to get thumbnail              
                'channel':i['channel']['name'],                
                'link':i['link'],                
                'views':i['viewCount']['short'],                
                'published':i['publishedTime']                
            }
            desc = '' # some video has a description but some not so outside dict
            if i['descriptionSnippet']: #more than one use for for desc
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list
            }
        return render (request,'dashboard/youtube.html',context)
    else:
        form = DashboardForm()
    context = {'form':form}
    return render(request,"dashboard/youtube.html",context)

@login_required
def todo(request):
    if request.method == 'POST':  # if req is post then create a todo form 
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == "on":
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(    # is an object
                user = request.user,
                title = request.POST["title"],
                is_finished = finished
            ) # after passing we going to save
            todos.save()
            messages.success(request,f"Todo added from {request.user.username}!!")
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'todos':todo,
        'form':form,
        'todos_done':todos_done
        }
    return render(request,'dashboard/todo.html',context)

@login_required
def update_todo(request,pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:  # check if the row is finished or not
        todo.is_finished = False #then assign todo is equal to false
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')

@login_required
def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")

def books(request):  # if u hit the search button
    if request.method == 'POST':
        form = DashboardForm(request.POST) # to call dashboard from on forms section
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url) # to get the url is not an builtin function so import explicity
        answer = r.json() # we get the result in json object
        result_list = []
        for i in range(10):
            result_dict = {
                'title':answer['items'][i]['volumeInfo']['title'],  # inside items ith object and volume info and get the title               
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'), 
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink')
            }
            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list
            }
        return render (request,'dashboard/books.html',context) # render to books.html file
    else:
        form = DashboardForm()
    context = {'form':form}
    return render(request,"dashboard/books.html",context)

def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST) # to call dashboard from on forms section
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r = requests.get(url) # to get the url is not an builtin function so import explicity
        answer = r.json() # we get the result in json object
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']  # more defs so geting the first def
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            #synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,  # there is no multiple data so we pass directly so no need to add inside the list
                'example':example,
                #'synonyms':synonyms
            }
        except:
            context = {
                'form':form,
                'input':"",
            }
        return render(request,'dashboard/dictionary.html',context)
    else:
        form = DashboardForm()
        context = {'form':form}
    return render(request,'dashboard/dictionary.html',context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Account created for {username}!!!")
            return redirect("login")
    else:
        form = UserRegistrationForm()
    context = {
        'form':form
    }
    return render(request,'dashboard/register.html',context)

@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished=False,user=request.user)
    todos = Todo.objects.filter(is_finished=False,user=request.user)
    if len(homeworks) ==0:
        homework_done = True
    else:
        homework_done = False 
    if len(todos) ==0:
        todo_done = True
    else:
        todo_done = False 
    context = {
        'homeworks' : homeworks,
        'todos' : todos,
        'homework_done' : homework_done,
        'todo_done' : todo_done
    }
    return render (request,'dashboard/profile.html',context)











