from django.urls import path
from .views import *

urlpatterns = [
    path('api/vendors/', VendorListCreate.as_view()),
    path('api/vendors/<int:pk>/', VendorRetrieveUpdateDestroy.as_view()),
    path('api/purchase_orders/', PurchaseOrderListCreate.as_view(), name='purchase-order-list-create'),
    path('api/purchase_orders/<str:pk>/', PurchaseOrderRetrieveUpdateDelete.as_view(), name='purchase-order-retrieve-update-delete'),
    path('api/vendors/<int:pk>/performance/', VendorPerformance.as_view()),
    path('api/purchase_orders/<str:pk>/acknowledge/', AcknowledgePurchaseOrder.as_view(), name='acknowledge-purchase-order'),

]