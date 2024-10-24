from django.urls import path
import apps.post.views as views  #importo todas las vistas que se encuentran en apps/post/views

app_name = 'post' #defino el nombre de la aplicacion 

urlpatterns = [
    path('posts/create', views.PostCreateView.as_view(),name= 'post_create'), #URL :Para crear post
    path('posts/<slug:slug>', views.PostDetailView.as_view(), name = 'post_detail'), #URL :Para Detalle post
    path('posts/<slug:slug>/update', views.PostUpdateView.as_view(), name = 'post_update'), #URL :Para Update Post
    path('posts/<slug:slug>/delete', views.PostDeleteView.as_view(), name= 'post_delete'),#URL :Para Delete Post
    path('posts/', views.PostListView.as_view(), name ='post_list'), # URL :Para listar los post
]
