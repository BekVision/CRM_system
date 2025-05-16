from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from datetime import timedelta

from django.db.models import Q, Count, Sum, F, FloatField

from .forms import SignUpForm, LoginForm, CustomerForm, CategoryForm, ProductForm, InventoryForm, OrderCreateForm, OrderItemFormSet, ShipmentForm, PaymentForm
from .models import Customers, Orders, ProductCategory, Products, Inventory, OrderItems, Shipments, Payments



def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if user.role == 'admin':
                    return redirect('admin_dashboard')
                elif user.role == 'manager':
                    return redirect('manager_dashboard')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('login')

    total_orders = Orders.objects.count()
    total_revenue = Orders.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    customers_count = Customers.objects.count()
    products_count = Products.objects.count()
    low_stock_products = Inventory.objects.filter(quantity_in_stock__lte=F('reorder_level'))

    context = {
        'total_amount': total_orders,
        'total_revenue': total_revenue,
        'customers_count': customers_count,
        'products_count': products_count,
        'low_stock_products': low_stock_products,
    }
    return render(request, 'admin_dashboard.html', context)


@login_required
def manager_dashboard(request):
    if request.user.role != 'manager':
        return redirect('login')
    customers_count = Customers.objects.count()
    products_count = Products.objects.count()
    orders_count = Orders.objects.count()
    context = {
        'customers_count': customers_count,
        'products_count': products_count,
        'orders_count': orders_count,
    }
    return render(request, 'manager_dashboard.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'admin_dashboard.html')



# Customer View ________________________________
@login_required
def customers_view(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customers')
    else:
        form = CustomerForm()

    q = request.GET.get('q', '').strip()
    qs = Customers.objects.all()
    if q:
        qs = qs.filter(
            Q(name__icontains=q) |
            Q(company_name__icontains=q) |
            Q(email__icontains=q)
        )
    qs = qs.order_by('-created_at')

    return render(request, 'customers/customers_list.html', {
        'form': form,
        'customers': qs,
        'q': q,
    })

@login_required
def customer_update_view(request, pk):
    customer = get_object_or_404(Customers, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customers')
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customers/customer_form.html', {
        'form': form,
        'customer': customer,
    })

@login_required
def customer_delete_view(request, pk):
    customer = get_object_or_404(Customers, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customers')
    return render(request, 'customers/customer_confirm_delete.html', {
        'customer': customer,
    })

@login_required
def customer_orders_view(request, pk):
    customer = get_object_or_404(Customers, pk=pk)
    orders = Orders.objects.filter(customer=customer).order_by('-order_date')
    return render(request, 'customers/customer_orders.html', {
        'customer': customer,
        'orders': orders,
    })



# Product View ________________________________

@login_required
def category_list_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm()

    categories = ProductCategory.objects.all().order_by('-id')
    return render(request, 'products/categories_list.html', {
        'form': form,
        'categories': categories,
    })

@login_required
def category_update(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'products/category_form.html', {
        'form': form,
        'category': category,
    })

@login_required
def category_delete(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('categories')
    return render(request, 'products/category_confirm_delete.html', {
        'category': category,
    })


# -- PRODUCT CRUD --
@login_required
def product_list_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            Inventory.objects.get_or_create(product=product, defaults={
                'quantity_in_stock': 0,
                'quantity_reserved': 0,
                'reorder_level': 0,
            })
            return redirect('products')
    else:
        form = ProductForm()

    products = Products.objects.select_related('category').all().order_by('-id')
    return render(request, 'products/products_list.html', {
        'form': form,
        'products': products,
    })

@login_required
def product_update(request, pk):
    product = get_object_or_404(Products, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/product_form.html', {
        'form': form,
        'product': product,
    })

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Products, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products')
    return render(request, 'products/product_confirm_delete.html', {
        'product': product,
    })


# -- INVENTORY STATUS VIEW --
@login_required
def product_inventory(request, pk):
    product = get_object_or_404(Products, pk=pk)
    inventory = getattr(product, 'inventory', None)

    warning = False
    if inventory and inventory.quantity_in_stock < inventory.reorder_level:
        warning = True

    return render(request, 'products/product_inventory.html', {
        'product': product,
        'inventory': inventory,
        'warning': warning,
    })


# Order View ________________________________

@login_required
def order_list_view(request):
    # Optionally allow search/filtering
    orders = Orders.objects.select_related('customer').all().order_by('-order_date')
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_create_view(request):
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            order = form.save(commit=False)
            order.status = 'pending'
            order.total_amount = 0
            order.save()
            formset.instance = order
            items = formset.save(commit=False)
            total = 0
            for item in items:
                item.price = item.product.price
                item.save()
                total += item.price * item.quantity
            order.total_amount = total
            order.save()
            formset.save_m2m()
            return redirect('order_list')
    else:
        form = OrderCreateForm()
        formset = OrderItemFormSet()
    return render(request, 'orders/order_form.html', {
        'form': form,
        'formset': formset,
    })

@login_required
def order_update_status_view(request, pk):
    order = get_object_or_404(Orders, pk=pk)
    next_status = None
    if order.status == 'pending':
        next_status = 'approved'
    elif order.status == 'approved':
        next_status = 'delivered'

    if request.method == 'POST' and next_status:
        order.status = next_status
        order.save()
        return redirect('order_list')
    return render(request, 'orders/order_status_update.html', {
        'order': order,
        'next_status': next_status,
    })

@login_required
def order_detail_view(request, pk):
    order = get_object_or_404(Orders, pk=pk)
    items = order.order_items.select_related('product').all()
    item_list = []
    for item in items:
        total_for_item = item.quantity * item.price
        item_list.append({
            'item': item,
            'total': total_for_item,
        })
    total_paid = sum(p.amount for p in order.payments.all())

    return render(request, 'orders/order_detail.html', {
        'order': order,
        'items': item_list,
        'total_paid': total_paid
    })


# Shipment View ________________________________
def shipment_create(request, order_id):
    order = get_object_or_404(Orders, pk=order_id)
    if request.method == 'POST':
        form = ShipmentForm(request.POST)
        if form.is_valid():
            shipment = form.save(commit=False)
            shipment.order = order
            shipment.save()
            return redirect('shipment_detail', shipment_id=shipment.id)
    else:
        form = ShipmentForm()
    return render(request, 'shipment/shipment_form.html', {'form': form, 'order': order})

def shipment_detail(request, shipment_id):
    shipment = get_object_or_404(Shipments, pk=shipment_id)
    return render(request, 'shipment/shipment_detail.html', {'shipment': shipment})

def shipment_update(request, shipment_id):
    shipment = get_object_or_404(Shipments, pk=shipment_id)
    if request.method == 'POST':
        form = ShipmentForm(request.POST, instance=shipment)
        if form.is_valid():
            form.save()
            return redirect('shipment_detail', shipment_id=shipment.id)
    else:
        form = ShipmentForm(instance=shipment)
    return render(request, 'shipment/shipment_form.html', {'form': form, 'shipment': shipment})



# Shipment View ________________________________
def payment_create(request, order_id):
    order = get_object_or_404(Orders, pk=order_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.order = order
            payment.save()
            return redirect('payment_detail', payment_id=payment.id)
    else:
        form = PaymentForm()
    return render(request, 'payment/payment_form.html', {'form': form, 'order': order})

def payment_detail(request, payment_id):
    payment = get_object_or_404(Payments, pk=payment_id)
    return render(request, 'payment/payment_detail.html', {'payment': payment})

def payment_update(request, payment_id):
    payment = get_object_or_404(Payments, pk=payment_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('payment_detail', payment_id=payment.id)
    else:
        form = PaymentForm(instance=payment)
    return render(request, 'payment/payment_form.html', {'form': form, 'payment': payment})


# main_____________________________

def admin_stats_view(request):
    now = timezone.now()

    todays_orders = Orders.objects.filter(order_date__date=now.date()).count()

    year_orders = Orders.objects.filter(order_date__year=now.year).count()

    top_products = (
        OrderItems.objects.values(name=F('product__name'))
        .annotate(total=Count('id'))
        .order_by('-total')[:5]
    )

    customers_count = Customers.objects.count()
    customers_created = Customers.objects.filter(created_at__date=now.date()).count()
    customers_deleted = 0

    months = []
    revenues = []
    for i in range(11, -1, -1):
        month = (now - timedelta(days=i * 30)).replace(day=1)
        beg = month
        end = (beg + timedelta(days=32)).replace(day=1)
        monthly_payments = Payments.objects.filter(
            payment_date__gte=beg, payment_date__lt=end, status='Paid'
        ).aggregate(summ=Sum('amount'))['summ'] or 0
        months.append(month.strftime("%Y-%m"))
        revenues.append(monthly_payments)

    # CRUD statistika
    order_crud = {
        'created': Orders.objects.count(),
        'updated': Orders.objects.filter(order_date__gte=now - timedelta(days=1)).count(),
        'deleted': 0,
    }
    product_crud = {
        'created': Products.objects.count(),
        'updated': 0,
        'deleted': 0,
    }
    customer_crud = {
        'created': customers_count,
        'updated': 0,
        'deleted': customers_deleted
    }

    context = {
        'todays_orders': todays_orders,
        'year_orders': year_orders,
        'top_products': top_products,
        'customers_count': customers_count,
        'customers_created': customers_created,
        'months': months,
        'revenues': revenues,
        'order_crud': order_crud,
        'product_crud': product_crud,
        'customer_crud': customer_crud,
    }
    return render(request, 'admin_stats.html', context)