# Final Project: User Management System 

## Issues and Fixes

## Issue 1

**Issue:** Broader Error Handling

**Details:** The issue details are following:

1.	In updating and creating methods there is no proper handling of errors like issues related to databases, validations etc.
2.	This leads to handling critical errors incorrectly.

**Code Fix:** [Check Here](https://github.com/kaw393939/user_management/commit/79870d5df3a5d1625138e1565f9b69895e1e4e17)

## Issue 2

**Issue:** Potential Glitch in the Generation of Nicknames

**Details:** The issue details are following:

1.	There is a potential glitch in handling the nicknames if it is already existed.
2.	It may create an infinite loop that makes the application hang and exhausts valuable resources.

**Code Fix:** [Check Here](https://github.com/kaw393939/user_management/commit/63b8d12976aa9921cf8d7a36f17536490b16bf5e)
