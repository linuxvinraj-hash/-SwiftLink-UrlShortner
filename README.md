# -SwiftLink-UrlShortner

# URL Shortener (AWS Serverless)

## 🚀 Overview
A serverless URL shortener built using AWS Lambda, API Gateway, DynamoDB, and S3.

## 🏗 Architecture
- S3 (Frontend)
- API Gateway
- Lambda
- DynamoDB

- <img width="838" height="451" alt="image" src="https://github.com/user-attachments/assets/aa56afea-9f83-4d68-9bb1-ddfdba42bded" />


## 🔗 API Endpoints
https://dphkf5s57d.execute-api.ap-southeast-2.amazonaws.com

### Create Short Link
POST /links

### Get All Links
GET /admin/links

### Redirect
GET /{shortCode}

## DynamoDB Schema
Table Name: ShortLinksTable

Primary Key:
- shortCode (String)

Attributes:
- target_url (String)
- click_count (Number)
- created_at (String)

## ⚙️ Setup
1. Deploy Lambda
2. Connect API Gateway
3. Create DynamoDB table
4. Upload frontend to S3



## 🌐 Live Demo
ShortnerUrl - https://url-short-cut.s3.ap-southeast-2.amazonaws.com/Index1.html
Admin AnalyticsUrl - https://url-short-cut.s3.ap-southeast-2.amazonaws.com/admin1.html

