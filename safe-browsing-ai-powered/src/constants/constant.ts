// Base API URLs for different environments
const API_BASE_URL = process.env.NODE_ENV === 'production'
  ? 'https://yourapi.com'
  : 'http://127.0.0.1:8000';

// Authentication Endpoints
export const API_URLS = {
  SIGNUP: `${API_BASE_URL}/signup`,
  LOGIN: `${API_BASE_URL}/login`,
  ADD_WEBSITE : `${API_BASE_URL}/bannedWebsite`
};

// Other Constants
export const APP_NAME = "Safe Browsing Powered by AI";
export const STORAGE_KEYS = {
  TOKEN: "auth_token",
  USER_DATA: "user_data"
};

// Error Messages
export const ERROR_MESSAGES = {
  NETWORK_ERROR: "Network error, please try again later.",
  LOGIN_FAILED: "Invalid email or password.",
  SIGNUP_FAILED: "Sign up failed, please check your details."
};

// Success Messages
export const SUCCESS_MESSAGES = {
  LOGIN_SUCCESS: "Login successful!",
  SIGNUP_SUCCESS: "Sign up successful!",
};

//Actions
export const ACTIONS = {
  LOGIN: "login",
  SIGNUP: "signUp",
  ADD_WEBSITE: "GET_BLOCKED_WEBSITES"
};