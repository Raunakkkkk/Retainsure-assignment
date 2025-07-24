# URL Shortener Service - Implementation

## 📝 **Submission Details**

**Name:** Raunak Agarwal

**Email:** agarwalraunak2000@gmail.com

**Date Submitted:** 24-07-2025

**Time Taken:** [Hours/Minutes]

**Assignment:** URL Shortener Service


---

##  **Implementation Details**

This URL shortener service has been fully implemented with all required features. Below are the implementation details:

---

## 📋 **Features Implemented**

✅ **POST /api/shorten** - Shortens URLs and returns 6-character alphanumeric codes  
✅ **GET /<short_code>** - Redirects to original URLs with click tracking  
✅ **GET /api/stats/<short_code>** - Returns analytics (clicks, creation time, original URL)  
✅ **Thread-safe in-memory storage** - Handles concurrent requests safely  
✅ **URL validation** - Validates URLs before shortening  
✅ **Error handling** - Proper HTTP status codes and error messages  
✅ **Comprehensive tests** - 12 test cases covering all functionality

---

## 🏗️ **Architecture Overview**

### **Technology Stack:**

- **Flask 3.0.0** - Web framework
- **Python 3.8+** - Programming language
- **Threading locks** - Concurrency handling
- **Pytest** - Testing framework
- **In-memory storage** - Simple and fast

### **Design Decisions:**

- **In-memory storage** - Fast and simple, suitable for assignment scope
- **Thread-safe design** - Using `threading.Lock()` for concurrent request handling
- **6-character codes** - Alphanumeric (62^6 = 56+ billion possible combinations)
- **Regex URL validation** - Ensures proper URL format before processing
- **Modular structure** - Separated concerns into models, utils, and main app

---

## 📁 **Project Structure**

```
url-shortener/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # Flask application with all endpoints
│   ├── models.py            # URLStore class for data management
│   └── utils.py             # Utility functions (validation, code generation)
├── tests/
│   ├── conftest.py          # Pytest configuration for imports
│   └── test_basic.py        # Comprehensive test suite (12 tests)
├── __init__.py              # Root package initialization
├── run.py                   # Easy server startup script
└── requirements.txt         # Dependencies
```

---

## 🚦 **Quick Start**

### **1. Install Dependencies:**

```bash
pip install -r requirements.txt
```

### **2. Run the Server:**

```bash
python run.py
```

Server will be available at: `http://localhost:5000`

### **3. Run Tests:**

```bash
pytest tests/ -v
```

---

## 🔧 **API Usage Examples**

### **Shorten a URL:**

```bash
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/very/long/url"}'

# Response:
{
  "short_code": "abc123",
  "short_url": "http://localhost:5000/abc123"
}
```

### **Use Short URL (Redirect):**

```bash
curl -L http://localhost:5000/abc123
# Redirects to: https://www.example.com/very/long/url
```

### **Get Analytics:**

```bash
curl http://localhost:5000/api/stats/abc123

# Response:
{
  "url": "https://www.example.com/very/long/url",
  "clicks": 5,
  "created_at": "2024-01-15T10:30:45.123456"
}
```

### **Health Check:**

```bash
curl http://localhost:5000/api/health

# Response:
{
  "status": "ok",
  "message": "URL Shortener API is running"
}
```

---

## 🧪 **Testing Coverage**

The test suite covers:

- ✅ Health check endpoints
- ✅ Valid URL shortening
- ✅ Invalid URL handling
- ✅ Missing URL parameter handling
- ✅ URL redirection functionality
- ✅ Click tracking
- ✅ Analytics/stats retrieval
- ✅ Non-existent short code handling
- ✅ Invalid short code format handling
- ✅ Concurrent request handling
- ✅ Error responses and status codes

**Test Results:** 12/12 tests passing ✅

---

## 🔒 **Concurrency & Thread Safety**

- **Thread-safe storage** using `threading.Lock()`
- **Atomic operations** for click counting
- **Unique code generation** with collision detection
- **Safe concurrent URL shortening** and access

---

## 🎯 **Key Implementation Details**

### **Short Code Generation:**

- Uses `string.ascii_letters + string.digits` (62 characters)
- Generates 6-character codes (62^6 = 56+ billion combinations)
- Collision detection with retry mechanism
- Cryptographically random using Python's `random` module

### **URL Validation:**

- Regex pattern: `^(https?|ftp)://[^\s/$.?#].[^\s]*$`
- Supports HTTP, HTTPS, and FTP protocols
- Validates basic URL structure
- Rejects empty or malformed URLs

### **Error Handling:**

- **400 Bad Request** - Invalid URLs, missing parameters
- **404 Not Found** - Non-existent short codes, invalid formats
- **500 Internal Server Error** - Server-side issues
- **302 Found** - Successful redirects

---

## 📊 **Performance Characteristics**

- **O(1) lookups** - Dictionary-based storage
- **Thread-safe operations** - Minimal lock contention
- **Memory efficient** - Simple in-memory storage
- **Fast redirects** - Direct dictionary access

---
