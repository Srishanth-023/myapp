from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("", views.index, name = "index"),
    path("post/<int:post_id>", views.detail, name = "detail"),
    # path("post/<str:post_id>", views.detail, name = "detail"),
    path("new_changed_url", views.new_url_view, name = "new_url"),
    path("old_url", views.old_url_redirect, name = "old_url"),
]