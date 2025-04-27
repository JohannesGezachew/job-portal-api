# Frontend Integration Guide for Job Portal API

This guide provides code examples for integrating your frontend application with our Job Portal API.

## Authentication

### User Registration

```javascript
// Register a new user
async function registerUser(userData) {
  try {
    const response = await fetch('https://your-job-api.onrender.com/api/accounts/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: userData.username,
        password: userData.password,
        password2: userData.password,
        email: userData.email,
        first_name: userData.firstName,
        last_name: userData.lastName,
        user_type: userData.userType // 'job_seeker' or 'employer'
      }),
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(JSON.stringify(errorData));
    }
    
    const data = await response.json();
    // Store the token in localStorage or a secure state management solution
    localStorage.setItem('authToken', data.token);
    localStorage.setItem('userType', data.user.user_type);
    
    return data;
  } catch (error) {
    console.error('Registration error:', error);
    throw error;
  }
}
```

### User Login

```javascript
// User login
async function loginUser(username, password) {
  try {
    const response = await fetch('https://your-job-api.onrender.com/api/accounts/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username,
        password
      }),
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(JSON.stringify(errorData));
    }
    
    const data = await response.json();
    // Store the token
    localStorage.setItem('authToken', data.token);
    localStorage.setItem('userType', data.user_type);
    
    return data;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
}
```

### User Logout

```javascript
// Logout user
async function logoutUser() {
  try {
    const token = localStorage.getItem('authToken');
    
    const response = await fetch('https://your-job-api.onrender.com/api/accounts/logout/', {
      method: 'POST',
      headers: {
        'Authorization': `Token ${token}`,
      },
    });
    
    // Clear local storage regardless of response
    localStorage.removeItem('authToken');
    localStorage.removeItem('userType');
    
    return response.ok;
  } catch (error) {
    console.error('Logout error:', error);
    // Still clear local storage on error
    localStorage.removeItem('authToken');
    localStorage.removeItem('userType');
    throw error;
  }
}
```

### Authenticated API Request Helper

```javascript
// Helper function for authenticated requests
async function apiRequest(url, method = 'GET', data = null) {
  try {
    const token = localStorage.getItem('authToken');
    const headers = {
      'Content-Type': 'application/json',
    };
    
    if (token) {
      headers['Authorization'] = `Token ${token}`;
    }
    
    const options = {
      method,
      headers,
    };
    
    if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
      options.body = JSON.stringify(data);
    }
    
    const response = await fetch(`https://your-job-api.onrender.com/api${url}`, options);
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(JSON.stringify(errorData));
    }
    
    // For DELETE requests, there might not be any response body
    if (method === 'DELETE') {
      return { success: true };
    }
    
    return await response.json();
  } catch (error) {
    console.error(`API ${method} request error:`, error);
    throw error;
  }
}
```

## User Profile Management

### Get Current User Profile

```javascript
// Get user profile
async function getUserProfile() {
  return apiRequest('/accounts/profile/');
}
```

### Update User Profile

```javascript
// Update user profile
async function updateUserProfile(profileData) {
  return apiRequest('/accounts/profile/', 'PATCH', profileData);
}
```

### Change Password

```javascript
// Change password
async function changePassword(oldPassword, newPassword) {
  return apiRequest('/accounts/change-password/', 'PUT', {
    old_password: oldPassword,
    new_password: newPassword,
    new_password2: newPassword
  });
}
```

## Companies Management

### Get Companies

```javascript
// Get list of companies with optional filters
async function getCompanies(filters = {}) {
  const queryParams = new URLSearchParams();
  
  if (filters.search) queryParams.append('search', filters.search);
  if (filters.industry) queryParams.append('industry', filters.industry);
  if (filters.location) queryParams.append('location', filters.location);
  if (filters.ordering) queryParams.append('ordering', filters.ordering);
  if (filters.page) queryParams.append('page', filters.page);
  
  const queryString = queryParams.toString() ? `?${queryParams.toString()}` : '';
  return apiRequest(`/companies/${queryString}`);
}
```

### Create Company (for employers)

```javascript
// Create a new company
async function createCompany(companyData) {
  return apiRequest('/companies/', 'POST', companyData);
}
```

### Get Company Details

```javascript
// Get company details
async function getCompanyDetails(companyId) {
  return apiRequest(`/companies/${companyId}/`);
}
```

### Update Company

```javascript
// Update company details
async function updateCompany(companyId, companyData) {
  return apiRequest(`/companies/${companyId}/`, 'PATCH', companyData);
}
```

## Jobs Management

### Get Jobs

```javascript
// Get jobs with filters
async function getJobs(filters = {}) {
  const queryParams = new URLSearchParams();
  
  if (filters.search) queryParams.append('search', filters.search);
  if (filters.job_type) queryParams.append('job_type', filters.job_type);
  if (filters.experience_level) queryParams.append('experience_level', filters.experience_level);
  if (filters.location) queryParams.append('location', filters.location);
  if (filters.company) queryParams.append('company', filters.company);
  if (filters.ordering) queryParams.append('ordering', filters.ordering);
  if (filters.page) queryParams.append('page', filters.page);
  
  const queryString = queryParams.toString() ? `?${queryParams.toString()}` : '';
  return apiRequest(`/jobs/${queryString}`);
}
```

### Create Job (for employers)

```javascript
// Create a new job posting
async function createJob(jobData) {
  return apiRequest('/jobs/', 'POST', jobData);
}
```

### Get Job Details

```javascript
// Get job details
async function getJobDetails(jobId) {
  return apiRequest(`/jobs/${jobId}/`);
}
```

### Get My Jobs (for employers)

```javascript
// Get jobs posted by the current employer
async function getMyJobs() {
  return apiRequest('/jobs/my-jobs/');
}
```

## Job Applications

### Apply for a Job (for job seekers)

```javascript
// Apply for a job
async function applyForJob(jobId, coverLetter, resume) {
  // For file uploads, use FormData
  if (resume) {
    const formData = new FormData();
    formData.append('job', jobId);
    formData.append('cover_letter', coverLetter);
    formData.append('resume', resume);
    
    const token = localStorage.getItem('authToken');
    
    // Special handling for FormData uploads
    const response = await fetch('https://your-job-api.onrender.com/api/applications/', {
      method: 'POST',
      headers: {
        'Authorization': `Token ${token}`,
      },
      body: formData
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(JSON.stringify(errorData));
    }
    
    return await response.json();
  } else {
    // Regular JSON request without file upload
    return apiRequest('/applications/', 'POST', {
      job: jobId,
      cover_letter: coverLetter
    });
  }
}
```

### Get Applications

```javascript
// Get applications 
// (job seekers see their applications, employers see applications to their jobs)
async function getApplications() {
  return apiRequest('/applications/');
}
```

### Update Application Status (for employers)

```javascript
// Update application status
async function updateApplicationStatus(applicationId, status) {
  return apiRequest(`/applications/${applicationId}/`, 'PATCH', {
    status
  });
}
```

## Bookmarks

### Get Bookmarked Jobs

```javascript
// Get bookmarked jobs
async function getBookmarkedJobs() {
  return apiRequest('/bookmarks/');
}
```

### Toggle Bookmark

```javascript
// Toggle bookmark for a job
async function toggleJobBookmark(jobId) {
  return apiRequest(`/bookmarks/toggle/${jobId}/`, 'POST');
}
```

## Example React Component

Here's an example of a React component that displays a list of jobs with a search feature:

```jsx
import React, { useState, useEffect } from 'react';

function JobsList() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    job_type: '',
    location: '',
    page: 1
  });

  useEffect(() => {
    // Function to fetch jobs
    async function fetchJobs() {
      try {
        setLoading(true);
        const response = await apiRequest(`/jobs/?search=${searchTerm}&job_type=${filters.job_type}&location=${filters.location}&page=${filters.page}`);
        setJobs(response);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch jobs');
        setLoading(false);
        console.error(err);
      }
    }

    fetchJobs();
  }, [searchTerm, filters]);

  const handleSearch = (e) => {
    e.preventDefault();
    // Reset to page 1 when searching
    setFilters(prev => ({ ...prev, page: 1 }));
  };

  const handleBookmark = async (jobId) => {
    try {
      const result = await toggleJobBookmark(jobId);
      // Update the job in the list to reflect bookmark status
      setJobs(prev => {
        const updated = { ...prev };
        updated.results = prev.results.map(job => 
          job.id === jobId 
            ? { ...job, is_bookmarked: !job.is_bookmarked }
            : job
        );
        return updated;
      });
    } catch (err) {
      console.error('Failed to toggle bookmark', err);
    }
  };

  return (
    <div className="jobs-list">
      <h1>Available Jobs</h1>
      
      <form onSubmit={handleSearch}>
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search jobs..."
        />
        
        <select 
          value={filters.job_type}
          onChange={(e) => setFilters(prev => ({ ...prev, job_type: e.target.value }))}
        >
          <option value="">All Job Types</option>
          <option value="full_time">Full Time</option>
          <option value="part_time">Part Time</option>
          <option value="contract">Contract</option>
          <option value="freelance">Freelance</option>
          <option value="internship">Internship</option>
        </select>
        
        <input
          type="text"
          value={filters.location}
          onChange={(e) => setFilters(prev => ({ ...prev, location: e.target.value }))}
          placeholder="Location"
        />
        
        <button type="submit">Search</button>
      </form>
      
      {loading ? (
        <p>Loading jobs...</p>
      ) : error ? (
        <p className="error">{error}</p>
      ) : (
        <div className="jobs-grid">
          {jobs.results && jobs.results.length > 0 ? (
            jobs.results.map(job => (
              <div key={job.id} className="job-card">
                <h2>{job.title}</h2>
                <h3>{job.company_name}</h3>
                <p><strong>Location:</strong> {job.location}</p>
                <p><strong>Type:</strong> {job.job_type.replace('_', ' ').toUpperCase()}</p>
                <p><strong>Salary:</strong> ${job.salary_min} - ${job.salary_max}</p>
                <div className="job-actions">
                  <button onClick={() => handleBookmark(job.id)}>
                    {job.is_bookmarked ? 'Unbookmark' : 'Bookmark'}
                  </button>
                  <button onClick={() => window.location.href = `/jobs/${job.id}`}>
                    View Details
                  </button>
                </div>
              </div>
            ))
          ) : (
            <p>No jobs found matching your criteria.</p>
          )}
        </div>
      )}
      
      {jobs.count > 0 && (
        <div className="pagination">
          <button 
            disabled={!jobs.previous} 
            onClick={() => setFilters(prev => ({ ...prev, page: prev.page - 1 }))}
          >
            Previous
          </button>
          <span>Page {filters.page} of {Math.ceil(jobs.count / 10)}</span>
          <button 
            disabled={!jobs.next} 
            onClick={() => setFilters(prev => ({ ...prev, page: prev.page + 1 }))}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}

export default JobsList;
```

## Error Handling

```javascript
// Standardized error handling
function handleApiError(error) {
  try {
    // Try to parse the error message as JSON
    const errorData = JSON.parse(error.message);
    
    // Check for different types of error responses
    if (typeof errorData === 'object') {
      // Handle validation errors (field-specific errors)
      if (Object.keys(errorData).length > 0) {
        const firstError = Object.entries(errorData)[0];
        return {
          field: firstError[0],
          message: Array.isArray(firstError[1]) ? firstError[1][0] : firstError[1]
        };
      }
    }
    
    // Handle generic error message
    return {
      field: null,
      message: errorData.error || errorData.detail || 'An unexpected error occurred'
    };
  } catch (e) {
    // If JSON parsing fails, return the raw error message
    return {
      field: null,
      message: error.message || 'An unexpected error occurred'
    };
  }
}
```

This guide provides the core functionality needed to integrate with the Job Portal API. Customize these examples based on your frontend framework and specific requirements. 