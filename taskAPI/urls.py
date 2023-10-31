from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.All.as_view()),
    path('expensive/', views.Expensive.as_view()),
    path('largest/', views.Largest.as_view()),
    path('all-villa/', views.AllVilla.as_view()),
    path('all-projects/', views.AllProjects.as_view()),
    path('search', views.SearchProject.as_view()),
    path('search-param', views.SearchParamProject.as_view()),
    path('searchp', views.SearchPostProject.as_view()),
    path('searchwid/<w_id>/', views.SearchWid.as_view()),

]
