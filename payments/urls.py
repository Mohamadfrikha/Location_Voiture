from django.urls import path
from . import views
app_name="payments"
urlpatterns = [
    path('pay/<int:loc_id>/', views.create_checkout_session, name='stripe-pay'),
    path('stripe-success/<int:id_loc>/', views.stripe_success, name='stripe-success'),
    path('stripe-cancel/', views.stripe_cancel, name='stripe-cancel'),
]