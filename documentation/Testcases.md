### 10 New Test Cases for Feature:

### Testing and Quality Assurance:
- Developed a Comprehensive Test Suite: Created and implemented over 10 test cases to thoroughly validate the functionality of the profile picture upload feature.

- Outcome: The test cases ensure the feature is robust, user-friendly, and reliable. Key aspects like file validation, storage integrity, API interactions, and edge cases (e.g., invalid file formats, oversized uploads) are rigorously tested.

- Impact: This testing approach ensures seamless integration with the MinIO storage backend, maintaining high levels of security, performance, and data integrity for the profile picture upload feature.

## Test Cases for File Upload and Retrieval Functions:
1. **Invalid File Type Upload:  [Link here]**(https://github.com/nisha2110/IS601_final_user_management/issues/17)

- **Test Case Name:** test_upload_profile_picture_invalid_file_type
- **Description:** Validates that the application raises a ValueError when attempting to upload a file with an unsupported file type
  (e.g., .txt). This ensures only valid file types (e.g., .jpg, .png) are allowed.

- **Steps:**
- Create a mock file with .txt extension.
- Call the upload_profile_picture function with the mock file and invalid file type.
- The system should raise a ValueError indicating the file type is unsupported.

- **Expected Outcome:** A ValueError is raised with the message "Unsupported file type".

2. **Successful File Upload: [Link here]**(https://github.com/nisha2110/IS601_final_user_management/issues/19)

- Test Case Name: test_upload_profile_picture_success
- **Description:** Verifies that a valid file (e.g., .jpg) can be uploaded successfully to the MinIO bucket.

- **Steps:**
- Create a mock file with .jpg extension.
- Call the upload_profile_picture function with the mock file.
- Ensure the function makes the correct call to MinIO to upload the file.
- Assert the URL returned by the function is formatted correctly.

- **Expected Outcome:**
- The file is uploaded to the specified bucket in MinIO.
- The function returns a valid URL in the format http://localhost:9000/bucket_name/profile-picture.jpg.

3. **Retrieve URL for Existing File:  [Link here]**(https://github.com/nisha2110/IS601_final_user_management/issues/19)

- Test Case Name: test_get_profile_picture_url_success
- **Description:** Confirms that the system can generate a valid presigned URL for an existing file in the MinIO bucket.

- **Steps:**
-   Call the get_profile_picture_url function with an existing file name (e.g., profile-picture.jpg).
-   The system retrieves the presigned URL for the file.
-   Verify that the correct MinIO method (get_presigned_url) is called with the right parameters.

- **Expected Outcome:** A valid presigned URL is returned, which matches the expected URL for the file.

4. **Non-Existent File Retrieval:[Link here]**(https://github.com/nisha2110/IS601_final_user_management/issues/21)
- Test Case Name: test_get_profile_picture_url_non_existent_file
- **Description:** Ensures that the system raises an exception when attempting to retrieve a URL for a file that does not exist in the bucket.

- **Steps:**
- Call the get_profile_picture_url function with a non-existent file name (e.g., non-existent.jpg).
- Mock the behavior to simulate the scenario where the file does not exist.
- Verify that the system raises an exception indicating the file was not found.

- **Expected Outcome:** An exception is raised with the message "File not found".

5. **Large File Upload: [Link here]**(https://github.com/nisha2110/IS601_final_user_management/issues/21)
- Test Case Name: test_upload_profile_picture_large_file
- **Description:** Tests the ability of the system to upload large files (e.g., 20 MB) without issues.

- **Steps:**
- Create a mock file that is 20 MB in size.
- Call the upload_profile_picture function with the large file.
- Verify that the file is uploaded successfully and the correct MinIO method is called.

- **Expected Outcome:**
- The large file is uploaded without error, and the correct URL is returned for the uploaded file.

6. **Invalid Bucket Handling: [Link here]**(https://github.com/nisha2110/IS601_final_user_management/issues/21)
- Test Case Name: test_get_profile_picture_url_invalid_bucket
- **Description:** Verifies that the system handles an invalid bucket scenario and raises an appropriate exception.

- **Steps:**
- Simulate a situation where the specified bucket does not exist.
- Call the get_profile_picture_url function with a valid file name but an invalid bucket.
- Verify that the system raises an exception indicating "Bucket not found".

- **Expected Outcome:** An exception is raised with the message "Bucket not found".

7. **File Upload with Special Characters in Filename: [Link here]**(https://github.com/nisha2110/IS601_final_user_management/issues/21)
- Test Case Name: test_upload_profile_picture_special_characters
- **Description:** Ensures that files with special characters in their filenames (e.g., profile@picture#$.jpg) can be uploaded successfully.

- **Steps:**
- Create a mock file with special characters in its name.
- Call the upload_profile_picture function with the file.
- Verify that the file is uploaded and that the correct URL is returned.

- **Expected Outcome:**
- The file with special characters in the name is uploaded successfully.
- The correct URL, including the special characters, is returned.

8. **Server Error During File Upload:[Link here]**(https://github.com/nisha2110/IS601_final_user_management/issues/23)
- Test Case Name: test_upload_profile_picture_server_error
- **Description:** Simulates a server error during the file upload process and verifies that the system handles the error correctly.

- **Steps:**
- Simulate a server error (e.g., connection timeout or internal server issue) during the upload process.
- Call the upload_profile_picture function with a valid file.
- Verify that an exception is raised with a message indicating the server error.

- **Expected Outcome:** An exception is raised with the message "Server error".

9. **Timeout During URL Retrieval: [Link here]**(https://github.com/nisha2110/IS601_final_user_management/issues/23)
- Test Case Name: test_get_profile_picture_url_timeout
- **Description:** Ensures that the system raises a timeout exception when the URL retrieval process takes too long.

- **Steps:**
- Simulate a timeout error during the URL retrieval process (e.g., server takes too long to respond).
- Call the get_profile_picture_url function for a valid file.
- Verify that an exception is raised with the message "Request timed out".

- **Expected Outcome:** An exception is raised with the message "Request timed out".

10. **Empty File Upload:[Link here]**(https://github.com/nisha2110/IS601_final_user_management/issues/23)
- Test Case Name: test_upload_profile_picture_empty_file
- **Description:** Verifies that the system can handle the upload of an empty file (e.g., 0 bytes) without errors.

- **Steps:**
- Create an empty file (0 bytes).
- Call the upload_profile_picture function with the empty file.
- Verify that the file is uploaded successfully and that the correct URL is returned.

-**Expected Outcome:**The empty file is uploaded successfully, and the correct URL for the empty file is returned.





