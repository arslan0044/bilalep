from django.contrib import admin
from .models import Slider, Product, ProductImage, Category, BlogPost, Comment, Like

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_published", "published_at", "views", "likes")
    list_filter = ("is_published", "categories", "tags")
    search_fields = ("title", "content", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("views",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "created_at", "is_approved")
    list_filter = ("is_approved",)
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    approve_comments.short_description = "Approve selected comments"


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "created_at")


@admin.register(Slider)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "link", "created_at")


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of empty forms to display


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "stock", "is_available")
    prepopulated_fields = {"slug": ("title",)}  # Auto-generate slug from title
    inlines = [ProductImageInline]  # Add inline form for images


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "is_main", "alt_text")
    list_filter = ("is_main",)
