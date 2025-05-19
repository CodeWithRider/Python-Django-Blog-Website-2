from django.shortcuts import render
from django.conf import settings
from .models import Post
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET
from django.utils.decorators import method_decorator



def index(request):  # Renders the homepage and provides the template with dynamic content
    all_posts = Post.objects.all()       # All posts in reverse chronological order
    top_posts = Post.objects.all()     # All posts ordered by likes
    recent_posts = Post.objects.all()   # Same as all_posts, can customize later if needed

    # Debug logs
    print("Logged-in user:", request.user)
    print("All posts:", all_posts)
    print("Top posts by likes:", top_posts)
    print("Recent posts:", recent_posts)

    return render(request, "myapp/index.html", {
        'posts': all_posts,
        'top_posts': top_posts,
        'recent_posts': recent_posts,
        'user': request.user,
        'media_url': settings.MEDIA_URL
    })





def blog(request):
    return render(request,"myapp/blog.html",{
            'posts':Post.objects.filter(user_id=request.user.id).order_by("id").reverse(), #Psts created by currently logged-in user(request.user.id)
            'top_posts':Post.objects.all().order_by("-likes"),
            'recent_posts':Post.objects.all().order_by("-id"),
            'user':request.user,
            'media_url':settings.MEDIA_URL
        })

# from django.http import HttpResponse
# from django.views.decorators.http import require_GET

# @require_GET
# def load_new_content(request):
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         html = """
#         <h2>New Content Loaded via AJAX</h2>
#         <p>This content came from the same template logic, not a separate file.</p>
#         """
#         return HttpResponse(html)
#     return HttpResponse("Bad Request", status=400)
