from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Users, Customers, Products, Inventory, ProductCategory, Orders, OrderItems, Shipments, Payments

class SignUpForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ('username', 'email', 'role', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ['name', 'company_name', 'phone_number', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }









class CategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'category', 'color', 'brand', 'price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['quantity_in_stock', 'quantity_reserved', 'reorder_level']
        widgets = {
            'quantity_in_stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity_reserved': forms.NumberInput(attrs={'class': 'form-control'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control'}),
        }





class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['customer', 'delivery_date']

    delivery_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItems
        fields = ['product', 'quantity']

OrderItemFormSet = forms.inlineformset_factory(
    Orders,
    OrderItems,
    form=OrderItemForm,
    extra=1,
    can_delete=True
)


# Shipment

class ShipmentForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('In transit', 'In transit'),
        ('Delivered', 'Delivered'),
        ('Returned', 'Returned'),
    ]

    shipment_status = forms.ChoiceField(choices=STATUS_CHOICES, label='Yuk holati')

    class Meta:
        model = Shipments
        fields = ['courier_name', 'tracking_number', 'delivery_address', 'shipment_status']
        widgets = {
            'courier_name': forms.TextInput(attrs={'class': 'form-control'}),
            'tracking_number': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery_address': forms.TextInput(attrs={'class': 'form-control'}),
            'shipment_status': forms.Select(attrs={'class': 'form-select'}),
        }


# Payment

class PaymentForm(forms.ModelForm):
    PAYMENT_METHOD_CHOICES = [
        ('Naqd', 'Naqd'),
        ('Karta', 'Karta'),
        ('Bank o‘tkazmasi', 'Bank o‘tkazmasi'),
    ]
    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
    ]
    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES, label="To'lov usuli")
    status = forms.ChoiceField(choices=STATUS_CHOICES, label="To‘lov holati")

    class Meta:
        model = Payments
        fields = ['amount', 'payment_method', 'status']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
