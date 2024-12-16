

# The User Management System Final Project

## Issues and Fixes

### Issue 1

**Issue:** Email verification in user creation

**Details:** The issue details are following:

1. **Format Validation of Email:** The “EmailStr” type from “Pydantic” class ensures the email is in a valid format (e.g., test@domain. com). But, using patterns like “admin” is not restricted.
2. **Configurable Domains:** There is no dynamic use of a set of domains from email providers.
3. **Consistent Checking:** Converts usernames and domains into lowercase, but does not check consistently.
4. **Error Handing:** There is no such handing of errors with actionable feedback if validation fails.

**Code Fix:** [Click Here](https://github.com/kaw393939/user_management/commit/c9b3ccf8e8c190d7c3f7c3016a2155b18fc027db)

