import json
import boto3
import string
import random
from decimal import Decimal
from datetime import datetime

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ShortLinksTable')


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,DELETE,OPTIONS",  # Added DELETE
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps(body, default=decimal_default)
    }


def lambda_handler(event, context):
    method = event.get('requestContext', {}).get('http', {}).get('method')
    path = event.get('rawPath', '/')

    # OPTIONS — CORS preflight (needed for DELETE from browser)
    if method == "OPTIONS":
        return response(200, {})

    # POST /links — Create a new short link
    if method == "POST" and path == "/links":
        try:
            body = json.loads(event.get('body', '{}'))
            target_url = body.get('target_url')
            if not target_url:
                return response(400, {"error": "target_url is required"})

            short_code = generate_code()
            table.put_item(Item={
                'shortCode': short_code,
                'target_url': target_url,
                'click_count': 0,
                'created_at': datetime.utcnow().isoformat()
            })
            return response(201, {"shortCode": short_code})
        except Exception as e:
            return response(500, {"error": str(e)})

    # GET /admin/links — List all links
    elif method == "GET" and path == "/admin/links":
        try:
            items = table.scan().get('Items', [])
            return response(200, items)
        except Exception as e:
            return response(500, {"error": str(e)})

    # DELETE /admin/links/{code} — Delete a short link
    elif method == "DELETE" and path.startswith("/admin/links/"):
        short_code = path.split("/")[-1]
        try:
            table.delete_item(Key={'shortCode': short_code})
            return response(200, {"message": f"Deleted {short_code}"})
        except Exception as e:
            return response(500, {"error": str(e)})

    # GET /{code} — Redirect to target URL
    elif method == "GET":
        short_code = path.strip("/")
        try:
            res = table.get_item(Key={'shortCode': short_code})
            item = res.get('Item')
            if item:
                table.update_item(
                    Key={'shortCode': short_code},
                    UpdateExpression="ADD click_count :inc",
                    ExpressionAttributeValues={':inc': 1}
                )
                return {
                    "statusCode": 301,
                    "headers": {"Location": item['target_url']}
                }
            return response(404, {"error": "Link not found"})
        except Exception as e:
            return response(500, {"error": str(e)})

    return response(404, {"error": "Not Found"})
