from django.contrib import admin
from django.utils.html import format_html
from .models import Category, SubCategory, SubSubCategory, Product, ProductVariation, ExtraProductPicture, ExtraVariationProductPicture
from django.urls import reverse

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')


class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'category', 'slug')


class SubcategoryFilter(admin.SimpleListFilter):
    title = 'Subcategory'
    parameter_name = 'subcategory'

    def lookups(self, request, model_admin):
        subcategories = set()
        for product in Product.objects.all():
            subcategories.add((product.subcategory.id, product.subcategory.name))
        return sorted(subcategories, key=lambda x: x[1])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(subcategory__id=self.value())


class SubSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_subcategory', 'get_category', 'slug',)
    list_filter = (SubcategoryFilter, 'subcategory__category',)
    search_fields = ('name',)

    def get_category(self, obj):
        return obj.subcategory.category.name
    get_category.short_description = 'Category'

    def get_subcategory(self, obj):
        return obj.subcategory.name
    get_subcategory.short_description = 'SubCategory'
  
class ExtraProductPictureInline(admin.TabularInline):
    model = ExtraProductPicture
    extra = 1


class ExtraVariationProductPictureInline(admin.TabularInline):
    model = ExtraVariationProductPicture
    extra = 1


class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 1

    readonly_fields = ('view_product_variation',)

    def view_product_variation(self, obj):
        if obj.pk:
            url = reverse('admin:product_productvariation_change', args=[obj.pk])
            return format_html('<a href="{}">View ProductVariation</a>', url)
        else:
            return '-'

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductVariationInline, ExtraProductPictureInline]
    list_display = ('name', 'category', 'get_subcategory', 'subsubcategory', 'image_tag', 'available')
    list_filter = ('category', 'subcategory', 'subsubcategory', 'on_promotion', 'available')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.image.url))
        else:
            return ""

    image_tag.short_description = 'Image Preview'


    def get_category(self, obj):
      if obj.category.name:
        return obj.category.name
      return '-'
    get_category.short_description = 'Category'
  
    def get_subcategory(self, obj):
      if obj.subcategory.name:
        return obj.subcategory.name
      return '-'
    get_subcategory.short_description = 'SubCategory'

    def get_subcategory(self, obj):
        if obj.subcategory is not None and obj.subcategory.name:
            return obj.subcategory.name
        return '-'
    get_subcategory.short_description = 'SubCategory'

    """
    class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductVariationInline, ExtraProductPictureInline]
    list_display = ('name', 'category', 'get_subcategory', 'image_tag', 'available')
    list_filter = ('category', 'subcategory', 'on_promotion', 'available')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.image.url))
        else:
            return ""

    image_tag.short_description = 'Image Preview'


    def get_category(self, obj):
      if obj.category.name:
        return obj.category.name
      return '-'
    get_category.short_description = 'Category'
  
    def get_subcategory(self, obj):
      if obj.subcategory.name:
        return obj.subcategory.name
      return '-'
    get_subcategory.short_description = 'SubCategory'

    def get_subsubcategory(self, obj):
        if obj.subsubcategory.exists():
            return obj.subsubcategory.first().name
        return '-'
    get_subsubcategory.short_description = 'SubSubCategory'
    
    
    """
  
class ProductVariationAdmin(admin.ModelAdmin):
    inlines = [ExtraVariationProductPictureInline]
    list_display = (
        'name', 'product_link', 'image_tag', 'available', 'product_info', 'price', 'promotion_price',
    )
    list_editable = ('price', 'promotion_price',)
    list_filter = ('product__category', 'product__subcategory', 'product__subsubcategory', 'product__on_promotion', 'product__available')
    
    def product_link(self, obj):
        url = reverse('admin:product_product_change', args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', url, obj.product.name)
    product_link.short_description = 'Product'

    def get_category(self, obj):
        if obj.product.category.name:
            return obj.product.category.name
        return '-'
    get_category.short_description = 'Category'
  
    def get_subcategory(self, obj):
        if obj.product.subcategory.name:
            return obj.product.subcategory.name
        return '-'
    get_subcategory.short_description = 'SubCategory'

    def get_subsubcategory(self, obj):
        if obj.product.subsubcategory:
            return obj.product.subsubcategory.name
        return '-'
    get_subsubcategory.short_description = 'SubSubCategory'

    def product_info(self, obj):
        return format_html(
            '<div>{}</div><div>{}</div><div>{}</div>', 
            self.get_category(obj), 
            self.get_subcategory(obj),
            self.get_subsubcategory(obj)
        )
    product_info.short_description = 'Product Info'
  
    def image_tag(self, obj):
        if obj.product.image:
            return format_html('<img src="{}" style="max-width:70px; max-height:100px"/>'.format(obj.product.image.url))
        return ""

    image_tag.short_description = 'Image'


    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name in self.list_editable:
            formfield.widget.attrs.update({'style': 'width: 60px;'})
        return formfield
      
class ExtraProductPictureAdmin(admin.ModelAdmin):
    list_display = (
        'image_tag', 'product_link', 'get_category', 'get_subcategory', 'get_subsubcategory',
    )
    search_fields = ('product__name',)
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:70px; max-height:100px"/>'.format(obj.image.url))
        return ""

    image_tag.short_description = 'Image'

    def product_link(self, obj):
        url = reverse('admin:product_product_change', args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', url, obj.product.name)
    product_link.short_description = 'Product'

    image_tag.short_description = 'Image'
  
  
    def get_category(self, obj):
        if obj.product.category.name:
            return obj.product.category.name
        return '-'
    get_category.short_description = 'Category'
  
    def get_subcategory(self, obj):
        if obj.product.subcategory.name:
            return obj.product.subcategory.name
        return '-'
    get_subcategory.short_description = 'SubCategory'

    def get_subsubcategory(self, obj):
        if obj.product.subsubcategory:
            return obj.product.subsubcategory.name
        return '-'
    get_subsubcategory.short_description = 'SubSubCategory'

class ExtraVariationProductPictureAdmin(admin.ModelAdmin):
    list_display = (
        'image_tag', 'product_variation_link', 'get_category', 'get_subcategory', 'get_subsubcategory',
    )

    def product_variation_link(self, obj):
        url = reverse('admin:product_productvariation_change', args=[obj.variation.id])
        return format_html('<a href="{}">{}</a>', url, obj.variation.name)
    product_variation_link.short_description = 'Product Variation'

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:70px; max-height:100px"/>'.format(obj.image.url))
        return ""

    image_tag.short_description = 'Image'

    def get_category(self, obj):
        if obj.variation.product.category.name:
            return obj.variation.product.category.name
        return '-'
    get_category.short_description = 'Category'

    def get_subcategory(self, obj):
        if obj.variation.product.subcategory.name:
            return obj.variation.product.subcategory.name
        return '-'
    get_subcategory.short_description = 'SubCategory'
    def get_subsubcategory(self, obj):
        subsubcategory = obj.variation.product.subsubcategory
        if subsubcategory is not None:
            return subsubcategory.name
        return '-'
    get_subsubcategory.short_description = 'SubSubCategory'
  
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(SubSubCategory, SubSubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariation, ProductVariationAdmin)
admin.site.register(ExtraProductPicture, ExtraProductPictureAdmin)
admin.site.register(ExtraVariationProductPicture, ExtraVariationProductPictureAdmin)
"""
class VariationInLine(admin.TabularInline):
    model = models.ProductVariation
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )


class SubSubCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'category',
        'subcategory',
        'on_promotion',
    )

    list_editable = ('on_promotion', )
    inlines = [
        VariationInLine,
    ]


class VariationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'product',
    )
    ordering = (
        'product__slug',
        'name',
    )


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.SubCategory, SubCategoryAdmin)
admin.site.register(models.SubSubCategory, SubSubCategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductVariation, VariationAdmin)
admin.site.register(models.ExtraProductPicture)
admin.site.register(models.ExtraVariationProductPicture)

"""