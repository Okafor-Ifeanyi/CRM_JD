from django.urls import path
from . import views

app_name = "leads"

urlpatterns = [
    path('', views.leads, name="leads"),
    path('<int:pk>/', views.lead_details, name="lead_details"),
    path('create/', views.lead_create, name="lead_create"),
    path('<int:pk>/update/', views.lead_update , name="lead_update"),
    path('<int:pk>/delete/', views.lead_delete , name="lead_delete"),
]