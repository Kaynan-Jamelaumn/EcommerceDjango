from django.shortcuts import render, redirect

from django.http import JsonResponse

from .models import Product, Category, SubCategory, SubSubCategory, ProductVariation, ExtraVariationProductPicture

from django.core.paginator import Paginator

from django.urls import resolve

from django.shortcuts import render, get_object_or_404


# Create your views here.
def index(request):

    products = Product.objects.filter(available=True).order_by('id')
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    subsubcategories = SubSubCategory.objects.all()
    paginator = Paginator(products, 25)

    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    onPromotion = Product.objects.filter(on_promotion=True)
    return render(
        request, 'index.html', {
            'products': products,
            'categories': categories,
            'subcategories': subcategories,
            'subsubcategories': subsubcategories,
            'onPromotion': onPromotion
        })


def category(request, category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(available=True, category=category_id)
    paginator = Paginator(products, 3)

    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, 'product/category.html', {
        'products': products,
        'category': category
    })


def subcategory(request, category_id, subcategory_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(available=True,
                                      subcategory=subcategory_id)
    subcategory = SubCategory.objects.get(id=subcategory_id)
    paginator = Paginator(products, 25)

    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, 'product/subcategory.html', {
        'products': products,
        'category': category,
        'subcategory': subcategory
    })


def subsubcategory(request, subcategory_id, subsubcategory_id):
    subcategory = SubCategory.objects.get(id=subcategory_id)
    category = Category.objects.get(id=subcategory.category.id)
    products = Product.objects.filter(available=True,
                                      subsubcategory=subsubcategory_id)
    subsubcategory = SubSubCategory.objects.get(id=subsubcategory_id)
    paginator = Paginator(products, 25)

    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(
        request, 'product/subsubcategory.html', {
            'products': products,
            'category': category,
            'subcategory': subcategory,
            'subsubcategory': subsubcategory
        })


def detail(request, slug):
    #product = Product.objects.get(slug=slug)
    product = get_object_or_404(Product, slug=slug)
    category = Category.objects.get(id=product.category.id)
    if product.subcategory:
        subcategory = SubCategory.objects.get(id=product.subcategory.id)
    else:
        subcategory = None
    if product.subsubcategory:
        subsubcategory = SubSubCategory.objects.get(id=product.subsubcategory.id)
    else:
        subsubcategory = None
    return render(
        request, 'product/detail.html', {
            'detailproduct': product,
            'category': category,
            'subcategory': subcategory,
            'subsubcategory': subsubcategory,
        })


def search(request):
    result = request.GET.get('result')
    if result is None:
        current_url = resolve(request.path_info).url_name
        return render(request, current_url)

    products = Product.objects.all().filter(
        available=True, name__icontains=result).order_by('-id')
    #print(products.query)
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    paginator = Paginator(products, 25)

    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(
        request, 'product/search.html', {
            'products': products,
            'categories': categories,
            'subcategories': subcategories,
            'search': result
        })


def variation_on_change(request):
    if request.POST.get('action') == 'variation_on_change':
        variation_id = request.POST.get('variation_selected')
        variation = ProductVariation.objects.get(id=variation_id)
        if variation:
            pictures = ExtraVariationProductPicture.objects.filter(
                variation=variation)
            picture_list = []
            for picture in pictures:
                picture_list.append(picture.image.url)
            description = variation.long_description
            stock = variation.stock
            if variation.on_promotion == True:
                price = variation.price
                promotion_price = variation.promotion_price
                return JsonResponse({
                    'price': price,
                    'promotion_price': promotion_price,
                    'description': description,
                    'stock': stock,
                    'pictures': picture_list
                })
            else:
                price = variation.price
                return JsonResponse({
                    'price': price,
                    'description': description,
                    'stock': stock,
                    'pictures': picture_list,
                })
        return redirect('product:index')


def buy_product(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            request.POST.get('quantity')
        return redirect('product:index')
    else:
        redirect('account:login')


def select_filter(request):
    if request.POST.get('action') == "select-filter":
        filter = request.POST.get('filter')
        if filter == 'new':
            products = Product.objects.filter(available=False).order_by('-id')
        elif filter == 'default':
            products = Product.objects.filter(available=False).order_by('id')
        elif filter == 'high-price':
            pass
            #filter_product = Product.objects.filter(available=True).order_by('-price')
        elif filter == 'low-price':
            pass
            #filter_product = Product.objects.filter(available=True).order_by('price')
        categories = Category.objects.all()
        subcategories = SubCategory.objects.all()
        paginator = Paginator(products, 25)

        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)
        return render(
            request, 'clone.html', {
                'products': products,
                'categories': categories,
                'subcategories': subcategories
            })
