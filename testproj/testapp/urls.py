from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('google', views.google),
    path('success', views.success),
    path('like/<int:id>', views.add_like),

    # localhost:8000/bbp
    # path('bbp/', views.bbp),
    # localhost:8000/shows
    path('shows/', views.google),
    # localhost:8000/shows/new
    path('shows/new', views.new),
    # localhost:8000/shows/create
    path('shows/create', views.create),
    # localhost:8000/shows/<show_id>/edit
    path('shows/<int:show_id>/edit', views.edit),
    # localhost:8000/shows/<show_id>/update
    path('shows/<int:show_id>/update', views.update),
    # localhost:8000/shows/<show_id>
    path('shows/<int:show_id>', views.show),
    # localhost:8000/shows/<show_id>/delete
    path('shows/<int:show_id>/delete', views.delete),
    # path for liked posts
    
]