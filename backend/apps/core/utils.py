"""
Common utility functions.
"""
import hashlib
import hmac
import secrets
from typing import Optional
from django.conf import settings
from django.core.files.storage import default_storage
import boto3
from botocore.exceptions import ClientError


def generate_transaction_id(prefix: str = 'TXN') -> str:
    """
    Generate a unique transaction ID.
    
    Args:
        prefix: Prefix for the transaction ID
        
    Returns:
        Unique transaction ID string
    """
    random_part = secrets.token_hex(8).upper()
    return f"{prefix}-{random_part}"


def calculate_platform_fee(amount: float) -> float:
    """
    Calculate platform fee based on donation amount.
    
    Args:
        amount: Donation amount
        
    Returns:
        Platform fee amount
    """
    fee_percentage = settings.PLATFORM_FEE_PERCENTAGE
    return round((amount * fee_percentage) / 100, 2)


def generate_presigned_url(
    file_key: str,
    expiration: int = 3600,
    http_method: str = 'PUT'
) -> Optional[str]:
    """
    Generate a presigned URL for S3 file upload/download.
    
    Args:
        file_key: S3 object key
        expiration: URL expiration time in seconds
        http_method: HTTP method (PUT for upload, GET for download)
        
    Returns:
        Presigned URL string or None if S3 is not configured
    """
    if not settings.USE_S3:
        return None
    
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        
        url = s3_client.generate_presigned_url(
            ClientMethod='put_object' if http_method == 'PUT' else 'get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': file_key,
            },
            ExpiresIn=expiration
        )
        return url
    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        return None


def verify_webhook_signature(payload: str, signature: str, secret: str) -> bool:
    """
    Verify webhook signature for payment gateways.
    
    Args:
        payload: Request payload
        signature: Signature from webhook
        secret: Secret key for verification
        
    Returns:
        True if signature is valid, False otherwise
    """
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, signature)


def format_bangladeshi_phone(phone: str) -> str:
    """
    Format phone number to Bangladeshi standard (+880).
    
    Args:
        phone: Phone number string
        
    Returns:
        Formatted phone number
    """
    # Remove all non-digit characters
    phone = ''.join(filter(str.isdigit, phone))
    
    # Remove leading 0 if present
    if phone.startswith('0'):
        phone = phone[1:]
    
    # Remove +880 or 880 if present
    if phone.startswith('880'):
        phone = phone[3:]
    
    # Add +880 prefix
    return f"+880{phone}"

