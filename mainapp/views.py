# myapp/views.py
from django.shortcuts import render, get_object_or_404
from .models import Slider, Product, BlogPost


def index(request):
    # Fetch all slider items from the database
    sliders = Slider.objects.all()[:3]
       # Fetch all available products
    products = Product.objects.filter(is_available=True)[:6]

    # Prepare a list of products with their main images
    products_with_main_images = []
    for product in products:
        main_image = product.images.filter(is_main=True).first()
        products_with_main_images.append({
            "product": product,
            "main_image": main_image,
        })
    # Define the company values
    values = [
        {
            "title": "Excellence",
            "description": "We uphold honesty and transparency in all our actions and decisions.",
            "image":"Images/excellence.png"
        },
        {
            "title": "Customer Focus",
            "description": "We prioritize customer satisfaction.",
            "image":"Images/customerfocus.png"
        },
        {
            "title": "Agility & Perseverance",
            "description": "We adapt quickly and persistently overcome challenges.",
            "image":"/Images/agility&preservance.png"
        },
        {
            "title": "Caring",
            "description": "We care for our employees, customers, and community.",
            "image":"/Images/caring.png"
        },
        {
            "title": "Ownership & Accountability",
            "description": "We take responsibility for our actions.",
            "image":"/Images/ownership&accountability.png"
        },
    ]

    # Pass the data to the template
    context = {
        "sliders": sliders,
        "values": values,
         "products_with_main_images": products_with_main_images,
    }

    return render(request, "index.html", context)

def about(request):
    return render(request,"about.html" )

def contact(request):
    return render(request,"contact.html" )
def product_list(request):
    products = Product.objects.filter(is_available=True)

    # Prepare a list of products with their main images
    products_with_main_images = []
    for product in products:
        main_image = product.images.filter(is_main=True).first()
        products_with_main_images.append({
            "product": product,
            "main_image": main_image.image.url if main_image else None,  # Ensure correct image URL
        })
    return render(request, "product_list.html", {"products": products_with_main_images})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "product_detail.html", {"product": product})


def news_list(request):
    """
    View to display a list of published blog posts (news articles).
    """
    # Fetch all published blog posts, ordered by their publication date
    posts = BlogPost.objects.filter(is_published=True).order_by("-published_at")

    # Pass the posts to the template
    context = {
        "posts": posts,
    }

    return render(request, "news.html", context)


def news_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "product_detail.html", {"product": product})


def custom_404(request, exception):
    return render(request, "404.html", status=404)



