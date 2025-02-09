import os
import time
import requests
import json
from dotenv import load_dotenv

load_dotenv()

shipping_company_api = os.getenv("Shipping_company_api")
Shipping_company_url = os.getenv("Shipping_company_url_for_success")
Shipping_company_url_for_failure = os.getenv("Shipping_company_url_for_failure")

CLIENT_ID = os.getenv("Paypal_Client_ID")
CLIENT_SECRET = os.getenv("Paypal_Client_Secret")
API_BASE = os.getenv("Paypal_API_BASE")


def send_product_details_to_shipping_company(product, buyer_email, seller_email):
    url = Shipping_company_url
    print(API_BASE)
    headers = {
        "Content-Type": "application/json",
        "Authorization": shipping_company_api,
    }
    data = {
        "buyer_email": buyer_email,
        "seller_email": seller_email,
        "product_details": product,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_data = response.json()
    return (
        response.status_code,
        response_data.get("status"),
        response_data.get("shipping_response"),
    )


def get_access_token():
    url = f"{API_BASE}/v1/oauth2/token"
    headers = {"Accept": "application/json", "Accept-Language": "en_US"}
    data = {"grant_type": "client_credentials"}
    response = requests.post(
        url, headers=headers, data=data, auth=(CLIENT_ID, CLIENT_SECRET)
    )
    response_data = response.json()
    if "access_token" in response_data:
        return response_data["access_token"]
    else:
        raise Exception(f"Failed to get access token: {response_data}")


def send_payout(recipient_email, amount, currency="USD"):
    access_token = get_access_token()
    url = f"{API_BASE}/v1/payments/payouts"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    payload = {
        "sender_batch_header": {
            "email_subject": "You have a payment!",
            "sender_batch_id": f"batch_{int(time.time())}",
        },
        "items": [
            {
                "recipient_type": "EMAIL",
                "amount": {
                    "value": f"{float(amount):.2f}",
                    "currency": currency,
                },
                "receiver": recipient_email,
                "note": "Thank you for your service!",
                "sender_item_id": f"item_{int(time.time())}",
            }
        ],
    }
    print(payload)
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()
