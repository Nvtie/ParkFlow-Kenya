from django.contrib import admin
from .models import (
    Vehicle,
    ParkingSlot,
    ParkingRate,
    ParkingSession,
    Payment,
    AuditRecord
)


admin.site.register(Vehicle)
admin.site.register(ParkingSlot)
admin.site.register(ParkingRate)
admin.site.register(ParkingSession)
admin.site.register(Payment)
admin.site.register(AuditRecord)
