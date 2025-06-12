from django.shortcuts import render, redirect
from .models import Post
from django.contrib import messages

# Create your views here.
def index(request):
    posts = Post.objects.all()
    return render(request,'index.html',{'posts':posts})

def post(request,x):
    posts = Post.objects.get(id=x)
    return render(request,'post.html',{'posts':posts})

def addpost(request):
    if request.method=='POST':
        topic=request.POST['topic']
        desc=request.POST['desc']
        created_at=request.POST['created_at']
        data=Post(titles=topic,body=desc,created_at=created_at)
        data.save()
        messages.info(request, 'Post added successfully!')
        return redirect('addpost')
    else:
        return render(request,'addpost.html')