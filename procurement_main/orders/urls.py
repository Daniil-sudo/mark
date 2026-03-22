from django.urls import path
from .views import *

urlpatterns = [
    path("cart/add/", AddToCart.as_view()),
    path("cart/remove/<int:item_id>/", RemoveFromCart.as_view()),
    path("contact/add/", ContactCreate.as_view()),
    path("confirm/", ConfirmOrder.as_view()),
    path("history/", OrderHistory.as_view()),
]