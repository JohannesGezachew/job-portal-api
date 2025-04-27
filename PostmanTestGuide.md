# Job Portal API - Postman Testing Guide

## Important Notes
1. Your API is deployed at: https://job-portal-api-cx5r.onrender.com
2. The free tier on Render goes to sleep after inactivity - **the first request may take 50+ seconds** to wake up the service
3. Most endpoints require authentication with a token

## Test 1: Basic API Connection
First, let's check if the API is accessible at all:

**Request**:
- Method: GET
- URL: https://job-portal-api-cx5r.onrender.com/

**Expected Response**: 
```json
{
  "message": "Welcome to Job Portal API",
  "endpoints": {
    "admin": "/admin/",
    "api": "/api/",
    "accounts": "/api/accounts/",
    "companies": "/api/companies/",
    "jobs": "/api/jobs/",
    "test": "/api-test/"
  }
}
```

## Test 2: Test Endpoint (No Authentication Required)
**Request**:
- Method: GET
- URL: https://job-portal-api-cx5r.onrender.com/api-test/

**Expected Response**:
```json
{
  "message": "API is working correctly",
  "method": "GET",
  "data_received": null
}
```

## Test 3: Create a User Account
**Request**:
- Method: POST
- URL: https://job-portal-api-cx5r.onrender.com/api/accounts/register/
- Headers:
  - Content-Type: application/json
- Body (raw JSON):
```json
{
  "username": "testuser",
  "password": "TestPassword123",
  "password2": "TestPassword123",
  "email": "test@example.com",
  "first_name": "Test",
  "last_name": "User",
  "user_type": "job_seeker"
}
```

**Expected Response**:
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "user_type": "job_seeker"
  },
  "token": "your_token_value_here"
}
```

## Test 4: Login
**Request**:
- Method: POST
- URL: https://job-portal-api-cx5r.onrender.com/api/accounts/login/
- Headers:
  - Content-Type: application/json
- Body (raw JSON):
```json
{
  "username": "testuser",
  "password": "TestPassword123"
}
```

**Expected Response**:
```json
{
  "token": "your_token_value_here",
  "user_id": 1,
  "username": "testuser",
  "user_type": "job_seeker"
}
```

## Test 5: Validate Your Token
**Request**:
- Method: GET
- URL: https://job-portal-api-cx5r.onrender.com/token-test/
- Headers:
  - Authorization: Token your_token_value_here

**Expected Response**:
```json
{
  "message": "Token is valid",
  "user_id": 1,
  "username": "testuser",
  "user_type": "job_seeker"
}
```

## Test 6: Get User Profile (Authenticated Request)
**Request**:
- Method: GET
- URL: https://job-portal-api-cx5r.onrender.com/api/accounts/profile/
- Headers:
  - Authorization: Token your_token_value_here

**Expected Response**:
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "first_name": "Test",
  "last_name": "User",
  "user_type": "job_seeker"
}
```

## Common Issues & Troubleshooting

### 1. Request Timeout
**Problem**: Request takes too long and times out
**Solution**: The free tier on Render goes to sleep after inactivity. The first request can take 50+ seconds to wake up the service. Wait and try again.

### 2. Authentication Issues
**Problem**: Getting 401 Unauthorized errors
**Solution**: 
- Make sure you're using the correct token format: `Token your_token_here` (with a space after "Token")
- Ensure your token is valid and not expired
- Try logging in again to get a fresh token
- Use the /token-test/ endpoint to validate your token

### 3. CORS Issues
**Problem**: Getting CORS-related errors
**Solution**:
- We've enabled all CORS origins for testing
- If using a browser-based tool, try Postman desktop application instead

### 4. Wrong HTTP Method
**Problem**: Getting 405 Method Not Allowed
**Solution**: Verify you're using the correct HTTP method (GET, POST, etc.) for each endpoint

### 5. Validation Errors
**Problem**: Getting 400 Bad Request with validation errors
**Solution**: Check the response body for specific validation errors and fix your request data

### 6. Free Tier Limitations
**Problem**: Your API seems to work intermittently
**Solution**: 
- The free tier on Render has limitations and your service may spin down during periods of inactivity
- It may take up to a minute for the first request to wake up the service
- Consider upgrading to a paid plan for production use 