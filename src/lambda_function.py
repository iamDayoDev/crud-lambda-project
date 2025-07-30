import json
import os
import boto3
import decimal

TABLE_NAME = os.environ["TABLE_NAME"]
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    """
    Expected routes:
      POST   /items
      GET    /items/{id}
      PUT    /items/{id}
      DELETE /items/{id}
    """
    method = event.get("httpMethod")
    path = event.get("path", "")
    path_params = event.get("pathParameters") or {}
    body = {}

    if event.get("body"):
        try:
            body = json.loads(event["body"])
        except Exception:
            body = {}

    if path.startswith("/items"):
        if method == "POST":
            return create_item(body)
        elif method == "GET":
            item_id = path_params.get("id")
            return get_item(item_id)
        elif method == "PUT":
            item_id = path_params.get("id")
            return update_item(item_id, body)
        elif method == "DELETE":
            item_id = path_params.get("id")
            return delete_item(item_id)

    return respond(404, {"message": "Not Found"})


def create_item(item):
    if "id" not in item:
        return respond(400, {"error": "id is required"})
    try:
        table.put_item(Item=item)
        return respond(201, {"message": "Item created", "item": item})
    except Exception as e:
        return respond(500, {"error": str(e)})


def get_item(item_id):
    if not item_id:
        return respond(400, {"error": "id path parameter is required"})
    try:
        res = table.get_item(Key={"id": item_id})
        return respond(200, res.get("Item", {}))
    except Exception as e:
        return respond(500, {"error": str(e)})


def update_item(item_id, item):
    if not item_id:
        return respond(400, {"error": "id path parameter is required"})
    item["id"] = item_id
    try:
        table.put_item(Item=item)
        return respond(200, {"message": "Item updated", "item": item})
    except Exception as e:
        return respond(500, {"error": str(e)})


def delete_item(item_id):
    if not item_id:
        return respond(400, {"error": "id path parameter is required"})
    try:
        table.delete_item(Key={"id": item_id})
        return respond(200, {"message": "Item deleted"})
    except Exception as e:
        return respond(500, {"error": str(e)})


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def respond(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
        },
        "body": json.dumps(body, cls=DecimalEncoder),
    }
