from django.urls import path
from .admin import task_manager_admin_site

urlpatterns = [
    path("admin/", task_manager_admin_site.urls),
]
