from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import hmac
import hashlib

GITHUB_WEBHOOK_SECRET = "<github_webhook_secret>"


@csrf_exempt
@require_http_methods(["POST"])
def github_webhook(request):
    # Get the request body and headers
    body = request.body
    headers = request.headers

    # Verify the request signature
    signature = headers.get("X-Hub-Signature")
    if not signature:
        return HttpResponse("Invalid signature", status=401)

    # Calculate the expected signature
    expected_signature = hmac.new(
        GITHUB_WEBHOOK_SECRET.encode(), body, hashlib.sha1
    ).hexdigest()

    # Compare the signatures
    if signature != expected_signature:
        return HttpResponse("Invalid signature", status=401)

    # Parse the event data
    event = request.json()

    # Print the event details
    print("Event:", event["event"])
    print("Repository:", event["repository"]["full_name"])
    print("Sender:", event["sender"]["login"])
    print("Payload:", event["payload"])

    return HttpResponse("Webhook received", status=200)
