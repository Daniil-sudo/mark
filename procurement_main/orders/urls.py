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
    path("cart/add/", AddToCart.as_view()),
    path("cart/remove/<int:item_id>/", RemoveFromCart.as_view()),
    path("contact/add/", ContactCreate.as_view()),
    path("confirm/", ConfirmOrder.as_view()),
    path("history/", OrderHistory.as_view()),
    path("api/schema/", SpectacularAPIView.as_view()),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    #path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
]