from django.urls import path
from .views import *

urlpatterns = [
    path('category/', CategoryListView.as_view()),
    path('category/create', CategoryCreateView.as_view()),
    path('category/<int:pk>', CategoryRetrieveView.as_view()),
    path('category/<int:pk>/update', CategoryUpdateView.as_view()),
    path('category/<int:pk>/delete', CategoryDestroyView.as_view()),
    path('subcategory/', SubCategoryListView.as_view()),
    path('subcategory/create', SubCategoryCreateView.as_view()),
    path('subcategory/<int:pk>', SubCategoryRetrieveView.as_view()),
    path('subcategory/<int:pk>/update', SubCategoryUpdateView.as_view()),
    path('subcategory/<int:pk>/delete', SubCategoryDestroyView.as_view()),
]
