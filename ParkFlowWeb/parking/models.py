from django.db import models



class Vehicle(models.Model):
    registration_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=50)

    def __str__(self):
        return self.registration_number


class ParkingSlot(models.Model):
    slot_number = models.PositiveIntegerField(unique=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('AVAILABLE', 'Available'),
            ('OCCUPIED', 'Occupied'),
        ],
        default='AVAILABLE'
    )

    def __str__(self):
        return f"Slot {self.slot_number}"


class ParkingRate(models.Model):
    minimum_minutes = models.PositiveIntegerField()
    maximum_minutes = models.PositiveIntegerField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    effective_from = models.DateTimeField(auto_now_add=True)
    effective_to = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"KSh {self.amount}"


class ParkingSession(models.Model):
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.PROTECT
    )

    slot = models.ForeignKey(
        ParkingSlot,
        on_delete=models.PROTECT
    )

    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(null=True, blank=True)

    duration_minutes = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('ACTIVE', 'Active'),
            ('COMPLETED', 'Completed'),
        ],
        default='ACTIVE'
    )

    def __str__(self):
        return f"{self.vehicle} - Slot {self.slot}"


class Payment(models.Model):
    session = models.OneToOneField(
        ParkingSession,
        on_delete=models.PROTECT
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=[
            ('MPESA', 'M-Pesa'),
            ('CARD', 'Card'),
            ('CASH', 'Cash'),
        ]
    )

    transaction_reference = models.CharField(
        max_length=100,
        blank=True
    )

    payment_time = models.DateTimeField(
        auto_now_add=True
    )

    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('CONFIRMED', 'Confirmed'),
            ('FAILED', 'Failed'),
        ],
        default='PENDING'
    )

    receipt_number = models.CharField(
        max_length=100,
        unique=True
    )

    vat_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.receipt_number


class AuditRecord(models.Model):
    payment = models.ForeignKey(
        Payment,
        on_delete=models.PROTECT
    )

    action = models.CharField(max_length=100)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    user = models.CharField(
        max_length=150,
        blank=True
    )

    def __str__(self):
        return self.action