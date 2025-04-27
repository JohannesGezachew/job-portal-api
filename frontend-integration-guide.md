# Job Portal API - Frontend Integration Guide

## API Overview
The Job Portal API provides all the backend functionality needed for a complete job portal website. This guide will help you integrate the frontend with our RESTful API service.

## Base URL
```
https://job-portal-api-cx5r.onrender.com
```

## Important Notes
- The API is hosted on Render's free tier which sleeps after inactivity
- First request after inactivity might take 50+ seconds to process
- All authenticated requests require a token in the header

## Authentication Flow

### 1. User Registration
Users must first register before using most of the API features:

```javascript
async function registerUser(userData) {
  try {
    const response = await fetch('https://job-portal-api-cx5r.onrender.com/api/accounts/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || JSON.stringify(data));
    }
    
    // Save token after successful registration
    localStorage.setItem('token', data.token);
    localStorage.setItem('user', JSON.stringify(data.user));
    
    return data;
  } catch (error) {
    console.error('Registration failed:', error);
    throw error;
  }
}

// Example usage:
const userData = {
  username: 'newuser',
  password: 'SecurePassword123',
  password2: 'SecurePassword123',
  email: 'user@example.com',
  first_name: 'First',
  last_name: 'Last',
  user_type: 'job_seeker' // or 'employer'
};

// Call the registration function
registerUser(userData)
  .then(data => console.log('Registration successful:', data))
  .catch(error => console.error('Registration error:', error));
```

### 2. User Login
For existing users, use the login endpoint:

```javascript
async function loginUser(credentials) {
  try {
    const response = await fetch('https://job-portal-api-cx5r.onrender.com/api/accounts/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Login failed');
    }
    
    // Save authentication data
    localStorage.setItem('token', data.token);
    localStorage.setItem('userId', data.user_id);
    localStorage.setItem('username', data.username);
    localStorage.setItem('userType', data.user_type);
    
    return data;
  } catch (error) {
    console.error('Login failed:', error);
    throw error;
  }
}

// Example usage:
const credentials = {
  username: 'existinguser',
  password: 'YourPassword123'
};

loginUser(credentials)
  .then(data => console.log('Login successful:', data))
  .catch(error => console.error('Login error:', error));
```

### 3. Making Authenticated Requests
After login/registration, include the token in all subsequent requests:

```javascript
// Helper function for authenticated API requests
async function apiRequest(endpoint, method = 'GET', data = null) {
  const token = localStorage.getItem('token');
  
  if (!token) {
    throw new Error('Authentication required. Please log in.');
  }
  
  const options = {
    method,
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json',
    },
  };
  
  if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
    options.body = JSON.stringify(data);
  }
  
  try {
    const response = await fetch(`https://job-portal-api-cx5r.onrender.com${endpoint}`, options);
    
    // Handle 204 No Content response
    if (response.status === 204) {
      return { success: true };
    }
    
    const responseData = await response.json();
    
    if (!response.ok) {
      throw new Error(responseData.error || JSON.stringify(responseData));
    }
    
    return responseData;
  } catch (error) {
    console.error(`API request to ${endpoint} failed:`, error);
    throw error;
  }
}

// Example usage:
// Get user profile
apiRequest('/api/accounts/profile/')
  .then(data => console.log('User profile:', data))
  .catch(error => console.error('Error fetching profile:', error));

// Create a job posting (for employers)
const newJob = {
  title: 'Frontend Developer',
  company: 1, // company ID
  description: 'We are looking for a skilled frontend developer...',
  requirements: 'React, JavaScript, CSS',
  responsibilities: 'Developing user interfaces, implementing features',
  location: 'Remote',
  salary_min: 60000,
  salary_max: 80000,
  job_type: 'full_time',
  experience_level: 'mid',
  skills_required: 'React, JavaScript, Redux, CSS',
  deadline: '2025-12-31T00:00:00Z'
};

apiRequest('/api/jobs/', 'POST', newJob)
  .then(data => console.log('Job created:', data))
  .catch(error => console.error('Error creating job:', error));
```

### 4. Handling Logout
To log a user out, call the logout endpoint and clear local storage:

```javascript
async function logoutUser() {
  try {
    await apiRequest('/api/accounts/logout/', 'POST');
    
    // Clear all authentication data
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    localStorage.removeItem('username');
    localStorage.removeItem('userType');
    
    return { success: true, message: 'Logged out successfully' };
  } catch (error) {
    console.error('Logout failed:', error);
    // Still clear local storage even if the API call fails
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    localStorage.removeItem('username');
    localStorage.removeItem('userType');
    throw error;
  }
}
```

## React Integration Example

Here's a more complete example using React hooks:

```jsx
import React, { useState, useEffect, createContext, useContext } from 'react';

// Create auth context for state management
const AuthContext = createContext();

// Auth provider component
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Check if user is logged in on initial load
  useEffect(() => {
    const checkAuthStatus = async () => {
      if (token) {
        try {
          const userData = await fetchUserProfile();
          setUser(userData);
        } catch (err) {
          // Token might be invalid, clear it
          console.error('Auth verification failed:', err);
          localStorage.removeItem('token');
          setToken(null);
        } finally {
          setLoading(false);
        }
      } else {
        setLoading(false);
      }
    };
    
    checkAuthStatus();
  }, [token]);
  
  // API request helper with token
  const apiRequest = async (endpoint, method = 'GET', data = null) => {
    try {
      const options = {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
      };
      
      if (token) {
        options.headers['Authorization'] = `Token ${token}`;
      }
      
      if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
        options.body = JSON.stringify(data);
      }
      
      const response = await fetch(`https://job-portal-api-cx5r.onrender.com${endpoint}`, options);
      
      if (response.status === 204) {
        return { success: true };
      }
      
      const responseData = await response.json();
      
      if (!response.ok) {
        throw new Error(responseData.error || JSON.stringify(responseData));
      }
      
      return responseData;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };
  
  // Fetch user profile
  const fetchUserProfile = async () => {
    return apiRequest('/api/accounts/profile/');
  };
  
  // Login function
  const login = async (credentials) => {
    try {
      const data = await apiRequest('/api/accounts/login/', 'POST', credentials);
      setToken(data.token);
      localStorage.setItem('token', data.token);
      
      // Fetch complete user data
      const userData = await fetchUserProfile();
      setUser(userData);
      
      return userData;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };
  
  // Register function
  const register = async (userData) => {
    try {
      const data = await apiRequest('/api/accounts/register/', 'POST', userData);
      setToken(data.token);
      localStorage.setItem('token', data.token);
      setUser(data.user);
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };
  
  // Logout function
  const logout = async () => {
    try {
      await apiRequest('/api/accounts/logout/', 'POST');
    } catch (err) {
      console.error('Logout API error:', err);
      // Continue with logout even if API fails
    } finally {
      localStorage.removeItem('token');
      setToken(null);
      setUser(null);
    }
  };
  
  const authContextValue = {
    user,
    token,
    loading,
    error,
    login,
    register,
    logout,
    apiRequest
  };
  
  return (
    <AuthContext.Provider value={authContextValue}>
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook for using auth context
export function useAuth() {
  return useContext(AuthContext);
}

// Example Login component
function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [loginError, setLoginError] = useState(null);
  const { login } = useAuth();
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setLoginError(null);
    
    try {
      await login({ username, password });
      // Redirect after successful login
      window.location.href = '/dashboard';
    } catch (err) {
      setLoginError(err.message);
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="login-container">
      <h2>Login to Your Account</h2>
      {loginError && <div className="error-message">{loginError}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      <p>
        Don't have an account? <a href="/register">Register here</a>
      </p>
    </div>
  );
}
```

## Common API Endpoints

### User Management
- `POST /api/accounts/register/` - Register new user
- `POST /api/accounts/login/` - User login
- `POST /api/accounts/logout/` - User logout
- `GET /api/accounts/profile/` - Get user profile
- `PUT /api/accounts/profile/` - Update user profile
- `PUT /api/accounts/change-password/` - Change password

### Jobs
- `GET /api/jobs/` - List all jobs (with filtering/pagination)
- `POST /api/jobs/` - Create new job (employers only)
- `GET /api/jobs/{id}/` - Get job details
- `PUT /api/jobs/{id}/` - Update job (creator only)
- `DELETE /api/jobs/{id}/` - Delete job (creator only)
- `GET /api/jobs/my-jobs/` - List jobs posted by current employer

### Applications
- `GET /api/applications/` - List applications (job seekers see their applications, employers see applications to their jobs)
- `POST /api/applications/` - Apply for a job
- `GET /api/applications/{id}/` - Get application details
- `PATCH /api/applications/{id}/` - Update application status (employers only)

### Bookmarks
- `GET /api/bookmarks/` - List bookmarked jobs
- `POST /api/bookmarks/` - Bookmark a job
- `DELETE /api/bookmarks/{id}/` - Remove bookmark
- `POST /api/bookmarks/toggle/{job_id}/` - Toggle bookmark status

### Companies
- `GET /api/companies/` - List companies
- `POST /api/companies/` - Create company (employers only)
- `GET /api/companies/{id}/` - Get company details
- `PUT /api/companies/{id}/` - Update company (owner only)

## Error Handling Best Practices

Always handle API errors gracefully:

```javascript
try {
  const data = await apiRequest('/some/endpoint');
  // Handle success
} catch (error) {
  // Check for specific error types
  if (error.message.includes('401') || error.message.includes('unauthorized')) {
    // Authentication error - redirect to login
    redirectToLogin();
  } else if (error.message.includes('403') || error.message.includes('forbidden')) {
    // Permission error
    showPermissionError('You don\'t have permission to perform this action');
  } else if (error.message.includes('404') || error.message.includes('not found')) {
    // Resource not found
    showNotFoundError('The requested resource was not found');
  } else {
    // General error
    showErrorMessage('An error occurred. Please try again later.');
  }
  
  // Log the error (in development)
  console.error('API error:', error);
}
```

## Performance Optimization Tips

1. **State Management**: Use context API or Redux for managing application state
2. **Caching**: Cache API responses for better performance
3. **Debouncing**: Implement debounce for search functionality
4. **Lazy Loading**: Use React.lazy() for code splitting
5. **Pagination**: Implement pagination for listing pages (API supports pagination)

```javascript
// Example of implementing pagination
function JobListPage() {
  const [jobs, setJobs] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const { apiRequest } = useAuth();
  
  useEffect(() => {
    const fetchJobs = async () => {
      setLoading(true);
      try {
        const response = await apiRequest(`/api/jobs/?page=${page}`);
        setJobs(response.results);
        setTotalPages(Math.ceil(response.count / 10)); // 10 is page size
      } catch (error) {
        console.error('Error fetching jobs:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchJobs();
  }, [page, apiRequest]);
  
  return (
    <div className="jobs-container">
      <h1>Available Jobs</h1>
      
      {loading ? (
        <div className="loading-spinner">Loading...</div>
      ) : (
        <>
          <div className="jobs-list">
            {jobs.map(job => (
              <JobCard key={job.id} job={job} />
            ))}
          </div>
          
          <div className="pagination">
            <button 
              onClick={() => setPage(prev => Math.max(prev - 1, 1))}
              disabled={page === 1 || loading}
            >
              Previous
            </button>
            
            <span>Page {page} of {totalPages}</span>
            
            <button
              onClick={() => setPage(prev => prev + 1)}
              disabled={page >= totalPages || loading}
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  );
}
```

## Testing with Render Free Tier

Due to the free tier limitations of Render:
- The first request may take up to a minute as the service spins up
- Implement a loading state to handle this delay
- Consider adding retry logic for failed initial requests

```javascript
// Example retry logic
async function apiRequestWithRetry(endpoint, method = 'GET', data = null, retries = 3, delay = 2000) {
  try {
    return await apiRequest(endpoint, method, data);
  } catch (error) {
    if (retries > 0) {
      console.log(`Retrying request to ${endpoint}. Attempts remaining: ${retries-1}`);
      await new Promise(resolve => setTimeout(resolve, delay));
      return apiRequestWithRetry(endpoint, method, data, retries - 1, delay);
    }
    throw error;
  }
}
```

## Security Considerations

1. **Never** store tokens in cookies without proper security measures
2. **Always** validate user input before sending to the API
3. **Don't** expose sensitive data in the frontend code
4. **Use** HTTPS for all requests
5. **Implement** proper logout functionality

## Contact & Support

If you encounter any issues with the API or need additional endpoints, please contact:
- Email: [your-email@example.com]
- GitHub: [https://github.com/JohannesGezachew/job-portal-api]

## API Version Information

Current version: 1.0.0 (April 2025)
- All breaking changes will be communicated in advance
- Check the GitHub repository for the latest updates 