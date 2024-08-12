from django.urls import path
from panel import views

app_name = 'panel'
urlpatterns = [
    path('', views.PanelView.as_view(), name='panel_home'),
    path('users', views.UserListView.as_view(), name='user_list'),
    path('users/<str:level>', views.UserListView.as_view(), name='user_list'),
    path('admin', views.AdminListView.as_view(), name='admin_list'),
    path('posts', views.PostListView.as_view(), name='post_lists'),
    path('new_post', views.NewPostView.as_view(), name='new_post'),
    path('update_post/<int:pk>', views.update_post, name='update_post'),
    path('delete_post/<int:post_id>', views.delete_post, name='delete_post'),
    path('edite_user/<int:pk>', views.UserUpdateView.as_view(), name='edite_user'),
    path('profile/<int:pk>', views.ProfileView.as_view(), name='profile'),
    path('profile_update/<int:pk>', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('new_category/', views.CategoryCreateView.as_view(), name='new_category'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('delete_category/<int:category_id>', views.delete_category, name='category_delete'),
    path('update_category/<int:pk>', views.CategoryUpdateView.as_view(), name='category_update'),
]
