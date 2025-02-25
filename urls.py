from django.contrib import admin
from django.urls import path
from .views import (
    welcome,
    CustomLoginView,
    owner_dashboard,
    user_dashboard,
    accept_order,
    delete_order,
    add_menu_item,
    logout_view,
    toggle_availability,
    earnings_report,
    view_cart,
    confirm_order,
    add_to_cart,
    update_cart_item,
    remove_from_cart,
    cancel_order,
    owner_mark_prepared,
    order_confirmed,
    mark_prepared,
    mark_delivered,
    order_confirmation_page
)




from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path('user_dashboard/', user_dashboard, name='user_dashboard'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('update_cart_item/<int:cart_item_id>/', update_cart_item, name='update_cart_item'),
    path('confirm_order/', confirm_order, name='confirm_order'),
    path('cancel_order/', cancel_order, name='cancel_order'),
    path('', welcome, name='welcome'),
    path('cancel_order/', cancel_order, name='cancel_order'),
   # path('confirm_order/', confirm_order, name='confirm_order'),
    path('order_prepared/<int:order_id>/', owner_mark_prepared, name='mark_order_prepared'),
    path('user_dashboard/', user_dashboard, name='user_dashboard'),
    path('view_cart/', view_cart, name='view_cart'),
    #path('confirm_order/', confirm_order, name='confirm_order'),
    #path('cancel_order/<int:order_id>/', cancel_order, name='cancel_order'),
    path('remove_from_cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/confirm/', confirm_order, name='confirm_order'),
    path('cart/confirm/<int:order_id>/', order_confirmation_page, name='order_confirmed'),
    #path('order/placed/', order_placed, name='order_placed'),
    path('order/<int:order_id>/mark_prepared/', mark_prepared, name='mark_prepared'),
    path('order/<int:order_id>/mark_delivered/', mark_delivered, name='mark_delivered'),
    path('order_confirmed/', order_confirmed, name='order_confirmed_default'),
 #path('owner/mark_prepared/<int:order_id>/', owner_mark_prepared, name='owner_mark_prepared'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('owner_dashboard/', owner_dashboard, name='owner_dashboard'),
    path('user_dashboard/', user_dashboard, name='user_dashboard'),
    path('earnings_report/', earnings_report, name='earnings_report'),
    path('accept_order/<int:order_id>/', accept_order, name='accept_order'),
    path('delete_order/<int:order_id>/', delete_order, name='delete_order'),
    path('add_menu_item/', add_menu_item, name='add_menu_item'),
    path('logout/', logout_view, name='logout'),
    path('toggle_availability/<int:item_id>/', toggle_availability, name='toggle_availability'),# Add this line
]
