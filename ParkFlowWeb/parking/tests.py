from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from decimal import Decimal

from .models import (
    Vehicle,
    ParkingSlot,
    ParkingRate,
    ParkingSession,
    Payment,
    AuditRecord,
)


class ParkingSystemTests(TestCase):

    def setUp(self):

        # -----------------------------
        # Create Parking Staff user
        # -----------------------------

        self.user = User.objects.create_user(
            username='testadmin',
            password='testpassword123'
        )

        staff_group, created = Group.objects.get_or_create(
            name='Parking Staff'
        )

        self.user.groups.add(staff_group)

        # -----------------------------
        # Create Management user
        # -----------------------------

        self.manager = User.objects.create_user(
            username='testmanager',
            password='managerpassword123'
        )

        management_group, created = Group.objects.get_or_create(
            name='Management'
        )

        self.manager.groups.add(management_group)

        # -----------------------------
        # Create parking slot
        # -----------------------------

        self.slot = ParkingSlot.objects.create(
            slot_number=1,
            status='AVAILABLE'
        )

        # -----------------------------
        # Create parking rates
        # -----------------------------

        ParkingRate.objects.create(
            minimum_minutes=0,
            maximum_minutes=30,
            amount=0
        )

        ParkingRate.objects.create(
            minimum_minutes=31,
            maximum_minutes=120,
            amount=50
        )

        ParkingRate.objects.create(
            minimum_minutes=121,
            maximum_minutes=240,
            amount=100
        )

        ParkingRate.objects.create(
            minimum_minutes=241,
            maximum_minutes=360,
            amount=300
        )

        ParkingRate.objects.create(
            minimum_minutes=361,
            maximum_minutes=None,
            amount=500
        )

    # ==========================================
    # AUTHENTICATION TESTS
    # ==========================================

    def test_dashboard_requires_login(self):

        response = self.client.get(
            reverse('dashboard')
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_login_works(self):

        response = self.client.post(
            reverse('login'),
            {
                'username': 'testadmin',
                'password': 'testpassword123'
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

    # ==========================================
    # VEHICLE ENTRY TESTS
    # ==========================================

    def test_vehicle_entry(self):

        self.client.login(
            username='testadmin',
            password='testpassword123'
        )

        response = self.client.post(
            reverse('vehicle_entry'),
            {
                'registration_number': 'KCA 123A',
                'vehicle_type': 'Saloon'
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

        vehicle = Vehicle.objects.get(
            registration_number='KCA 123A'
        )

        session = ParkingSession.objects.get(
            vehicle=vehicle
        )

        self.assertEqual(
            session.status,
            'ACTIVE'
        )

        self.slot.refresh_from_db()

        self.assertEqual(
            self.slot.status,
            'OCCUPIED'
        )

    def test_duplicate_vehicle_is_rejected(self):

        self.client.login(
            username='testadmin',
            password='testpassword123'
        )

        vehicle = Vehicle.objects.create(
            registration_number='KCA 456B',
            vehicle_type='SUV'
        )

        ParkingSession.objects.create(
            vehicle=vehicle,
            slot=self.slot,
            status='ACTIVE'
        )

        self.slot.status = 'OCCUPIED'
        self.slot.save()

        response = self.client.post(
            reverse('vehicle_entry'),
            {
                'registration_number': 'KCA 456B',
                'vehicle_type': 'SUV'
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            ParkingSession.objects.filter(
                vehicle=vehicle,
                status='ACTIVE'
            ).count(),
            1
        )

    # ==========================================
    # PARKING RATE TESTS
    # ==========================================

    def test_parking_rates_exist(self):

        self.assertEqual(
            ParkingRate.objects.count(),
            5
        )

        free_rate = ParkingRate.objects.get(
            minimum_minutes=0,
            maximum_minutes=30
        )

        self.assertEqual(
            free_rate.amount,
            Decimal('0')
        )

        two_hour_rate = ParkingRate.objects.get(
            minimum_minutes=31,
            maximum_minutes=120
        )

        self.assertEqual(
            two_hour_rate.amount,
            Decimal('50')
        )

    # ==========================================
    # MANAGEMENT ACCESS TESTS
    # ==========================================

    def test_staff_cannot_access_reports(self):

        self.client.login(
            username='testadmin',
            password='testpassword123'
        )

        response = self.client.get(
            reverse('reports')
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_management_can_access_reports(self):

        self.client.login(
            username='testmanager',
            password='managerpassword123'
        )

        response = self.client.get(
            reverse('reports')
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_staff_cannot_manage_rates(self):

        self.client.login(
            username='testadmin',
            password='testpassword123'
        )

        response = self.client.get(
            reverse('manage_rates')
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_management_can_manage_rates(self):

        self.client.login(
            username='testmanager',
            password='managerpassword123'
        )

        response = self.client.get(
            reverse('manage_rates')
        )

        self.assertEqual(
            response.status_code,
            200
        )

    # ==========================================
    # AUDIT LOG ACCESS TESTS
    # ==========================================

    def test_staff_cannot_access_audit_log(self):

        self.client.login(
            username='testadmin',
            password='testpassword123'
        )

        response = self.client.get(
            reverse('audit_log')
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_management_can_access_audit_log(self):

        self.client.login(
            username='testmanager',
            password='managerpassword123'
        )

        response = self.client.get(
            reverse('audit_log')
        )

        self.assertEqual(
            response.status_code,
            200
        )

    # ==========================================
    # LIVE DISPLAY TEST
    # ==========================================

    def test_live_display_is_public(self):

        response = self.client.get(
            reverse('display')
        )

        self.assertEqual(
            response.status_code,
            200
        )

    # ==========================================
    # PAYMENT AND AUDIT MODEL TEST
    # ==========================================

    def test_payment_and_audit_record(self):

        vehicle = Vehicle.objects.create(
            registration_number='KCA 999Z',
            vehicle_type='Saloon'
        )

        session = ParkingSession.objects.create(
            vehicle=vehicle,
            slot=self.slot,
            status='COMPLETED',
            duration_minutes=90,
            amount=Decimal('50.00')
        )

        payment = Payment.objects.create(
            session=session,
            amount=Decimal('50.00'),
            payment_method='CASH',
            transaction_reference='TEST-REF-001',
            payment_status='CONFIRMED',
            receipt_number='TEST-REC-001',
            vat_amount=Decimal('0.00')
        )

        audit = AuditRecord.objects.create(
            payment=payment,
            action='PAYMENT_CONFIRMED',
            amount=Decimal('50.00'),
            user='testadmin'
        )

        self.assertEqual(
            payment.payment_status,
            'CONFIRMED'
        )

        self.assertEqual(
            payment.amount,
            Decimal('50.00')
        )

        self.assertEqual(
            audit.amount,
            Decimal('50.00')
        )

        self.assertEqual(
            audit.action,
            'PAYMENT_CONFIRMED'
        )

    # ==========================================
    # RECEIPT TEST
    # ==========================================

    def test_receipt_page(self):

        vehicle = Vehicle.objects.create(
            registration_number='KDA 321X',
            vehicle_type='SUV'
        )

        session = ParkingSession.objects.create(
            vehicle=vehicle,
            slot=self.slot,
            status='COMPLETED',
            duration_minutes=90,
            amount=Decimal('50.00')
        )

        payment = Payment.objects.create(
            session=session,
            amount=Decimal('50.00'),
            payment_method='MPESA',
            transaction_reference='MPESA-TEST-001',
            payment_status='CONFIRMED',
            receipt_number='REC-TEST-001',
            vat_amount=Decimal('0.00')
        )

        self.client.login(
            username='testadmin',
            password='testpassword123'
        )

        response = self.client.get(
            reverse(
                'receipt',
                args=[payment.id]
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )