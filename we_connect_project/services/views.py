import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import Category, DirectMessage, Order, Review, Service
from .decorators import service_providers_only
from users.decorators import superuser_required
from django.core.paginator import Paginator
from django.db.models import Avg
from users.models import CustomUser as User, UserProfile

@login_required
@superuser_required
def add_category(request):
    if request.method == 'POST':
        category = request.POST['category']
        Category.objects.create(name=category)
        messages.success(request, 'Category Created Successfully')
        return HttpResponseRedirect('/services/list_category')
    return render(request, 'services/add_category.html')


@login_required
@superuser_required
def list_category(request):
    categories = Category.objects.all()
    return render(request, 'services/list_category.html', {'categories': categories})


@login_required
@service_providers_only
def create_service(request):
    if request.method == 'POST':
        selected_categories = request.POST.getlist('categories')
        title = request.POST['title']
        description = request.POST['description']
        picture = request.FILES['picture']
        price = request.POST['price']
        duration_quantity = request.POST['duration_quantity']
        duration_unit = request.POST['duration_unit']
        try:
            service = Service(
                user=request.user.userprofile, title=title, description=description, picture=picture, price=price,
                duration_quantity=duration_quantity, duration_unit=duration_unit
            )
            service.save()

            for category_id in selected_categories:
                category = Category.objects.get(id=category_id)
                service.category.add(category)
            messages.success(request, 'Service created successfully')
            return render(request, 'users/success.html')
        except:
            messages.error(request, 'Failed To Create Service')
            return render(request, 'services/create_service.html')
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'services/create_service.html', context)


@login_required
def service_details(request, id):
    service = Service.objects.get(id=id)
    all_reviews = Review.objects.filter(service=service)
    paginator = Paginator(all_reviews, 3)
    page = request.GET.get('page')
    reviews = paginator.get_page(page)
    order_exists = Order.objects.filter(buyer=request.user.userprofile, service=service).exists()
    context = {
        'service': service, 'reviews': reviews, 'order_exists': order_exists
    }
    return render(request, 'services/service_deatils.html', context)


def category_services(request, category_id):
    category = Category.objects.get(id=category_id)
    services = Service.objects.all()
    get_services = [service for service in services if category in service.category.all()]
    context = {
        'category': category,
        'services': get_services,
        'services_length': len(get_services)
    }

    return render(request, 'services/category_services.html', context)

@login_required
def add_review(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            reviewer = request.user
            service_id = data.get("service_id")
            rating = data.get('rating')
            comment = data.get("comment")
            Review.objects.create(
                reviewer=reviewer, service_id=service_id, rating=rating, comment=comment
            )
            return JsonResponse({'status': 'success', 'message': 'Review Created Successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': "error", 'message': 'Failed to add review'})


@login_required
def request_service(request):
    buyer = request.user.userprofile
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            seller_id = data.get('seller_id')
            service_title = data.get('service_title')
            service_id = data.get('service_id')
            receiver = User.objects.get(id=seller_id)
            seller = UserProfile.objects.get(user=receiver)
            service = Service.objects.get(id=service_id)
            message = f'{request.user.username} requested your service "{service_title}"'
            if Order.objects.filter(buyer=buyer, service_id=service_id).exists():
                return JsonResponse({'status': 'error', 'message': 'Order already exists'})
            Order.objects.create(
                seller=seller, buyer=buyer, service=service
            )
            # create direct message
            DirectMessage.objects.create(
                sender=request.user, receiver=receiver, service=service, message=message
            )
            return JsonResponse({'status': 'success', 'message': 'Order Created Successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': "error", 'message': 'Failed to request order'})

@login_required
def get_home_services(request):
    services = Service.objects.order_by('created').all()
    service_list = []
    average_rating = 0.0

    for service in services:
        # Get the review instances related to the current service
        reviews = Review.objects.filter(service=service)

        # Calculate the average rating for the service if there are reviews
        if reviews.exists():
            total_rating = sum(review.rating for review in reviews)
            average_rating = total_rating / reviews.count()

        # Create a dictionary for the service and its reviews
        service_data = {
            'id': service.id,
            'user': service.user.user.username,
            'title': service.title,
            'picture': service.picture.url,  # Use the URL of the picture
            'price': str(service.price),  # Convert the DecimalField to string for JSON serialization
            'duration_quantity': service.duration_quantity,
            'duration_unit': service.duration_unit,
            'average_rating': average_rating,  # Add the average rating to the service data
            'reviews': [],  # List to store the reviews
        }

        # Add each review's data to the 'reviews' list in the service_data dictionary
        for review in reviews:
            review_data = {
                'reviewer': review.reviewer.username,
                'rating': review.rating,
                'comment': review.comment,
            }
            service_data['reviews'].append(review_data)

        # Add the service_data dictionary to the service_list
        service_list.append(service_data)

    return JsonResponse({'services': service_list})

@login_required
def update_is_read(request, id):
    if request.method == 'POST':
        message = DirectMessage.objects.get(service__id=id)
        message.is_read = True
        message.save()
        return JsonResponse({'status': 'success', 'message': "message updated successfully"})
    return JsonResponse({'status': 'error', 'message': "invalid response"})