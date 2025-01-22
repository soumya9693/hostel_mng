# Hostel Management System (HMS)
A comprehensive hostel management system built with Django REST Framework featuring user authentication and complaint management.

## Backend Setup

### Prerequisites
- Python 3.8+
- Django 3.2+
- Django REST Framework
- Simple JWT
- Google Auth Library

### Installation
1. Clone the repository
```bash
git clone 
E
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
Create a `keyconfig.py` file in the project root/HMS and add:
```
GOOGLE_OAUTH2_CLIENT_ID=your_google_client_id
```

5. Run migrations
```bash
python manage.py migrate
```

6. Start the development server
```bash
python manage.py runserver
```

## API Documentation

### Authentication Endpoints

#### 1. User Registration
- **URL**: `/api/auth/register/`
- **Method**: `POST`
- **Request Body**:
```json
{
    "email": "user@example.com",
    "password": "strong_password",
    "password2": "strong_password",
    "first_name": "John",
    "last_name": "Doe"
}
```
- **Success Response**: `201 Created`
```json
{
    "user": {
        "id": 1,
        "email": "user@example.com",
        "user_type": "STUDENT",
        "first_name": "John",
        "last_name": "Doe"
    },
    "tokens": {
        "refresh": "refresh_token",
        "access": "access_token"
    }
}
``` 

#### 2. User Login
- **URL**: `/api/auth/login/`
- **Method**: `POST`
- **Request Body**:
```json
{
    "email": "user@example.com",
    "password": "your_password"
}
```
- **Success Response**: `200 OK`
```json
{
    "user": {
        "id": 1,
        "email": "user@example.com",
        "user_type": "STUDENT"
    },
    "tokens": {
        "refresh": "refresh_token",
        "access": "access_token"
    }
}
```

#### 3. Google OAuth2 Login
- **URL**: `/api/auth/google/login/`
- **Method**: `POST`
- **Request Body**:c
```json
{
    "token": "google_id_token"
}
```
- **Success Response**: `200 OK`
```json
{
    "user": {
        "id": 1,
        "email": "user@example.com",
        "user_type": "STUDENT"
    },
    "tokens": {
        "refresh": "refresh_token",
        "access": "access_token"
    }
}
```

#### 4. Token Refresh
- **URL**: `/api/auth/token/refresh/`
- **Method**: `POST`
- **Request Body**:
```json
{
    "refresh": "your_refresh_token"
}
```
- **Success Response**: `200 OK`
```json
{
    "access": "new_access_token"
}
```

## User Types and Permissions
The system supports four user types with different permission levels:
- **SUPERINTENDENT**: Highest level of access
- **ESTATE_MANAGER**: Management level access
- **WARDEN**: Supervisor level access
- **STUDENT**: Basic user access


### Complaint Management System

#### Student Endpoints

1. **Create Complaint**
- **URL**: `/api/complaints/create/`
- **Method**: `POST`
- **Permission**: Student only
- **Request Body**:
```json
{
    "block": "0",
    "floor": "1",
    "room_number": "101",
    "toilet": "T1",
    "request_related": "Carpenter",
    "subcategory": "Door",
    "complaint_description": "Door hinge is broken"
}
```
- **Success Response**: `201 Created`
```json
{
    "message": "Complaint submitted successfully",
    "complaint_data": {
        "id": 1,
        "user": 1,
        "block": "0",
        "floor": "1",
        "room_number": "101",
        "toilet": "T1",
        "request_related": "Carpenter",
        "subcategory": "Door",
        "complaint_description": "Door hinge is broken",
        "complaint_status": "Pending",
        "reported_at": "2024-01-01T10:00:00Z"
    }
}
```

2. **List Active Complaints**
- **URL**: `/api/complaints/student/active/`
- **Method**: `GET`
- **Permission**: Student only
- **Description**: Lists all active complaints (Pending, Approved) for the current student

3. **List Previous Complaints**
- **URL**: `/api/complaints/student/previous/`
- **Method**: `GET`
- **Permission**: Student only
- **Description**: Lists all resolved complaints for the current student

#### Superintendent Endpoints

1. **Update Complaint Status**
- **URL**: `/api/complaints/supri/update-status/`
- **Method**: `PUT`
- **Permission**: Superintendent only
- **Request Body**:
```json
{
    "complaint_id": 1,
    "new_status": "Approved",
    "send_to_ems": true
}
```

2. **List All Active Complaints**
- **URL**: `/api/complaints/supri/active/`
- **Method**: `GET`
- **Permission**: Superintendent only

3. **List All Previous Complaints**
- **URL**: `/api/complaints/supri/previous/`
- **Method**: `GET`
- **Permission**: Superintendent only
- **Description**: Includes detailed statistics and analysis

#### Warden Endpoints

1. **List All Complaints**
- **URL**: `/api/complaints/warden/all/`
- **Method**: `GET`
- **Permission**: Warden only
- **Description**: Lists all complaints without showing status

#### Estate Manager Endpoints

1. **View EMS Complaints**
- **URL**: `/api/complaints/estate-manager/complaints/`
- **Method**: `GET`
- **Permission**: Estate Manager only
- **Description**: Lists complaints marked for EMS attention

2. **Get Complaint Receipt**
- **URL**: `/api/complaints/estate-manager/complaints/receipt/<serial_number>/`
- **Method**: `GET`
- **Permission**: Estate Manager only

#### General Endpoints

1. **Resolve Complaint**
- **URL**: `/api/complaints/resolve/<complaint_id>/`
- **Method**: `PUT`
- **Permission**: Any authenticated user
- **Description**: Marks a complaint as resolved


### for more apis chekcout postman 
[Postman Handover Link](https://documenter.getpostman.com/view/33149114/2sAY4xAMny)



## Status Flow
```
Student Creates Complaint
        ↓
    [Pending]
        ↓
Superintendent Review
        ↓
    [Approved]
        ↓
Optional: Send to EMS
        ↓
    [Resolved]
```


## Security Considerations
1. Always use HTTPS in production
2. Implement rate limiting for authentication endpoints
3. Set secure and HTTP-only flags for cookies
4. Implement CORS properly
5. Regular token rotation
6. Validate Google tokens on the backend

## Error Handling
The API returns standard HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

