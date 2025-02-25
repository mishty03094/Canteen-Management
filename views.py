from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import MenuItem, Order, Earnings,  CartItem
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.db.models import Sum, F


from .models import OrderItem  # Correct import statement
  # Ensure this is the correct path to your OrderDetail model


# Earnings Report View
@login_required
def earnings_report(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')

    # Get earnings for today
    today_earnings = Earnings.daily_earnings().aggregate(Sum('amount'))['amount__sum'] or 0
    print(f"Today's Earnings: ₹{today_earnings}")

    # Get earnings for this month
    monthly_earnings = Earnings.monthly_earnings().aggregate(Sum('amount'))['amount__sum'] or 0
    print(f"This Month's Earnings: ₹{monthly_earnings}")

    # Get earnings for this year
    yearly_earnings = Earnings.yearly_earnings().aggregate(Sum('amount'))['amount__sum'] or 0
    print(f"This Year's Earnings: ₹{yearly_earnings}")

    return render(request, 'earnings_report.html', {
        'today_earnings': today_earnings,
        'monthly_earnings': monthly_earnings,
        'yearly_earnings': yearly_earnings,
    })


# Custom Login View
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy('owner_dashboard')
        return reverse_lazy('user_dashboard')


# Welcome page
def welcome(request):
    return render(request, 'welcome.html')


# Owner Dashboard View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import MenuItem, Order


from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import MenuItem, Order

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import MenuItem, Order
@login_required
def owner_dashboard(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')

    # Fetch menu items (excluding those with 0 quantity)
    menu_items = MenuItem.objects.filter(quantity__gt=0)

    # Fetch all orders that are in 'ordered', 'confirmed', 'prepared', or 'delivered'
    orders = Order.objects.filter(status__in=['ordered', 'confirmed', 'prepared'])

    # Handle actions on orders or menu items
    if request.method == 'POST':
        if "toggle_availability" in request.POST:
            # Toggle menu item availability
            item_id = request.POST.get("item_id")
            menu_item = get_object_or_404(MenuItem, id=item_id)
            menu_item.available = not menu_item.available
            menu_item.save()

        else:
            # Handle order actions
            order_id = request.POST.get('order_id')
            action = request.POST.get('action')

            try:
                order = Order.objects.get(id=order_id)

                if action == 'confirm':
                    # Mark the order as confirmed
                    order.status = 'confirmed'
                    order.save()

                elif action == 'accept':
                    # Mark the order as prepared (and deduct quantities)
                    order.status = 'prepared'
                    order.prepared_at = timezone.now()
                    order.save()

                    # Deduct quantity from the menu items
                    for order_item in order.order_items.all():
                        menu_item = order_item.menu_item
                        menu_item.quantity -= order_item.quantity
                        menu_item.save()

                elif action == 'mark_delivered':
                    # Mark the order as delivered
                    order.status = 'delivered'
                    order.delivered_at = timezone.now()
                    order.save()

            except Order.DoesNotExist:
                pass

    return render(request, 'owner_dashboard.html', {'menu_items': menu_items, 'orders': orders})


# Add Menu Item View
@login_required
def add_menu_item(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')

    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        quantity = request.POST['quantity']
        available = request.POST.get('available') == 'on'

        # Create and save a new menu item
        MenuItem.objects.create(name=name, price=price, quantity=quantity, available=available)
        messages.success(request, "Menu item added successfully!")
        return redirect('owner_dashboard')

    return render(request, 'add_menu_items.html')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, MenuItem


@login_required
def mark_prepared(request, order_id):
    # Get the order from the database
    order = get_object_or_404(Order, id=order_id)
    order.status = 'prepared'
    order.save()

    # Ensure the order is in the 'confirmed' state before processing
    '''if order.status == 'confirmed':
        # Iterate through the order items and decrease the quantity
        for order_item in order.order_items.all():
            menu_item = order_item.menu_item
            menu_item.quantity -= order_item.quantity  # Decrease the menu item quantity
            menu_item.save()

            # If the quantity reaches zero, delete the item from the menu
            if menu_item.quantity == 0:
                menu_item.delete()

        # Update the order status to 'prepared
        

        messages.success(request, f"Order {order.id} marked as prepared.")
    else:
        messages.error(request, f"Order {order.id} cannot be marked as prepared because it is not confirmed.")'''

    # Redirect back to the owner dashboard
    return redirect('owner_dashboard')



from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Order, MenuItem, OrderItem

# Mark Delivered view
from django.utils import timezone

@login_required
def mark_delivered(request, order_id):
    # Get the order object
    order = get_object_or_404(Order, id=order_id)

    # Only proceed if the order is 'prepared'
    if order.status == 'prepared':
        # Iterate through the order items and decrease the quantity
        for order_item in order.order_items.all():
            menu_item = order_item.menu_item
            menu_item.quantity -= order_item.quantity  # Decrease the menu item quantity
            menu_item.save()

            # If the quantity reaches zero, delete the item from the menu
            if menu_item.quantity == 0:
                menu_item.delete()

        # Update the order status to 'delivered'
        order.status = 'delivered'
        order.delivered_at = timezone.now()
        order.save()

        messages.success(request, f"Order {order.id} marked as delivered.")
    else:
        messages.error(request, f"Order {order.id} cannot be marked as delivered because it is not prepared.")

    # Redirect back to the owner dashboard
    return redirect('owner_dashboard')



# User Dashboard View
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import F
from .models import MenuItem, Order, CartItem
from django.contrib import messages

@login_required
def user_dashboard(request):
    # Fetch available menu items (excluding those with 0 quantity)
    menu_items = MenuItem.objects.filter(available=True, quantity__gt=0)

    # Handle placing an order
    if request.method == 'POST' and 'order_item' in request.POST:
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity'))
        menu_item = MenuItem.objects.get(id=item_id)

        # Check stock availability
        if menu_item.quantity >= quantity:
            total_price = menu_item.price * quantity

            # Create an order
            Order.objects.create(
                user=request.user,
                menu_item=menu_item,
                quantity=quantity,
                total_price=total_price,
            )

            # Reduce the quantity of the menu item
            menu_item.quantity = F('quantity') - quantity
            menu_item.save()

            messages.success(request, "Order placed successfully!")
        else:
            messages.error(request, f"Only {menu_item.quantity} of {menu_item.name} available.")

    # Retrieve user's orders
    user_orders = Order.objects.filter(user=request.user)

    # Fetch cart items
    cart_items = CartItem.objects.filter(user=request.user)

    # Calculate the total amount in the cart
    total_amount = 0
    for item in cart_items:
        total_amount += item.quantity * item.menu_item.price  # Assuming CartItem has 'product' and 'quantity'

    return render(request, 'user_dashboard.html', {
        'menu_items': menu_items,
        'user_orders': user_orders,
        'cart_items': cart_items,
        'total_amount': total_amount,  # Pass total_amount to the template
    })


# Accept Order (Mark as Prepared)
@login_required
def accept_order(request, order_id):
    if not request.user.is_staff:
        return redirect('user_dashboard')

    order = Order.objects.get(id=order_id)
    order.status = 'prepared'
    order.save()

    messages.success(request, f"Order {order.id} marked as prepared.")
    return redirect('owner_dashboard')


# Delete Order After Delivery
@login_required
def delete_order(request, order_id):
    if not request.user.is_staff:
        return redirect('user_dashboard')

    order = Order.objects.get(id=order_id)

    # Create an earnings entry for the order
    Earnings.objects.create(
        user=request.user,
        order=order,
        amount=order.total_price,
    )

    # Delete the order after delivery
    order.delete()

    messages.success(request, f"Order {order.id} deleted after delivery.")
    return redirect('owner_dashboard')


# Logout View
@login_required
def logout_view(request):
    if request.method == 'POST' and request.POST.get('confirm') == 'yes':
        logout(request)  # Logs the user out
        return redirect('welcome')  # Redirect to the welcome page after logout
    return render(request, 'logout_confirm.html')


# Toggle Menu Item Availability
from django.shortcuts import render, get_object_or_404, redirect
from .models import MenuItem

def toggle_availability(request, item_id):
    # Get the item by ID
    item = get_object_or_404(MenuItem, id=item_id)

    # Toggle the availability status
    item.toggle_availability()

    # Redirect back to the owner dashboard
    return redirect('owner_dashboard')


# Add To Cart View
def add_to_cart(request):
    if request.method == "POST":
        item_id = request.POST['item_id']
        quantity = int(request.POST['quantity'])

        item = MenuItem.objects.get(id=item_id)
        user = request.user

        # Check if the item already exists in the cart
        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            menu_item=item,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return redirect('user_dashboard')


# View Cart
@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []

    # Retrieve menu items for cart display
    for item_id, item_data in cart.items():
        menu_item = MenuItem.objects.get(id=item_id)
        cart_items.append({
            'item': menu_item,
            'quantity': item_data['quantity'],
            'total_price': float(item_data['price']) * item_data['quantity']
        })

    return render(request, 'cart.html', {'cart_items': cart_items})


# Confirm Order



# Finalize Confirmed Order
@login_required
def finalize_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty!")
        return redirect('user_dashboard')

    total_amount = 0
    for item_id, item_data in cart.items():
        menu_item = MenuItem.objects.get(id=item_id)
        total_amount += float(item_data['price']) * item_data['quantity']

    # Create the order and reduce stock
    for item_id, item_data in cart.items():
        menu_item = MenuItem.objects.get(id=item_id)
        quantity = item_data['quantity']
        Order.objects.create(
            user=request.user,
            menu_item=menu_item,
            quantity=quantity,
            total_price=menu_item.price * quantity,
        )
        menu_item.quantity = F('quantity') - quantity
        menu_item.save()

    # Clear the cart after successful order
    request.session['cart'] = {}
    messages.success(request, f"Your order has been placed successfully!")
    return redirect('user_dashboard')


from django.shortcuts import render, redirect
from .models import CartItem, MenuItem
from django.contrib import messages


# View to update cart item quantity
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CartItem  # Assuming you have a CartItem model

# View to update the quantity of an item in the cart
@login_required
def update_cart_item(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        if request.method == 'POST':
            # Assuming the form has a field for the updated quantity
            new_quantity = request.POST.get('quantity')
            if new_quantity.isdigit() and int(new_quantity) > 0:
                cart_item.quantity = int(new_quantity)
                cart_item.save()
                messages.success(request, "Cart item updated successfully.")
            else:
                messages.error(request, "Invalid quantity.")
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found in cart.")

    return redirect('user_dashboard')



from django.shortcuts import render, redirect
from .models import CartItem
from django.contrib import messages


# View to remove a cart item
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CartItem  # Assuming you have a CartItem model

# View to remove an item from the cart
@login_required
def remove_from_cart(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found in cart.")

    return redirect('user_dashboard')



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order


# View to cancel an order
@login_required
def cancel_order(request):
    # Delete all cart items for the current user
    CartItem.objects.filter(user=request.user).delete()

    messages.success(request, "Your cart has been cleared.")
    return redirect('user_dashboard')


from django.core.mail import send_mail




from django.shortcuts import render, redirect
from .models import Order
from django.contrib.auth.decorators import login_required


# In your views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CartItem, Order, OrderItem


from django.shortcuts import render, redirect
from .models import MenuItem, Order, OrderItem

from django.shortcuts import render, redirect
from .models import MenuItem, Order, OrderItem

@login_required
def confirm_order(request):
    # Retrieve the user's cart items and calculate the total
    cart_items = CartItem.objects.filter(user=request.user)
    total_amount = sum(item.menu_item.price * item.quantity for item in cart_items)

    # Place an order and mark it as confirmed
    if request.method == 'POST':
        # Create the order
        order = Order.objects.create(
            user=request.user,
            total_price=total_amount,
            status='confirmed'  # Assuming status is a valid choice in your model
        )

        # Loop through the cart items and create order items
        for item in cart_items:
            order_item_total_price = item.menu_item.price * item.quantity

            # Create the order items linked to the order
            OrderItem.objects.create(
                order=order,
                menu_item=item.menu_item,
                quantity=item.quantity,
                total_price=order_item_total_price  # Pass the total_price here
            )

            # Clear the cart after placing the order
            item.delete()

        # Redirect to the order_confirmed page with the order_id
        return redirect('order_confirmed', order_id=order.id)

    return render(request, 'confirm_order.html', {
        'cart_items': cart_items,
        'total_amount': total_amount
    })
 # Use the name of your URL for /cart/confirm


from django.shortcuts import render
from .models import Order

def order_confirmation_page(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return render(request, '404.html')  # handle the case where the order is not found

    # Assuming order status is a field of the Order model
    order_status = order.status  # or any other logic to determine the order status

    return render(request, 'order_confirmed.html', {
        'order': order,
        'order_status': order_status
    })


from django.shortcuts import render, get_object_or_404
from .models import Order


def order_confirmed(request, order_id=None):
    if order_id is None:
        return render(request, 'order_confirmed.html', {
            'order_status': "No specific order selected.",
            'order': None,
            'order_items': None,
            'total_price': 0
        })
    else:
        # Example data fetching from the database
        order = get_object_or_404(Order, id=order_id)
        order_items = order.items.all()  # Assuming Order has a related field `items`
        total_price = sum(item.quantity * item.price for item in order_items)
        return render(request, 'order_confirmed.html', {
            'order_status': "Order Confirmed!",
            'order': order,
            'order_items': order_items,
            'total_price': total_price
        })
@login_required
def owner_mark_prepared(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = Order.PREPARED
    order.save()
    return redirect('order_confirmed')

# View Cart

def update_order_status(request, order_id):
    # Fetch the order
    order = Order.objects.get(id=order_id)

    # Mark the order as 'prepared' if the action is triggered
    if request.POST.get('mark_prepared'):
        order.status = 'prepared'
        order.save()

    # Mark the order as 'delivered' if the action is triggered
    elif request.POST.get('mark_delivered'):
        order.status = 'delivered'
        order.save()

    return redirect('owner_dashboard')


