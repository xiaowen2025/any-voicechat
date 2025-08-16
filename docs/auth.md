# Authentication System

This document provides an overview of the email-based One-Time Password (OTP) authentication system.

## Overview

The authentication system is designed to be simple and secure. It uses a two-step process:

1.  **OTP Request:** The user enters their email address to request an OTP. The backend generates a 6-digit OTP, stores it in the database, and sends it to the user's email address.
2.  **OTP Verification:** The user enters the OTP they received. The backend verifies the OTP against the one stored in the database. If the OTP is valid, the backend generates a JSON Web Token (JWT) and sends it to the client.

The JWT is then used to authenticate subsequent requests to the API.

## API Endpoints

The authentication system exposes the following API endpoints:

### `POST /api/auth/request-otp`

This endpoint is used to request an OTP.

**Request Body:**

```json
{
  "email": "user@example.com"
}
```

**Response:**

```json
{
  "message": "OTP sent to your email."
}
```

### `POST /api/auth/verify-otp`

This endpoint is used to verify an OTP and get a JWT.

**Request Body:**

```json
{
  "email": "user@example.com",
  "otp": "123456"
}
```

**Response:**

```json
{
  "access_token": "your_jwt_token_here",
  "token_type": "bearer"
}
```

## Configuration

The authentication system requires the following environment variable to be set:

-   `JWT_SECRET_KEY`: A long, random, and secret string used to sign the JWTs.

You can set this variable in your `.env` file. See `.env.example` for an example.

## Frontend Integration

The frontend integration consists of two main parts:

-   **`Login.vue` component:** This component provides the user interface for the login process. It has two states: one for entering the email and one for entering the OTP.
-   **`user.js` store:** This Pinia store manages the user's authentication state. It handles the API calls to the backend and stores the user's JWT in local storage.

When the application loads, it checks if a JWT is present in local storage. If a token is found, the user is considered logged in. Otherwise, the user is shown the login page.
