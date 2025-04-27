# Job Portal API

A Django REST Framework API for a job posting website with features for job seekers and employers.

## Features

- **User Authentication**: Register, login, and manage profiles for job seekers and employers
- **Job Listings**: Full CRUD operations for job postings with detailed information
- **Company Profiles**: Manage company information for employers
- **Job Applications**: Apply to jobs, track application status
- **Bookmarks**: Save jobs for later reference
- **Search & Filtering**: Find jobs by various criteria
- **Admin Panel**: Comprehensive admin interface for site management

## Setup Instructions

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```
   python manage.py migrate
   ```
4. Create a superuser (for admin access):
   ```
   python manage.py createsuperuser
   ```
5. Run the development server:
   ```
   python manage.py runserver
   ```

## API Endpoints

### Authentication

- `POST /api/accounts/register/`: Register a new user
- `POST /api/accounts/login/`: Log in and get authentication token
- `POST /api/accounts/logout/`: Log out (invalidate token)
- `GET /api/accounts/profile/`: Get current user profile
- `PUT /api/accounts/profile/`: Update user profile
- `PUT /api/accounts/change-password/`: Change password

### Companies

- `GET /api/companies/`: List all companies
- `POST /api/companies/`: Create a new company (employers only)
- `GET /api/companies/{id}/`: Get company details
- `PUT /api/companies/{id}/`: Update company (company owner only)
- `DELETE /api/companies/{id}/`: Delete company (company owner only)

### Jobs

- `GET /api/jobs/`: List all active jobs with filters
- `POST /api/jobs/`: Create a new job posting (employers only)
- `GET /api/jobs/{id}/`: Get job details
- `PUT /api/jobs/{id}/`: Update job (job poster only)
- `DELETE /api/jobs/{id}/`: Delete job (job poster only)
- `GET /api/jobs/my-jobs/`: List jobs posted by current employer

### Job Applications

- `GET /api/applications/`: List applications (job seeker: own applications; employer: applications to their jobs)
- `POST /api/applications/`: Apply for a job (job seekers only)
- `GET /api/applications/{id}/`: Get application details
- `PUT /api/applications/{id}/`: Update application status (employers only)

### Bookmarks

- `GET /api/bookmarks/`: List bookmarked jobs
- `POST /api/bookmarks/`: Bookmark a job
- `DELETE /api/bookmarks/{id}/`: Remove a bookmark
- `POST /api/bookmarks/toggle/{job_id}/`: Toggle bookmark status for a job

## Authorization

- Authentication is token-based
- Include the token in the Authorization header:
  ```
  Authorization: Token your_token_here
  ```

## User Types

- **Job Seekers**: Can browse jobs, apply to jobs, manage applications, and bookmark jobs
- **Employers**: Can create company profiles, post jobs, and manage applications to their jobs
- **Admin**: Has access to all features and the admin panel

## Technology Stack

- Django and Django REST Framework
- SQLite (can be configured for other databases)
- Token Authentication
- Django Filters for advanced querying 