from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F
from .models import Product,StockMovement, Category
from .forms import ProductForm, CategoryForm
from django.shortcuts import render
from django.core.mail import send_mail
from django.utils.timezone import now
from django.db.models.functions import TruncMonth
import qrcode
from io import BytesIO
from django.core.files import File
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
import csv
import pandas as pd
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})

def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('product_list')

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})

# Ajouter catégorie
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'products/category_form.html', {'form': form})

# Modifier catégorie
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'products/category_form.html', {'form': form})

# Supprimer catégorie
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'products/category_confirm_delete.html', {'category': category})

LOW_STOCK_THRESHOLD = 5
ADMIN_EMAIL = 'admin@exemple.com'

def dashboard(request):
    # -------------------------------
    # 1️⃣ Statistiques de base
    # -------------------------------
    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(quantity__lte=LOW_STOCK_THRESHOLD)
    low_stock_count = low_stock_products.count()
    total_stock_value = Product.objects.aggregate(
        total=Sum(F('price') * F('quantity'))
    )['total'] or 0

    # -------------------------------
    # 2️⃣ Produits par catégorie
    # -------------------------------
    categories = Product.objects.values('category').annotate(total_qty=Sum('quantity'))

    # -------------------------------
    # 3️⃣ Produits les plus vendus
    # -------------------------------
    top_selling = StockMovement.objects.filter(movement_type='OUT') \
        .values('product__name') \
        .annotate(total_sold=Sum('quantity')) \
        .order_by('-total_sold')[:5]

    # -------------------------------
    # 4️⃣ Historique entrées/sorties par mois
    # -------------------------------
    current_year = now().year
    monthly_movements = StockMovement.objects.filter(date__year=current_year) \
        .annotate(month=TruncMonth('date')) \
        .values('month','movement_type') \
        .annotate(total=Sum('quantity')) \
        .order_by('month')

    # -------------------------------
    # 5️⃣ Envoyer email alerte stock faible
    # -------------------------------
    if low_stock_products.exists():
        product_list = "\n".join([f"{p.name} ({p.quantity} restant)" for p in low_stock_products])
        send_mail(
            subject="⚠️ Alerte Stock Faible",
            message=f"Produits avec stock faible :\n{product_list}",
            from_email=None,
            recipient_list=[ADMIN_EMAIL],
            fail_silently=True,
        )

    # -------------------------------
    # 6️⃣ Context pour le template
    # -------------------------------
    context = {
        'total_products': total_products,
        'low_stock_count': low_stock_count,
        'low_stock_products': low_stock_products,
        'total_stock_value': total_stock_value,
        'categories': categories,
        'top_selling': top_selling,
        'monthly_movements': monthly_movements,
    }

    return render(request, 'products/dashboard.html', context)

def export_products_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=products.csv'

    writer = csv.writer(response)
    writer.writerow(['Nom', 'Prix', 'Quantité', 'Catégorie'])

    for p in Product.objects.all():
        writer.writerow([p.name, p.price, p.quantity, p.category])

    return response

# --- Export Excel ---
def export_products_excel(request):
    products = Product.objects.all().values('name','price','quantity','category')
    df = pd.DataFrame(products)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=products.xlsx'
    df.to_excel(response, index=False)
    return response

def import_products_csv(request):
    if request.method == "POST" and request.FILES['file']:
        import_file = request.FILES['file']
        import csv
        decoded_file = import_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        for row in reader:
            Product.objects.update_or_create(
                name=row['Nom'],
                defaults={
                    'price': row['Prix'],
                    'quantity': row['Quantité'],
                    'category': row['Catégorie']
                }
            )
    return redirect('product_list')

def generate_qrcode(product):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f"Produit: {product.name}\nID: {product.id}")
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    buffer = BytesIO()
    img.save(buffer)
    filename = f"qrcode_{product.id}.png"
    product.qrcode.save(filename, File(buffer), save=True)