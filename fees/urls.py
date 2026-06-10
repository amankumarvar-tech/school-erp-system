from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import FeeStructureViewSet, FeePaymentViewSet, ExpenseViewSet

router = DefaultRouter()
router.register('fee-structures', FeeStructureViewSet)
router.register('fee-payments', FeePaymentViewSet)
router.register('expenses', ExpenseViewSet)
urlpatterns = [path('', include(router.urls))]
