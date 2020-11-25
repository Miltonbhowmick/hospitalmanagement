from django.db import models


class StatusChoice(models.TextChoices):
    PENDING_PAYMENT = 'pending_payment', 'Pending Payment'
    PROCESSING = 'processing', 'Processing'
    IN_TRANSIT = 'in_transit', 'In Transit'
    DELIVERED = 'delivered', 'Delivered'
    RETURN_REQUEST = 'return_request', 'Return Request'
    RETURN_IN_TRANSIT = 'return_in_transit', 'Return In Transit'
    RETURNED = 'returned', 'Returned'
    REFUND_INITIATED = 'refund_initiated', 'Refund Initiated'
    REFUNDED = 'refunded', 'Refunded'


class PaymentStatusChoice(models.TextChoices):
    PENDING = 'pending', 'Pending'
    SUCCESS = 'success', 'Success'
    FAILED = 'failed', 'Failed'