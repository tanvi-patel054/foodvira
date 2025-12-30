from django.shortcuts import render, get_object_or_404
from apps.master.models import Contact, Blog, TeamMember
from apps.products.models import Product, ProductImages, ProductInquiry, Category
from django.contrib import messages
from django.shortcuts import redirect
from django.core.paginator import Paginator
# Create your views here.
def index(request):
    products = Product.objects.order_by('-created_at')[:8]   # last 8 added products
    blogs = Blog.objects.order_by('-created_at')[:3]          # last 3 added blogs

    context = {
        'products': products,
        'blogs': blogs
    }
    return render(request, "store/index.html", context)

def products(request):
    category_id = request.GET.get("category")

    categories = Category.objects.all()

    product_list = Product.objects.order_by("-created_at")

    # ✅ Filter by category if selected
    if category_id:
        product_list = product_list.filter(category_id=category_id)

    paginator = Paginator(product_list, 12)  # products per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "categories": categories,
        "products": page_obj.object_list,
        "page_obj": page_obj,
        "selected_category": category_id,
    }
    return render(request, "store/products.html", context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    product_images = ProductImages.objects.filter(product=product)

    # ✅ Related products (same category, exclude current)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id).order_by("-created_at")[:4]

    context = {
        "product": product,
        "product_images": product_images,
        "related_products": related_products,
    }
    return render(request, "store/product_detail.html", context)


def blog(request):
    blog_list = Blog.objects.order_by("-created_at")

    paginator = Paginator(blog_list, 6)  # 👈 blogs per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "blogs": page_obj.object_list,
        "page_obj": page_obj,
    }
    return render(request, "store/blog.html", context)


def product_inquiry(request):
    if request.method == "POST":
        product = get_object_or_404(Product, id=request.POST.get("product_id"))

        ProductInquiry.objects.create(
            product=product,
            name=request.POST.get("name"),
            mobile=request.POST.get("mobile"),
            quantity=request.POST.get("quantity"),
            message=request.POST.get("message"),
        )

        messages.success(request, "Your inquiry has been submitted successfully!")

        return redirect(request.META.get("HTTP_REFERER", "/"))

    return redirect("/")


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    latest_blogs = Blog.objects.exclude(id=blog.id).order_by('-created_at')[:5]

    
    # Optional: increment view count
    # blog.views = blog.views + 1 if blog.views else 1
    # blog.save(update_fields=['views'])
    
    context = {
        'blog': blog,
        "latest_blogs":latest_blogs
    }
    return render(request, 'store/blog_detail.html', context)

def about(request):
    # Get all team members ordered by the 'order' field
    team_members = TeamMember.objects.all()
    
    context = {
        'team_members': team_members
    }
    
    return render(request, "store/about.html", context)

def contact(request):
    if request.method == "POST":
        name_ = request.POST['name']
        email_ = request.POST['email']
        message_ = request.POST['message']
        print(name_, email_, message_)

        new_contact = Contact.objects.create(
            name = name_,
            email = email_,
            message = message_
        )
        new_contact.save()
        messages.success(request, "Your request submited successfully.")
        return redirect("contact")


    return render(request, "store/contact.html")