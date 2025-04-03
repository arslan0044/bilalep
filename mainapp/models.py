# mainapp/models.py

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField  # For rich text editing
from taggit.managers import TaggableManager  # For tagging posts

# Create your models here.


class Slider(models.Model):
    # Title of the product (e.g., "Fruit & Vegetables")
    title = models.CharField(max_length=255)

    # Description of the product
    description = models.TextField()

    # Image for the product
    image = models.ImageField(upload_to="slider_images/")

    # Link or action (optional, can be used for redirection)
    link = models.CharField(blank=True, null=True, max_length=30)

    # Timestamps for record-keeping
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title




class Product(models.Model):
    # Basic Product Information
    title = models.CharField(max_length=255, unique=True, help_text="The name of the product.")
    description = models.TextField(help_text="A detailed description of the product.")
    short_description = models.CharField(max_length=255, blank=True, null=True, help_text="A brief summary of the product.")
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Price of the product.")
    stock = models.PositiveIntegerField(default=0, help_text="Number of items available in stock.")
    is_available = models.BooleanField(default=True, help_text="Whether the product is currently available for purchase.")

    # SEO Fields
    slug = models.SlugField(unique=True, blank=True, null=True, help_text="URL-friendly version of the product title.")
    meta_title = models.CharField(max_length=255, blank=True, null=True, help_text="Title for SEO purposes (optional).")
    meta_description = models.TextField(blank=True, null=True, help_text="Meta description for search engines.")
    meta_keywords = models.CharField(max_length=255, blank=True, null=True, help_text="Comma-separated keywords for SEO.")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the product was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the product was last updated.")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Automatically generate a slug from the title if it's not provided.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Return the URL to access a particular product instance.
        """
        return reverse("product_detail", kwargs={"slug": self.slug})


class ProductImage(models.Model):
    """
    Model to store multiple images for a single product.
    """
    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE,
        help_text="The product this image belongs to."
    )
    image = models.ImageField(upload_to="product_images/", help_text="An image of the product.")
    alt_text = models.CharField(max_length=255, blank=True, null=True, help_text="Alternative text for the image (for accessibility).")
    is_main = models.BooleanField(default=False, help_text="Whether this is the main image for the product.")

    def __str__(self):
        return f"Image for {self.product.title}"
    


class Category(models.Model):
    """
    Model to categorize blog posts.
    """
    name = models.CharField(max_length=255, unique=True, help_text="The name of the category.")
    slug = models.SlugField(unique=True, blank=True, null=True, help_text="URL-friendly version of the category name.")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})


class BlogPost(models.Model):
    """
    Model for blog posts with SEO optimization and user engagement features.
    """
    # Basic Post Information
    title = models.CharField(max_length=255, unique=True, help_text="The title of the blog post.")
    slug = models.SlugField(unique=True, blank=True, null=True, help_text="URL-friendly version of the post title.")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts", help_text="The author of the post.")
    content = RichTextField(help_text="The main content of the blog post.")
    excerpt = models.TextField(blank=True, null=True, help_text="A short summary of the post (for previews).")
    featured_image = models.ImageField(upload_to="blog_images/", blank=True, null=True, help_text="Featured image for the post.")
    alt_text = models.CharField(max_length=255, blank=True, null=True, help_text="Alternative text for the featured image (for accessibility).")

    # Categorization
    categories = models.ManyToManyField(Category, related_name="posts", blank=True, help_text="Categories associated with the post.")
    tags = TaggableManager(blank=True, help_text="Tags for the post (comma-separated).")

    # SEO Fields
    meta_title = models.CharField(max_length=255, blank=True, null=True, help_text="Title for SEO purposes (optional).")
    meta_description = models.TextField(blank=True, null=True, help_text="Meta description for search engines.")
    meta_keywords = models.CharField(max_length=255, blank=True, null=True, help_text="Comma-separated keywords for SEO.")

    # Engagement Features
    likes = models.PositiveIntegerField(default=0, help_text="Number of likes for the post.")
    views = models.PositiveIntegerField(default=0, help_text="Number of views for the post.")
    allow_comments = models.BooleanField(default=True, help_text="Whether comments are allowed on the post.")
    is_published = models.BooleanField(default=False, help_text="Whether the post is published and visible to users.")
    published_at = models.DateTimeField(blank=True, null=True, help_text="Date and time when the post was published.")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the post was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the post was last updated.")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Automatically generate a slug from the title if it's not provided.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Return the URL to access a particular blog post instance.
        """
        return reverse("blog_detail", kwargs={"slug": self.slug})

    def increment_views(self):
        """
        Increment the view count for the post.
        """
        self.views += 1
        self.save(update_fields=["views"])


class Comment(models.Model):
    """
    Model for user comments on blog posts.
    """
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments", help_text="The post this comment belongs to.")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", help_text="The user who made the comment.")
    content = models.TextField(help_text="The content of the comment.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the comment was created.")
    is_approved = models.BooleanField(default=False, help_text="Whether the comment is approved by the admin.")

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"


class Like(models.Model):
    """
    Model to track likes on blog posts.
    """
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="post_likes", help_text="The post that was liked.")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes", help_text="The user who liked the post.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the like was recorded.")

    class Meta:
        unique_together = ("post", "user")  # Prevent duplicate likes

    def __str__(self):
        return f"Like by {self.user.username} on {self.post.title}"