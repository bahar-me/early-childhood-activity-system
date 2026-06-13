# Sprint 2 Test Cases

## TC-01-01: User Login (Positive)

**Input:** Valid email and password

**Expected Result:** User is authenticated successfully and redirected to the appropriate dashboard.

---

## TC-01-02: User Login (Negative)

**Input:** Invalid email or password

**Expected Result:** Authentication fails and an appropriate error message is displayed.

---

## TC-01-03: Unauthorized Access Attempt

**Input:** Request to a protected endpoint without a valid JWT token

**Expected Result:** Access is denied and HTTP 401 Unauthorized is returned.

---

## TC-01-04: Role-Based Access Validation

**Input:** Teacher user attempts to access School Administrator resources

**Expected Result:** Access is denied according to role permissions.

---

## TC-02-01: Teacher Profile Creation (Positive)

**Input:** All required profile fields completed correctly

**Expected Result:** Teacher profile is created and saved successfully.

---

## TC-02-02: Teacher Profile Creation (Negative)

**Input:** One or more required fields are missing

**Expected Result:** Validation error message is displayed and profile is not saved.

---

## TC-02-03: Teacher Profile Update

**Input:** Existing teacher profile with modified information

**Expected Result:** Profile changes are saved successfully.

---

## TC-02-04: Teacher Profile Data Retrieval

**Input:** Existing teacher account with previously saved profile

**Expected Result:** Saved profile information is loaded correctly and displayed to the user.

## Summary

Sprint 2 testing focuses on authentication, authorization, and teacher profile management functionality. Both positive and negative scenarios are tested to verify system reliability, validation rules, and role-based access control.
