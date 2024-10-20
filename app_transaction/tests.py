from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from app_transaction.models.transaction import Transaction


class TransactionModelTest(TestCase):

    def setUp(self):
        # Set up non-modified objects used by all test methods
        Transaction.objects.create(
            merchant_order_id='123456',
            pgw_order_id='pgw123456',
            merchant_id='merchant001',
            merchant_name='Test Merchant',
            user_id='user001',
            bank_name='Test Bank',
            bank_trx_id='banktrx001',
            request_amount=Decimal('100.00'),
            request_currency='USD',
            base_currency='USD',
            status='pending',
            transaction_type='payment'
        )

    def test_transaction_creation(self):
        """Test the proper creation and saving of a Transaction object."""
        transaction = Transaction.objects.get(merchant_order_id='123456')
        self.assertEqual(transaction.merchant_name, 'Test Merchant')
        self.assertEqual(transaction.request_amount, Decimal('100.00'))
        self.assertEqual(transaction.status, 'pending')

    def test_transaction_method_is_completed(self):
        transaction = Transaction.objects.get(merchant_order_id='123456')
        transaction.status = 'paid'  # Assuming 'paid' means the transaction is completed
        transaction.save()
        self.assertTrue(transaction.is_completed())

    def test_transaction_total_cost_calculation(self):
        """Test the total cost calculation of a transaction."""
        transaction = Transaction.objects.get(merchant_order_id='123456')
        expected_total_cost = transaction.request_amount + transaction.commission + transaction.transaction_fee
        self.assertEqual(transaction.calculate_total_cost(), expected_total_cost)

    def test_transaction_defaults(self):
        """Test default values of fields."""
        transaction = Transaction.objects.get(merchant_order_id='123456')
        self.assertEqual(transaction.commission, Decimal('0.00'))
        self.assertEqual(transaction.transaction_fee, Decimal('0.00'))
        self.assertEqual(transaction.transaction_type, 'payment')

    def test_string_representation(self):
        """Test the string representation of the transaction."""
        transaction = Transaction.objects.get(merchant_order_id='123456')
        self.assertEqual(str(transaction), f"Transaction {transaction.merchant_order_id} - {transaction.status}")

    def test_invalid_data(self):
        """Test validation for invalid field data."""
        transaction = Transaction(
            merchant_order_id='',
            pgw_order_id='pgw123457',
            merchant_id='merchant002',
            merchant_name='Invalid Merchant',
            user_id='user002',
            bank_name='Invalid Bank',
            bank_trx_id='banktrx002',
            request_amount=Decimal('-100.00'),  # Negative amount, should raise an error
            request_currency='ZZZ',  # Invalid currency code
            base_currency='ZZZ',
            status='nonexistent_status'  # Invalid status
        )
        with self.assertRaises(ValidationError):
            transaction.full_clean()

    def test_metadata_field(self):
        """Test that metadata JSONField works correctly."""
        transaction = Transaction.objects.get(merchant_order_id='123456')
        metadata = {'info': 'additional transaction details'}
        transaction.metadata = metadata
        transaction.save()
        updated_transaction = Transaction.objects.get(merchant_order_id='123456')
        self.assertEqual(updated_transaction.metadata, metadata)
