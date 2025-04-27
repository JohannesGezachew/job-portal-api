# Job Portal API Documentation

## Base URL
https://your-job-api.onrender.com/api/

## Authentication
All endpoints except registration and login require token authentication.
Include the token in the request header:
```
Authorization: Token your_token_here
```

## User Types
The API supports three types of users:
1. `job_seeker` - Can apply to jobs and bookmark jobs
2. `employer` - Can create companies and post jobs
3. `admin` - Has full access to all endpoints

## Endpoints

### Authentication

#### Register a New User
- **URL**: `/accounts/register/`
- **Method**: `POST`
- **Auth Required**: No
- **Data**:
  ```json
  {
    "username": "username",
    "password": "password123",
    "password2": "password123",
    "email": "user@example.com",
    "first_name": "First",
    "last_name": "Last",
    "user_type": "job_seeker"  // or "employer"
  }
  ```
- **Success Response**:
  - **Code**: 201 CREATED
  - **Content**:
    ```json
    {
      "user": {
        "id": 1,
        "username": "username",
        "email": "user@example.com",
        "first_name": "First",
        "last_name": "Last",
        "user_type": "job_seeker"
      },
      "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
    }
    ```

#### Login
- **URL**: `/accounts/login/`
- **Method**: `POST`
- **Auth Required**: No
- **Data**:
  ```json
  {
    "username": "username",
    "password": "password123"
  }
  ```
- **Success Response**:
  - **Code**: 200 OK
  - **Content**:
    ```json
    {
      "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
      "user_id": 1,
      "username": "username",
      "user_type": "job_seeker"
    }
    ```

#### Logout
- **URL**: `/accounts/logout/`
- **Method**: `POST`
- **Auth Required**: Yes
- **Success Response**:
  - **Code**: 200 OK
  - **Content**:
    ```json
    {
      "message": "Successfully logged out."
    }
    ```

#### Get User Profile
- **URL**: `/accounts/profile/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Success Response**:
  - **Code**: 200 OK
  - **Content**:
    ```json
    {
      "id": 1,
      "username": "username",
      "email": "user@example.com",
      "first_name": "First",
      "last_name": "Last",
      "user_type": "job_seeker",
      "phone_number": "+1234567890",
      "bio": "User biography",
      "skills": "Python, Django, JavaScript"
    }
    ```

#### Update User Profile
- **URL**: `/accounts/profile/`
- **Method**: `PUT` or `PATCH`
- **Auth Required**: Yes
- **Data**: Any profile fields to update
- **Success Response**:
  - **Code**: 200 OK
  - **Content**: Updated user profile data

#### Change Password
- **URL**: `/accounts/change-password/`
- **Method**: `PUT`
- **Auth Required**: Yes
- **Data**:
  ```json
  {
    "old_password": "currentpassword",
    "new_password": "newpassword123",
    "new_password2": "newpassword123"
  }
  ```
- **Success Response**:
  - **Code**: 200 OK
  - **Content**:
    ```json
    {
      "message": "Password updated successfully"
    }
    ```

### Companies

#### List Companies
- **URL**: `/companies/`
- **Method**: `GET`
- **Auth Required**: No
- **Query Parameters**:
  - `search`: Search term for name, description or industry
  - `industry`: Filter by industry
  - `location`: Filter by location
  - `ordering`: Order by fields (e.g., `name`, `-created_at`)
  - `page`: Page number for pagination
- **Success Response**:
  - **Code**: 200 OK
  - **Content**: List of companies with pagination

#### Create Company
- **URL**: `/companies/`
- **Method**: `POST`
- **Auth Required**: Yes (must be employer)
- **Data**:
  ```json
  {
    "name": "Company Name",
    "description": "Company description",
    "industry": "Technology",
    "location": "City, Country",
    "website": "https://example.com",
    "founded_year": 2020,
    "size": "50-100 employees"
  }
  ```
- **Success Response**:
  - **Code**: 201 CREATED
  - **Content**: Created company data

#### Get Company Details
- **URL**: `/companies/{id}/`
- **Method**: `GET`
- **Auth Required**: No
- **Success Response**:
  - **Code**: 200 OK
  - **Content**: Company details including job count

#### Update Company
- **URL**: `/companies/{id}/`
- **Method**: `PUT` or `PATCH`
- **Auth Required**: Yes (must be employer and creator)
- **Data**: Fields to update
- **Success Response**:
  - **Code**: 200 OK
  - **Content**: Updated company data

#### Delete Company
- **URL**: `/companies/{id}/`
- **Method**: `DELETE`
- **Auth Required**: Yes (must be employer and creator)
- **Success Response**:
  - **Code**: 204 NO CONTENT

### Jobs

#### List Jobs
- **URL**: `/jobs/`
- **Method**: `GET`
- **Auth Required**: No
- **Query Parameters**:
  - `search`: Search term for title, description or skills
  - `job_type`: Filter by job type (full_time, part_time, etc.)
  - `experience_level`: Filter by experience level
  - `location`: Filter by location
  - `company`: Filter by company ID
  - `ordering`: Order by fields (e.g., `-posted_at`, `salary_min`)
  - `page`: Page number for pagination
- **Success Response**:
  - **Code**: 200 OK
  - **Content**: List of jobs with pagination

#### Create Job
- **URL**: `/jobs/`
- **Method**: `POST`
- **Auth Required**: Yes (must be employer)
- **Data**:
  ```json
  {
    "title": "Job Title",
    "company": 1,
    "description": "Job description",
    "requirements": "Job requirements",
    "responsibilities": "Job responsibilities",
    "location": "City, Country",
    "salary_min": 50000,
    "salary_max": 80000,
    "job_type": "full_time",
    "experience_level": "entry",
    "skills_required": "Required skills",
    "deadline": "2025-12-31T00:00:00Z"
  }
  ```
- **Success Response**:
  - **Code**: 201 CREATED
  - **Content**: Created job data

#### Get Job Details
- **URL**: `/jobs/{id}/`
- **Method**: `GET`
- **Auth Required**: No
- **Success Response**:
  - **Code**: 200 OK
  - **Content**: 
    ```json
    {
      "id": 1,
      "title": "Job Title",
      "company": {
        "id": 1,
        "name": "Company Name",
        "industry": "Technology",
        "location": "City, Country"
      },
      "description": "Job description",
      "requirements": "Job requirements",
      "responsibilities": "Job responsibilities",
      "location": "City, Country",
      "salary_min": 50000,
      "salary_max": 80000,
      "job_type": "full_time",
      "experience_level": "entry",
      "skills_required": "Required skills",
      "is_active": true,
      "posted_at": "2023-01-01T12:00:00Z",
      "deadline": "2025-12-31T00:00:00Z",
      "application_count": 5,
      "is_bookmarked": false,
      "has_applied": false
    }
    ```

#### Update Job
- **URL**: `/jobs/{id}/`
- **Method**: `PUT` or `PATCH`
- **Auth Required**: Yes (must be employer and job poster)
- **Data**: Fields to update
- **Success Response**:
  - **Code**: 200 OK
  - **Content**: Updated job data

#### Delete Job
- **URL**: `/jobs/{id}/`
- **Method**: `DELETE`
- **Auth Required**: Yes (must be employer and job poster)
- **Success Response**:
  - **Code**: 204 NO CONTENT

#### List My Jobs
- **URL**: `/jobs/my-jobs/`
- **Method**: `GET`
- **Auth Required**: Yes (must be employer)
- **Success Response**:
  - **Code**: 200 OK
  - **Content**: List of jobs posted by the current employer

### Job Applications

#### List Applications
- **URL**: `/applications/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Notes**: Returns different results based on user type:
  - Job seekers see their own applications
  - Employers see applications to their jobs
- **Success Response**:
  - **Code**: 200 OK
  - **Content**: List of applications with pagination

#### Apply for a Job
- **URL**: `/applications/`
- **Method**: `POST`
- **Auth Required**: Yes (must be job seeker)
- **Data**:
  ```json
  {
    "job": 1,
    "cover_letter": "Cover letter content"
  }
  ```
- **Success Response**:
  - **Code**: 201 CREATED
  - **Content**: Created application data

#### Get Application Details
- **URL**: `/applications/{id}/`
- **Method**: `GET`
- **Auth Required**: Yes (must be applicant or job poster)
- **Success Response**:
  - **Code**: 200 OK
  - **Content**: Application details

#### Update Application Status
- **URL**: `/applications/{id}/`
- **Method**: `PATCH`
- **Auth Required**: Yes (must be employer and job poster)
- **Data**:
  ```json
  {
    "status": "under_review"  // pending, under_review, shortlisted, rejected, hired
  }
  ```
- **Success Response**:
  - **Code**: 200 OK
  - **Content**: Updated application data

### Bookmarks

#### List Bookmarked Jobs
- **URL**: `/bookmarks/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Success Response**:
  - **Code**: 200 OK
  - **Content**: List of bookmarked jobs with pagination

#### Bookmark a Job
- **URL**: `/bookmarks/`
- **Method**: `POST`
- **Auth Required**: Yes
- **Data**:
  ```json
  {
    "job": 1
  }
  ```
- **Success Response**:
  - **Code**: 201 CREATED
  - **Content**: Created bookmark data

#### Remove a Bookmark
- **URL**: `/bookmarks/{id}/`
- **Method**: `DELETE`
- **Auth Required**: Yes (must be bookmark owner)
- **Success Response**:
  - **Code**: 204 NO CONTENT

#### Toggle Bookmark
- **URL**: `/bookmarks/toggle/{job_id}/`
- **Method**: `POST`
- **Auth Required**: Yes
- **Success Response**:
  - **Code**: 200 OK or 201 CREATED
  - **Content**: 
    ```json
    {
      "status": "Bookmark added"  // or "Bookmark removed"
    }
    ```

## Error Responses

All endpoints return standard HTTP status codes with error messages:

- **400 Bad Request**: Invalid data
- **401 Unauthorized**: Missing or invalid authentication
- **403 Forbidden**: Not allowed to perform action
- **404 Not Found**: Resource not found
- **500 Server Error**: Something went wrong on the server side

Example error response:
```json
{
  "error": "You have already applied for this job"
}
```

## Pagination

All list endpoints return paginated results:

```json
{
  "count": 100,
  "next": "https://your-job-api.onrender.com/api/jobs/?page=2",
  "previous": null,
  "results": [
    // data items
  ]
}
```

To navigate through pages, use the `page` query parameter. 