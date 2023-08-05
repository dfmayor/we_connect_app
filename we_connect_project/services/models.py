import uuid
from datetime import timedelta
from django.db import models
from users.models import UserProfile, CustomUser as User
from django.db.models import Avg


# Create your models here.
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Service(models.Model):
    DURATION_CHOICES = (
        ('hours', 'Hours'),
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=255)
    description = models.TextField()
    picture = models.ImageField(upload_to="service_pics")
    price = models.DecimalField(default=0, decimal_places=2, max_digits=11)
    duration_quantity = models.PositiveIntegerField(default=1)
    duration_unit = models.CharField(choices=DURATION_CHOICES, max_length=10, default='hours')
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return f'{self.title} by {self.user.user.username}'

    def get_duration(self):
        if self.duration_unit == 'hours':
            return timedelta(hours=self.duration_quantity)
        elif self.duration_unit == 'days':
            return timedelta(days=self.duration_quantity)
        elif self.duration_unit == 'weeks':
            return timedelta(weeks=self.duration_quantity)
        elif self.duration_unit == 'months':
            return timedelta(weeks=self.duration_quantity * 4)
        
    def total_reviews(self):
        return Review.objects.filter(service=self).count()
    
    def average_rating(self):
        average = Review.objects.filter(service=self).aggregate(Avg('rating'))['rating__avg']
        return round(average, 2) if average else 0

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    rating = models.CharField(max_length=5)
    comment = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created', )
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f'Review by {self.reviewer} for {self.service.title}'


class Buyer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sellers')
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='buyers')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    started = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Contract between buyer "{self.buyer.user.username}" and seller "{self.seller.user.username}"'


class DirectMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def formatted_timestamp(self):
        return self.timestamp.strftime('%I:%M%p %A %d %B, %Y')

    def __str__(self):
        return f"From: {self.sender.username}, To: {self.receiver.username}, Sent at: {self.formatted_timestamp()}"
