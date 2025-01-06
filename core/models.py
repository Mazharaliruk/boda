from django.utils import timezone

from django.db import models
from sales.models import Currency
from rest_framework.permissions import IsAuthenticated

# Create your models here.


# creating choices
class Status(models.TextChoices):
    DRAFT = "Draft"
    CONFIRMED = "Confirmed"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

    def __str__(self):
        return self.value


class BusinessType(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)
    image_url = models.ImageField(upload_to="business_types/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank=True)
    icon_url = models.ImageField(upload_to="business_types/", null=True, blank=True)

    def __str__(self):
        return self.name


class Business(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)
    image_url = models.ImageField(upload_to="business/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank=True)
    business_type = models.ForeignKey(BusinessType, on_delete=models.CASCADE)
    icon_url = models.ImageField(upload_to="business/", null=True, blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(
        "account.CustomerProfile", on_delete=models.CASCADE, null=True, blank=True
    )  # where role is customer
    location = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    price = models.FloatField(default=0.0)
    currency = models.CharField(
        max_length=3, choices=Currency.choices, default=Currency.PKR
    )
    image_url = models.ImageField(upload_to="event/", null=True, blank=True)
    guest_count = models.IntegerField(default=0)
    budget = models.FloatField(default=0.0)
    status = models.CharField(
        max_length=50, choices=Status.choices, default=Status.DRAFT
    )
    maximum_capacity = models.IntegerField(null=True, blank=True)
    minimum_capacity = models.IntegerField(null=True, blank=True)
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vendor = models.ForeignKey(
        "account.VendorProfile", on_delete=models.CASCADE
    )  # where role is vendor
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    price = models.FloatField(default=0.0)
    currency = models.CharField(
        max_length=3, choices=Currency.choices, default=Currency.PKR
    )

    def __str__(self):
        return self.name


class EventServiceStatus(models.TextChoices):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"

    def __str__(self):
        return self.value


class EventService(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    vendor = models.ForeignKey("account.VendorProfile", on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)
    price = models.FloatField(default=0.0)
    currency = models.CharField(
        max_length=3, choices=Currency.choices, default=Currency.PKR
    )
    status = models.CharField(
        max_length=50,
        choices=EventServiceStatus.choices,
        default=EventServiceStatus.PENDING,
    )

    def __str__(self):
        return self.status


class MediaType(models.TextChoices):
    IMAGE = "Image"
    VIDEO = "Video"

    def __str__(self):
        return self.value


class EventMedia(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    event_service = models.ForeignKey(
        EventService, on_delete=models.CASCADE, null=True, blank=True
    )
    media_file = models.FileField(
        upload_to="event_media/", null=True, blank=True
    )  # Stores both images and videos
    media_type = models.CharField(
        max_length=50, choices=MediaType.choices, default=MediaType.IMAGE
    )
    uploaded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.media_file.url) if self.media_file else "No media"


class Reviews(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, null=True, blank=True
    )
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)
    vendor = models.ForeignKey(
        "account.VendorProfile", on_delete=models.CASCADE, null=True, blank=True
    )
    rating = models.FloatField(default=0)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.service} - {self.rating}"


# Notification Table


class Notification(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    message = models.TextField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class AIRecommendation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    recommendation_data = models.JSONField(null=True)

    def __str__(self):
        return self.recommendation


class RoomStatus(models.TextChoices):
    ACTIVE = "Active"
    CLOSED = "Closed"
    ARCHIVED = "Archived"

    def __str__(self):
        return self.value


class RoomType(models.TextChoices):
    CUSTOMER = "Customer"
    VENDOR = "Vendor"
    ADMIN = "Admin"

    def __str__(self):
        return self.value


class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_id1 = models.ForeignKey("account.VendorProfile", on_delete=models.CASCADE)
    user_id2 = models.ForeignKey("account.CustomerProfile", on_delete=models.CASCADE)
    admin_id = models.ForeignKey("account.AdminProfile", on_delete=models.CASCADE)
    room_status = models.CharField(
        max_length=50, choices=RoomStatus.choices, default=RoomStatus.ACTIVE
    )
    room_type = models.CharField(
        max_length=50, choices=RoomType.choices, default=RoomType.CUSTOMER
    )

    def __str__(self):
        return self.name


class MessageType(models.TextChoices):
    TEXT = "Text"
    IMAGE = "Image"
    VIDEO = "Video"
    AUDIO = ("Audio",)
    FILE = "File"

    def __str__(self):
        return self.value


class DeliveryStatus(models.TextChoices):
    SENT = "Sent"
    DELIVERED = "Delivered"
    READ = "Read"

    def __str__(self):
        return self.value


class Messages(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=True, blank=True)

    # The ID of the sender (could be customer, vendor, or admin).
    sender_id = models.ForeignKey(
        "account.User", on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver_id = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="received_messages",
    )

    # Content of the message
    message_content = models.TextField(null=True, blank=True)
    message_type = models.CharField(
        max_length=50, choices=MessageType.choices, default=MessageType.TEXT
    )

    # Attachments (for file, image, video, audio types)
    attachment_url = models.URLField(
        null=True, blank=True, help_text="URL for the attached file or media."
    )

    # Read and sent timestamps
    sent_at = models.DateTimeField(default=timezone.now)
    read_at = models.DateTimeField(null=True, blank=True)

    # Status of the message
    is_read = models.BooleanField(
        default=False, help_text="Indicates if the message has been read."
    )
    is_deleted = models.BooleanField(
        default=False, help_text="Indicates if the message has been deleted."
    )

    # Parent message for threads (optional)
    parent_message = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="replies",
        help_text="Reference to the parent message in case of replies.",
    )

    # Priority or delivery status
    is_urgent = models.BooleanField(
        default=False, help_text="Marks if the message is urgent."
    )
    delivery_status = models.CharField(
        max_length=20,
        choices=DeliveryStatus.choices,
        default=DeliveryStatus.SENT,
        help_text="Status of the message delivery.",
    )

    def __str__(self):
        return (
            f"Message from {self.sender_id} to {self.receiver_id} - {self.message_type}"
        )
