from django.urls import include, path
from rest_framework.routers import DefaultRouter
from categories.views import CategoryViewSet, SubCategoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'sub_categories', SubCategoryViewSet, basename='sub_category')

urlpatterns = [
    path('', include(router.urls)),
]