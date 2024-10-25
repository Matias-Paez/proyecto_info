from django.urls import path
import apps.post.views as views  #importo todas las vistas que se encuentran en apps/post/views

app_name = 'post' #defino el nombre de la aplicacion 

urlpatterns = [
    path('posts/create', views.PostCreateView.as_view(),name= 'post_create'), #URL :Para crear post
    path('posts/<slug:slug>', views.PostDetailView.as_view(), name = 'post_detail'), #URL :Para Detalle post
    path('posts/<slug:slug>/update', views.PostUpdateView.as_view(), name = 'post_update'), #URL :Para Update Post
    path('posts/<slug:slug>/delete', views.PostDeleteView.as_view(), name= 'post_delete'),#URL :Para Delete Post
    path('posts/', views.PostListView.as_view(), name ='post_list'), # URL :Para listar los post
    path('posts/<slug:slug>/comments/create/', views.CommentCreateView.as_view(), name= 'comment_create'),#URL :Para Crear comentario
    path('comments/<uuid:pk>/update', views.CommentUpdateView.as_view(), name= 'comment_update'),#URL :Para Crear comentario
    path('comments/<uuid:pk>/delete', views.CommentDeleteView.as_view(), name= 'comment_delete'),#URL :Para Crear comentario
    
    path('category/', views.CategoryListView.as_view(), name = 'category_list'), # URL para listar las categorias
    path('category/create', views.CategoryCreateView.as_view(), name = 'category_create'), # URL para crear una categorias
    path('category/update/<uuid:pk>/', views.CategoryUpdateView.as_view(), name = 'category_update'), # URL para actualizar una categorias -- le paso el id de la categoria
    path('category/delete/<uuid:pk>/', views.CategoryDeleteView.as_view(), name = 'category_delete'), # URL para actualizar una categorias -- le paso el id de la categoria
]
