from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from accounts.forms import CustomUserChangeForm
from accounts.models import CustomUser
from accounts.forms import CustomUserChangeForm
from posts.forms import PostForm
from posts.models import Post
from category.models import Category
from category.forms import CategoryForm
from publication.models import Publication
from publication.forms import PublicationForm


class PanelView(generic.ListView):
    model = CustomUser
    template_name = 'panel/index_panel.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context_object_name = super().get_context_data(**kwargs)
        user_data = CustomUser.objects.all()
        context_object_name['phdCount'] = user_data.filter(student_level="PHD", status='current',
                                                           professor_verification=True).count()
        context_object_name['masterCount'] = user_data.filter(student_level="Master", status='current',
                                                              professor_verification=True).count()
        context_object_name['allStudent'] = user_data.filter(student_level__in=['Bachelors', 'Master', 'PHD'],
                                                             status__in=['current', 'Alumni'],
                                                             professor_verification=True).count()
        context_object_name['alumniStudent'] = user_data.filter(professor_verification=True, status='Alumni').count()
        context_object_name['newStudents'] = user_data.filter(professor_verification=False)
        context_object_name['admins'] = user_data.filter(professor_verification=True,
                                                         status__in=['current', 'Alumni'],
                                                         student_level__in=['Bachelors', 'Master', 'PHD'],
                                                         user_role='admin')
        return context_object_name


class UserListView(generic.ListView):
    def get(self, request, *args, **kwargs):
        level = kwargs.get('level')
        users = CustomUser.objects.filter(professor_verification=True, student_level__in=['Bachelors', 'Master', 'PHD'],
                                          status__in=['current', 'Alumni'])
        if level is not None:
            if level != 'Alumni':
                users = users.filter(student_level=level, status='current')
            else:
                users = users.filter(status=level)
        return render(request, 'panel/user_list.html', {'users': users})


class UserUpdateView(generic.UpdateView):
    model = CustomUser
    fields = ['username', 'first_name', 'last_name', 'email', 'status', 'student_level', 'user_role',
              'professor_verification']
    template_name = 'panel/edite_user.html'
    context_object_name = 'user'
    success_url = reverse_lazy('panel:panel_home')


def delete_user(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    user.delete()
    return redirect('panel:user_list')


def verify_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.professor_verification = True
    user.save()
    return redirect('panel:edite_user', user.id)


class AdminListView(generic.ListView):
    model = CustomUser
    template_name = 'panel/admin_list.html'
    context_object_name = 'admins'

    def get_queryset(self):
        admins = CustomUser.objects.filter(professor_verification=True, status__in=['current', 'Alumni'],
                                           student_level__in=['Bachelors', 'Master', 'PHD'],
                                           user_role='admin')
        return admins


def make_admin(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    user.user_role = 'admin'
    user.save()
    return redirect('panel:admin_list')


def un_role(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    user.user_role = 'student'
    user.save()
    return redirect('panel:admin_list')


class PostListView(generic.ListView):
    model = Post
    template_name = 'panel/posts.html'
    context_object_name = 'posts'


class NewPostView(generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'panel/new_post.html'
    success_url = reverse_lazy('panel:post_lists')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def update_post(request, pk):
    post = Post.objects.filter(pk=pk).first()
    category = Category.objects.all()
    form = PostForm(request.POST or None, instance=post)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('panel:post_lists')
    else:
        context = {'form': form, 'category': category}
        return render(request, template_name='panel/new_post.html', context=context)


def delete_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.delete()
    return redirect('panel:post_lists')


class ProfileView(generic.TemplateView):
    template_name = 'panel/profile.html'


class ProfileUpdateView(generic.UpdateView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = CustomUser.objects.get(pk=user_id)
        form = CustomUserChangeForm(instance=user)
        context = {'form': form}
        return render(request, template_name='panel/profile_update.html', context=context)

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = CustomUser.objects.get(pk=user_id)
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('panel:profile')


class CategoryCreateView(generic.CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'panel/new_category.html'
    success_url = reverse_lazy('panel:category_list')


class CategoryListView(generic.ListView):
    model = Category
    template_name = 'panel/categories.html'
    context_object_name = 'cats'


def delete_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    category.delete()
    return redirect('panel:category_list')


class CategoryUpdateView(generic.UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'panel/new_category.html'
    context_object_name = 'cat'
    success_url = reverse_lazy('panel:category_list')


class PublicationListView(generic.ListView):
    model = Publication
    template_name = 'panel/publications.html'
    context_object_name = 'pubs'


def delete_publication(request, pub_id):
    pub = Publication.objects.get(pk=pub_id)
    pub.delete()
    return redirect('panel:publication_list')


class PublicationCreateView(generic.CreateView):
    model = Publication
    form_class = PublicationForm
    template_name = 'panel/new_publication.html'
    success_url = reverse_lazy('panel:publication_list')


class PublicationUpdateView(generic.UpdateView):
    model = Publication
    form_class = PublicationForm
    template_name = 'panel/new_publication.html'
    context_object_name = 'pub'
    success_url = reverse_lazy('panel:publication_list')
