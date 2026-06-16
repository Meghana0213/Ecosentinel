from django.db import models


class Complaint(models.Model):

    STATUS_CHOICES = [

        ('Pending', 'Pending'),

        ('In Progress', 'In Progress'),

        ('Resolved', 'Resolved'),

    ]

    waste_type = models.CharField(
        max_length=100,
        default="General Waste"
    )

    location = models.CharField(
        max_length=255
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to='complaints/'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    priority = models.CharField(
        max_length=20,
        default="Medium"
    )

    truck_number = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    driver_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    assigned_team = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):

        return self.waste_type