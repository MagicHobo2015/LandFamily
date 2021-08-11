from django.shortcuts import render
from django.views.generic import DetailView, CreateView, ListView, DeleteView, ArchiveIndexView, UpdateView
from django.views.generic.dates import MonthArchiveView
from blog.models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

# Create your views here.


def home(request):
    post_object = Post.objects.last()
    id = Post.objects.last().id
    context = {'post': post_object, 'title': 'Home', 'comments': Comment.objects.filter(post=id)}
    return render(request, 'blog/home.html', context)


def contact(request):
    context = {'title': 'Contact Us'}
    return render(request, 'blog/contact.html', context)


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog-home')

    # TODO: this should be re-written to query the group the user is in that way it can be an 'editor' group instead
    def test_func(self):
        user = self.request.user.username
        if user == 'Christina':
            return True
        return False


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        primary_key = self.kwargs['pk']
        form.instance.post = Post.objects.filter(pk=primary_key).first()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('Post-Detail', kwargs={'pk': self.object.post.pk})


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all()


class PostArchiveIndexView(ArchiveIndexView):
    model = Post
    date_field = 'date_posted'


class PostMonthArchiveView(MonthArchiveView):
    queryset = Post.objects.all()
    date_field = "date_posted"
    context_object_name = 'latest'
    template_name = 'blog/post_archive.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=context['post'])
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/post_update_form.html'

    def test_func(self):
        comment = self.get_object()
        user_id = self.request.user.id
        return comment.author.id == user_id

    def get_success_url(self):
        post_id = self.object.post.pk
        return reverse_lazy('Post-Detail', kwargs={'pk': post_id})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/post_confirm_delete.html'

    def test_func(self):
        the_user = self.request.user.id
        the_author = self.get_object()
        return self.request.user.is_staff or the_user == the_author.author.id

    def get_success_url(self):
        post_pk = self.object.post.pk
        return reverse_lazy('Post-Detail', kwargs={'pk': post_pk})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self, **kwargs):
        post_pk = self.object.pk
        return reverse_lazy('Post-Detail', kwargs={'pk': post_pk})
