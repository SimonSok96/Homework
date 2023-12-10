from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .forms import EmailPostForm, CommentForm
from .models import Post, Comment

class PostListView(ListView):
    """Альтернативне подання списку постів"""
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/list.html'
    
    
def post_share(request, post_id):
    # Отримати пост за id
    post = get_object_or_404(Post, id=post_id)
    sent = False
    if request.method == 'POST':
        # Форма передана на обробку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля форми успішно пройшли валідацію
            cd = form.cleaned_data
            # відправити електронного листа
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd["name"]} recommends you read {post.title}'
            message = f'Read {post.title} at {post_url}\n\n' \
                      f'{cd["name"]}\'s comments: {cd["comments"]}'
            send_mail(subject, message, 'your_account@gmail.com', [cd['to']])
            sent = True              
    else:
        form = EmailPostForm()
    return render(request, 'blog/share.html', {'post': post, 'form': form, 'sent': sent})
    
    
# def post_list(request):
#     post_list = Post.published.all()
#     # Посторінкове розбиття з 3 постами на сторінку
#     paginator = Paginator(post_list, 3)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = paginator.page(page_number)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     return render(request, 'blog/list.html', {'posts': posts})


# def post_detail(request, id):
#     try:
#         post = Post.objects.get(id=id)
#     except Post.DoesNotExist:
#         raise Http404('No Post found')
#
#     return render(request, 'blog/detail.html', {'post': post})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post)
     # Список активних коментарів до цього посту
    comments = post.comments.filter(active=True)
    # Форма для коментування користувачами
    form = CommentForm()
    return render(request, "blog/detail.html", {"post": post, 'comments': comments, 'form': form})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment = None
    # Комментар було відправлено
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Створити об'єкт Comment, не зберігаючи його в базі даних
        comment = form.save(commit=False)
        # Призначити пост коментарю
        comment.post = post
        # Зберегти коментар в БД
        comment.save()
    return render(
        request,
        "blog/comment.html",
        context={
            "post": post,
            "form": form,
            "comment": comment,
        },
    )