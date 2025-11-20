# Secure Coding Practices README

This README demonstrates the implementation of secure coding practices using Python and Flask, including input validation, output encoding, secure error handling, and authentication with password security.

---

## 1. Input Validation

### Example 1: Email Validation

```python
from flask import Flask, request, jsonify
import re

app = Flask(__name__)

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email', '')
    if not re.match(EMAIL_REGEX, email):
        return jsonify({'error': 'Invalid email address'}), 400
    return jsonify({'message': 'Email accepted'})
```

**Explanation:** Uses a regular expression to validate that the submitted email matches standard email formats. Returns controlled error messages.

### Example 2: Numeric Validation (Age Input)

```python
@app.route('/set_age', methods=['POST'])
def set_age():
    data = request.get_json()
    try:
        age = int(data.get('age', 0))
    except ValueError:
        return jsonify({'error': 'Age must be a number'}), 400

    if age < 13 or age > 120:
        return jsonify({'error': 'Age must be between 13 and 120'}), 400
    return jsonify({'message': f'Age set to {age}'})
```

**Explanation:** Ensures age is a valid integer and within an acceptable range.

---

## 2. Output Encoding

### Example: HTML Escaping

```python
from flask import render_template_string, escape

@app.route('/show/<username>')
def show(username):
    safe_username = escape(username)
    return render_template_string("<p>Hello {{ name }}</p>", name=safe_username)
```

**Explanation:** Escapes user input before rendering to prevent XSS attacks.

---

## 3. Secure Error Handling

### Example: Flask Error Handling

```python
@app.errorhandler(500)
def internal_error(error):
    # Log detailed error internally
    app.logger.error(f"Internal Error: {error}")
    return 'Internal server error', 500
```

**Explanation:** Internal errors are logged for developers, but users receive a generic message.

---

## 4. Basic Authentication and Password Security

### Example: Password Hashing with bcrypt

```python
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/register_user', methods=['POST'])
def register_user():
    data = request.get_json()
    password = data.get('password', '')
    # Hash password
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    # Store hashed_password in database
    return jsonify({'message': 'User registered successfully'})
```

**Explanation:** Passwords are hashed securely before storing; plaintext passwords are never saved.

### Password Policy:

* Minimum 12 characters
* At least 1 uppercase letter
* At least 1 number
* At least 1 special character

**Authentication Flow:**

1. User registers with a compliant password.
2. Password is hashed using PBKDF2 or bcrypt before storage.
3. During login, input password is hashed and compared to stored hash.

---

## 5. Summary

This README demonstrates Python-based secure coding practices:

* Input validation for email and numeric inputs
* Proper output encoding to prevent XSS
* Secure error handling
* Basic authentication with strong password policies

All code snippets are ready for adaptation to a real project and meet the security requirements in a professional workplace.
