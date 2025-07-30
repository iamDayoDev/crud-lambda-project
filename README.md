# 🗄️ Serverless CRUD API with AWS Lambda, API Gateway,DynamoDB & AWS Amplify (Frontend)

A beginner-friendly, **ClickOps-first** project that builds a CRUD API backed by DynamoDB using:
- **AWS Lambda** (Python)
- **Amazon API Gateway (REST API)**
- **Amazon DynamoDB**

You’ll deploy the infrastructure **manually in the AWS Console**

---

## 📚 What You’ll Build

**Endpoints (suggested mapping):**

| Method | Path            | Description        |
|--------|-----------------|--------------------|
| POST   | /items          | Create an item     |
| GET    | /items/{id}     | Get an item        |
| PUT    | /items/{id}     | Update an item     |
| DELETE | /items/{id}     | Delete an item     |

**DynamoDB Table**

- Table name: `ItemsTable` (you choose)
- **Partition key**: `id` (String)

---

## 🛠️ Prerequisites

- AWS Account
- IAM user with permissions for Lambda, API Gateway, DynamoDB
- GitHub repository

---

## 🖱️ Step-by-Step (ClickOps)

### 1) Create the DynamoDB table
1. **DynamoDB > Tables > Create table**
2. Table name: `ItemsTable`
3. Partition key: `id` (String)
4. Create

### 2) Create the Lambda function
1. **Lambda > Create function**
2. Author from scratch, Runtime **Python 3.11 (or 3.10/3.9)**
3. Function name: `crud-handler`
4. Create the function
5. In **Configuration > Environment variables**, add:
   - `TABLE_NAME = ItemsTable`
6. Give the Lambda **IAM role** permission to access DynamoDB (attach AWS managed policy: `AmazonDynamoDBFullAccess` for simplicity, or a tighter policy you craft).

### 3) Wire API Gateway to Lambda
1. **API Gateway > Create API > REST API**
2. Add routes:
   - `POST /items` → Lambda integration (`crud-handler`)
   - `GET /items/{id}` → Lambda integration
   - `PUT /items/{id}` → Lambda integration
   - `DELETE /items/{id}` → Lambda integration
3. **Deploy** the API and copy the invoke URL.

### 4) (Optional) Enable CORS
- In API Gateway, turn on CORS for your routes if you’ll call them from a browser/frontend.


---

## 🧪 Test with curl

```bash
# CREATE
curl -X POST "$API_URL/items"   -H "Content-Type: application/json"   -d '{"id":"123","name":"Book","price":25.5}'

# READ
curl "$API_URL/items/123"

# UPDATE
curl -X PUT "$API_URL/items/123"   -H "Content-Type: application/json"   -d '{"id":"123","name":"Book - 2nd Edition","price":35.0}'

# DELETE
curl -X DELETE "$API_URL/items/123"
```

---

# Project2-Serverless-CRUD-API-Lambda-Dynamodb-Amplify
