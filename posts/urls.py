from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('',views.post_list,name='post-list'),
    path('create-post/',views.create_post,name='create-post'),
    path('update-post/<int:postid>/',views.update_post,name='update-post'),
    path('delete-post/<int:postid>/',views.delete_post,name='delete-post'),
    path('search-post/',views.search_post,name='search-post'),
    path('topic-search/<slug:topic>',views.topic_search,name='topic-search'),
    path('toggle-like/<int:postid>/',views.toggle_like,name='toggle-like'),
    path('<int:postid>/',views.post_page,name='post-page'),
]

