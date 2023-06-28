from django.urls import include, path
from rest_framework.routers import DefaultRouter
from categories.views import CategoryViewSet, SaleOutCategories

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'categories_sale_out', SaleOutCategories, basename='category_sale_out')

urlpatterns = [
    path('', include(router.urls)),
]