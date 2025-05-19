from django.shortcuts import render, redirect  # For function-based views like savecomment, increaselikes
from django.contrib.auth.decorators import login_required  # If you use login_required on FBVs
from django.contrib import messages  # You're using messages in PostCreateView
from django.conf import settings  # For accessing MEDIA_URL in context
from django.urls import reverse_lazy  # You could use this in DeleteView for success_url
from .models import Post, Comment  # These models are used across all your views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from django.http import JsonResponse



#LoginRequiredMixin and CreateView are the base classes that PostCreateView inherits from.
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['postname', 'content', 'category', 'image']
    template_name = 'posts/create.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user

        # Print form data in terminal
        print("Form data (valid):", form.cleaned_data)

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form.save()
            return JsonResponse({'message': 'Post created successfully!'}, status=201)

        messages.success(self.request, "Your post has been created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Print form data and errors in terminal
        print("Form data (invalid):", form.data)
        print("Form errors:", form.errors)

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'errors': form.errors}, status=400)
        return super().form_invalid(form)


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/post-details.html'
    context_object_name = 'post'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['recent_posts'] = Post.objects.all().order_by('-id')
        context['media_url'] = settings.MEDIA_URL
        context['comments'] = Comment.objects.filter(post_id=self.object.id)
        context['total_comments'] = context['comments'].count()
        return context
    
def savecomment(request,id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        content = request.POST['message']
        Comment(post_id = post.id,user_id = request.user.id, content = content).save()
        return redirect("index")

def increaselikes(request,id):
    if request.method == 'POST':
        post = Post.objects.get(id=id)
        post.likes += 1
        post.save() 
    return redirect("index")

    
def deletecomment(request,id):
    comment = Comment.objects.get(id=id)
    postid = comment.post.id
    comment.delete()
    return post(request,postid)
    
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['postname', 'content', 'category']
    template_name = 'posts/postedit.html'
    success_url = '/profile/'

    def get_success_url(self):
        return f"/profile/{self.request.user.id}"
    
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'

    def get_success_url(self):
        return f"/profile/{self.request.user.id}"

