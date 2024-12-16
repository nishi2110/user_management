

# The User Management System Final Project

## Issues and Fixes

## Issue 1

**Issue:** Email verification in user creation

**Details:** The issue details are following:

1. **Format Validation of Email:** The “EmailStr” type from “Pydantic” class ensures the email is in a valid format (e.g., test@domain. com). But, using patterns like “admin” is not restricted.
2. **Configurable Domains:** There is no dynamic use of a set of domains from email providers.
3. **Consistent Checking:** Converts usernames and domains into lowercase, but does not check consistently.
4. **Error Handing:** There is no such handing of errors with actionable feedback if validation fails.

**Code Fix:** [Click Here](https://github.com/kaw393939/user_management/commit/c9b3ccf8e8c190d7c3f7c3016a2155b18fc027db)

## Issue 2

**Issue:** Password verification in user creation

**Details:** The issue details are following:

1. **Ensuring Password Length:** There is no validation present for password length which should be at least 8 characters long.
2. **Requirement of Uppercase, Lowercase, Digits and Special Characters:** There is no validation present for the condition if passwords have uppercase letters (A-Z), lowercase letters (a-z), numerical digits (0-9) and special characters (!@#$%^&*(),.?\":{}|<>).

**Code Fix:** [Click Here](https://github.com/kaw393939/user_management/commit/28335cc379c4ca2da07221ae2fcec8f4fcad7489)

## Issue 3

**Issue:** Validate Nickname

**Details:** The issue details are following:

1.	**Valid Nickname Usage:** There is no validation to allow nicknames using characters, underscores, or hyphens.
2.	**Length Validation:** Both minimum and maximum lengths are not declared.

**Code Fix:** [Click Here](https://github.com/kaw393939/user_management/commit/bd85389f5f3458d860e752c9582cba2ce9d98977)