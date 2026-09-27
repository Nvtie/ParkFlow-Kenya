from django.shortcuts import render, redirect
from .models import Vehicle, ParkingSlot, ParkingSession
import uuid
from django.utils import timezone
from decimal import Decimal
from django.db.models import Sum, Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.decorators import login_required, user_passes_test


from .models import (
    Vehicle,
    ParkingSlot,
    ParkingSession,
    ParkingRate,
    Payment,
    AuditRecord
)

def is_management(user):
    return user.is_superuser or user.groups.filter(
        name='Management'
    ).exists()


def is_staff_member(user):
    return (
        user.is_superuser
        or user.groups.filter(
            name__in=['Management', 'Parking Staff']
        ).exists()
    )

@login_required
@user_passes_test(is_staff_member)
@login_required
@user_passes_test(is_staff_member)
def dashboard(request):

    slots = ParkingSlot.objects.all().order_by('slot_number')

    total_slots = slots.count()

    occupied_slots = slots.filter(
        status='OCCUPIED'
    ).count()

    available_slots = slots.filter(
        status='AVAILABLE'
    ).count()

    active_parking = ParkingSession.objects.filter(
        status='ACTIVE'
    ).select_related(
        'vehicle',
        'slot'
    ).order_by(
        '-entry_time'
    )

    active_sessions = active_parking.count()

    context = {
        'slots': slots,
        'total_slots': total_slots,
        'occupied_slots': occupied_slots,
        'available_slots': available_slots,
        'active_parking': active_parking,
        'active_sessions': active_sessions,
    }

    return render(
        request,
        'parking/dashboard.html',
        context
    )
@login_required
@transaction.atomic
@user_passes_test(is_staff_member)
def vehicle_entry(request):

    if request.method == 'POST':

        registration_number = request.POST.get(
            'registration_number',
            ''
        ).strip().upper()

        vehicle_type = request.POST.get(
            'vehicle_type',
            ''
        ).strip()

        if not registration_number:
            return render(
                request,
                'parking/entry.html',
                {
                    'error': 'Please enter the vehicle registration number.'
                }
            )

        # Check whether vehicle is already parked
        existing_vehicle = Vehicle.objects.filter(
            registration_number=registration_number
        ).first()

        if existing_vehicle:

            active_session = ParkingSession.objects.filter(
                vehicle=existing_vehicle,
                status='ACTIVE'
            ).first()

            if active_session:
                return render(
                    request,
                    'parking/entry.html',
                    {
                        'error': (
                            f'Vehicle {registration_number} '
                            'already has an active parking session.'
                        )
                    }
                )

        # Find an available slot
        slot = ParkingSlot.objects.filter(
            status='AVAILABLE'
        ).order_by('slot_number').first()

        if slot is None:
            return render(
                request,
                'parking/entry.html',
                {
                    'error': 'No parking slots are currently available.'
                }
            )

        # Create or retrieve vehicle
        vehicle, created = Vehicle.objects.get_or_create(
            registration_number=registration_number,
            defaults={
                'vehicle_type': vehicle_type
            }
        )

        # Create parking session
        ParkingSession.objects.create(
            vehicle=vehicle,
            slot=slot
        )

        # Occupy slot
        slot.status = 'OCCUPIED'
        slot.save()

        return redirect('dashboard')

    return render(
        request,
        'parking/entry.html'
    )

from django.utils import timezone
from decimal import Decimal
from .models import Vehicle, ParkingSlot, ParkingSession, ParkingRate, Payment

@login_required
@transaction.atomic
@user_passes_test(is_staff_member)
def vehicle_exit(request):

    result = None
    error = None

    if request.method == 'POST':

        registration_number = request.POST.get(
            'registration_number'
        ).strip().upper()

        payment_method = request.POST.get(
            'payment_method'
        )

        # Find the vehicle
        try:
            vehicle = Vehicle.objects.get(
                registration_number=registration_number
            )
        except Vehicle.DoesNotExist:
            error = "Vehicle not found."

            return render(
                request,
                'parking/exit.html',
                {'error': error}
            )

        # Find active parking session
        session = ParkingSession.objects.filter(
            vehicle=vehicle,
            status='ACTIVE'
        ).first()

        if session is None:
            error = "No active parking session found for this vehicle."

            return render(
                request,
                'parking/exit.html',
                {'error': error}
            )

        # Record exit time
        exit_time = timezone.now()
        session.exit_time = exit_time

        # Calculate duration
        duration = exit_time - session.entry_time

        duration_minutes = max(
            0,
            int(duration.total_seconds() / 60)
        )

        session.duration_minutes = duration_minutes

        # Find applicable parking rate
        rates = ParkingRate.objects.filter(
            minimum_minutes__lte=duration_minutes
        ).order_by('-minimum_minutes')

        rate = None

        for parking_rate in rates:

            if (
                parking_rate.maximum_minutes is None
                or duration_minutes <= parking_rate.maximum_minutes
            ):
                rate = parking_rate
                break

        if rate is None:
            error = "No parking rate has been configured for this duration."

            return render(
                request,
                'parking/exit.html',
                {'error': error}
            )

        # Calculate fee
        amount = rate.amount

        session.amount = amount
        session.save()

        result = {
            'vehicle': vehicle,
            'session': session,
            'duration': duration_minutes,
            'amount': amount,
            'payment_method': payment_method,
        }

        # Process payment
        if payment_method:

            payment = Payment.objects.create(
                session=session,
                amount=amount,
                payment_method=payment_method,
                transaction_reference=f"SIM-{uuid.uuid4().hex[:10].upper()}",
                payment_status='CONFIRMED',
                receipt_number=f"REC-{uuid.uuid4().hex[:10].upper()}",
                vat_amount=Decimal('0.00')
            )

            #Check payment confirmation
            if payment.payment_status == 'CONFIRMED':

                AuditRecord.objects.create(
                    payment=payment,
                    action="PAYMENT_CONFIRMED",
                    amount=amount,
                    user=request.user.username
                    if request.user.is_authenticated
                    else "System"
                )
            

            # Mark session completed
            session.status = 'COMPLETED'
            session.save()

            # Release parking slot
            slot = session.slot
            slot.status = 'AVAILABLE'
            slot.save()

            result['payment'] = payment
            result['barrier_status'] = 'OPEN'

            return redirect(
                'receipt',
                payment_id=payment.id
            )

        else:
            result['barrier_status'] = 'CLOSEDS'

    return render(
        request,
        'parking/exit.html',
        {
            'result': result,
            'error': error
        }
    )

@login_required
@user_passes_test(is_management)
def reports(request):

    confirmed_payments = Payment.objects.filter(
        payment_status='CONFIRMED'
    )

    # Overall revenue
    total_revenue = confirmed_payments.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')

    # Revenue by payment method
    cash_revenue = confirmed_payments.filter(
        payment_method='CASH'
    ).aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')

    mpesa_revenue = confirmed_payments.filter(
        payment_method='MPESA'
    ).aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')

    card_revenue = confirmed_payments.filter(
        payment_method='CARD'
    ).aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')

    # Transaction statistics
    total_transactions = confirmed_payments.count()

    completed_sessions = ParkingSession.objects.filter(
        status='COMPLETED'
    ).count()

    # Recent confirmed payments
    recent_payments = confirmed_payments.select_related(
        'session',
        'session__vehicle',
        'session__slot'
    ).order_by(
        '-payment_time'
    )[:20]

    context = {
        'total_revenue': total_revenue,
        'cash_revenue': cash_revenue,
        'mpesa_revenue': mpesa_revenue,
        'card_revenue': card_revenue,
        'total_transactions': total_transactions,
        'completed_sessions': completed_sessions,
        'recent_payments': recent_payments,
    }

    return render(
        request,
        'parking/reports.html',
        context
    )

@login_required
@user_passes_test(is_management)
def audit_log(request):

    audit_records = AuditRecord.objects.select_related(
        'payment',
        'payment__session',
        'payment__session__vehicle'
    ).order_by('-timestamp')

    context = {
        'audit_records': audit_records,
    }

    return render(
        request,
        'parking/audit.html',
        context
    )

def display(request):

    slots = ParkingSlot.objects.all().order_by('slot_number')

    total_slots = slots.count()

    occupied_slots = slots.filter(
        status='OCCUPIED'
    ).count()

    available_slots = slots.filter(
        status='AVAILABLE'
    ).count()

    context = {
        'slots': slots,
        'total_slots': total_slots,
        'occupied_slots': occupied_slots,
        'available_slots': available_slots,
    }

    return render(
        request,
        'parking/display.html',
        context
    )

@login_required
@user_passes_test(is_management)
def manage_rates(request):

    if request.method == 'POST':

        rate_id = request.POST.get('rate_id')

        try:
            rate = ParkingRate.objects.get(id=rate_id)

            rate.minimum_minutes = int(
                request.POST.get('minimum_minutes')
            )

            maximum_minutes = request.POST.get(
                'maximum_minutes'
            )

            if maximum_minutes:
                rate.maximum_minutes = int(maximum_minutes)
            else:
                rate.maximum_minutes = None

            rate.amount = Decimal(
                request.POST.get('amount')
            )

            rate.save()

        except (
            ParkingRate.DoesNotExist,
            ValueError,
            TypeError
        ):
            pass

        return redirect('manage_rates')

    rates = ParkingRate.objects.all().order_by(
        'minimum_minutes'
    )

    return render(
        request,
        'parking/rates.html',
        {'rates': rates}
    )
def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    error = None

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        error = 'Invalid username or password.'

    return render(
        request,
        'parking/login.html',
        {'error': error}
    )


def logout_view(request):

    logout(request)

    return redirect('login')


@login_required
def receipt(request, payment_id):

    try:
        payment = Payment.objects.select_related(
            'session',
            'session__vehicle',
            'session__slot'
        ).get(
            id=payment_id,
            payment_status='CONFIRMED'
        )

    except Payment.DoesNotExist:

        return render(
            request,
            'parking/receipt.html',
            {'payment': None}
        )

    return render(
        request,
        'parking/receipt.html',
        {
            'payment': payment
        }
    )
def is_management(user):
    return user.is_superuser or user.groups.filter(
        name='Management'
    ).exists()


def is_staff_member(user):
    return (
        user.is_superuser
        or user.groups.filter(
            name__in=['Management', 'Parking Staff']
        ).exists()
    )