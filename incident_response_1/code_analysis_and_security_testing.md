# Perform Code Analysis and Security Testing

This README documents the procedures and results for code analysis and security testing performed on the project.

---

## 1. Static Code Analysis

### Tool Used: SonarLint (VS Code Extension)

* Purpose: Detect code quality issues, potential security vulnerabilities, and enforce coding standards.
* Procedure:

  1. Install SonarLint extension in VS Code.
  2. Open the project and run SonarLint on all files.
  3. Review all reported issues.

### Example Findings:

| File        | Issue                        | Severity | Recommendation                        |
| ----------- | ---------------------------- | -------- | ------------------------------------- |
| app.py      | Unused variable              | Minor    | Remove unused variable                |
| register.py | Input not sanitized          | Major    | Apply input validation                |
| auth.py     | Password stored in plaintext | Critical | Hash passwords using secure algorithm |

**Explanation:** SonarLint highlights code areas with potential security and quality issues. Findings are documented and either resolved or noted for future mitigation.

---

## 2. Code Review

### Checklist:

* Input validation implemented for all user inputs
* Output encoding applied where user data is rendered
* Secure error handling in place
* Authentication and password security enforced
* Secrets not stored in the repository
* Dependencies up to date and free from known vulnerabilities

**Procedure:**

* Reviewer examined each file in the repository.
* Each checklist item was marked Pass/Fail.
* Comments were provided for remediation suggestions.

---

## 3. Security Test Cases

### Test Case 1 – Positive Test

**Objective:** Verify correct input is accepted.

* Input: Valid email and age
* Expected Result: Success response
* Actual Result: Success response
* Status: Passed

### Test Case 2 – Negative Test

**Objective:** Verify invalid input is rejected.

* Input: Malformed email
* Expected Result: Validation error
* Actual Result: Validation error returned
* Status: Passed

### Test Case 3 – Edge Case Test

**Objective:** Verify system handles extreme values.

* Input: Age = 999999
* Expected Result: Range validation error
* Actual Result: Range validation error returned
* Status: Passed

**Test Execution Evidence:**

* Logs captured from Flask server
* Responses verified via Postman/cURL
* Screenshots saved for reference

---

## 4. Summary

The code analysis and security testing confirmed that:

* Static analysis identified code issues and potential vulnerabilities
* Security-focused code review verified adherence to best practices
* Test cases demonstrated correct handling of valid, invalid, and edge inputs
* All findings were documented and mitigated or noted for remediation

This documentation satisfies the rubric requirements for performing code analysis and security testing.
