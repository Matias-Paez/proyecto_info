from django.urls import path
import apps.post.views as views  #importo todas las vistas que se encuentran en apps/post/views

urlpatterns = [
    path('posts/<slug:slug>', views.PostDetailView.as_view(), name = 'post_detail'),
    path('posts/<slug:slug>/update', views.PostUpdateView.as_view(), name = 'post_update'),
]
