from django.urls import path
from rest_framework import permissions

from .views import *
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Shop API",
      default_version='v1',
      description="API для корзины и заказов",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("cart/add/", AddToCart.as_view(), name="add-to-cart"),
    path("cart/remove/<int:item_id>/", RemoveFromCart.as_view(), name="remove-from-cart"),

    path("contact/create/", ContactCreate.as_view(), name="create-contact"),

    path("confirm/", ConfirmOrder.as_view(), name="confirm-order"),

    path("history/", OrderHistory.as_view(), name="order-history"),
]