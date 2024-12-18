# Final Project: User Management System 

## Docker Hub URL [Check Here](https://hub.docker.com/repository/docker/hk574/final_project_user_management/general)


## Issues and Fixes

## Issue 1

**Issue:** Broader Error Handling

**Details:** The issue details are following:

1.	In updating and creating methods there is no proper handling of errors like issues related to databases, validations etc.
2.	This leads to handling critical errors incorrectly.

**Code Fix:** [Check Here](https://github.com/kaw393939/user_management/commit/09933034a73ed22d186100d30ad558d486a5ffdd)

## Issue 2

**Issue:** Potential Glitch in the Generation of Nicknames

**Details:** The issue details are following:

1.	There is a potential glitch in handling the nicknames if it is already existed.
2.	It may create an infinite loop that makes the application hang and exhausts valuable resources.

**Code Fix:** [Check Here](https://github.com/kaw393939/user_management/commit/563ca3f874cb5b3c8bab5a7adac4dfec3cad4dc5)

## Issue 3

**Issue:** No Expiry for Verification Tokens

**Details:** The issue details are following:

1.	No expiration duration has been mentioned for the tokens used for verification purposes.
2.	Security vulnerabilities may be found if the tokens are not expired.

**Code Fix:** [Check Here](https://github.com/kaw393939/user_management/commit/001f7c8803fa01f8a71b5b6d5e2c2741f85ab531)

## Issue 4

**Issue:** Indexing of Data Fields is Missing

**Details:** The issue details are following:

1.	Some of the fields like `id`,`email`, `nickname`, and `verification_token` are queried frequently without database indexing.
2.	In large-scale systems like user management, these degrade the overall performance.

**Code Fix:** [Check Here](https://github.com/kaw393939/user_management/commit/a07eb7f1de181af200d8df675b5adb42d0fc888f)

## Issue 5

**Issue:** Validation Gaps in Password Management

**Details:** The issue details are following:

1.	There is no validation of managing the user passwords. 
2.	Before hashing, there is no scope to validate for a strong password.

**Code Fix:** [Check Here](https://github.com/kaw393939/user_management/commit/5c0ed886fac7def2a9bc36b10403f3e1f3628091)
