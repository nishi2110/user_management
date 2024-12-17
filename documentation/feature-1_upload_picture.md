- This feature enhances the user profile management system by enabling users to upload and store profile pictures using Minio, a distributed object storage system. By personalizing their accounts with profile pictures, users gain a more engaging and tailored experience. The functionality focuses on secure storage, efficient retrieval, and seamless integration with the existing user profile management system.

### Description of Implementation:
1. API Endpoint for Uploading Profile Pictures:
- Create a dedicated API endpoint for handling profile picture uploads.
- Accept file uploads and validate the image format ( Supported e.g JPEG, PNG, GIF.) and size ( e.g.up to 5MB).

2. Integration with Minio:
- Configure Minio to securely store uploaded images in dedicated bucket.
- Generate a unique key for each image to avoid overwriting files.
- Use Minio REST API to upload images and retrieve their URLs.

3. Update User Profile Management:
- Add a new field in the user profile schema to store the profile picture URL.
- Update existing APIs to include the profile picture URL in responses.

4. Image Retrieval:
- Fetch the profile picture URL from Minio when displaying user profiles.
- Use Minio to create presigned URLs for safe and effective retrieval.
- Provide a default profile picture for users without an uploaded image.

5. Testing and Validation:
- Write Unit tests to verify the upload, storage, and retrieval workflows.
- Validate image formats and restrict sizes to ensure consistent uploads.
- Write Integration tests:
  - tested every step of the process, from upload to display.
  - Verify that API endpoints provide accurate information for both valid and invalid inputs.

### Important Points to Remember: 
- Security: Use access keys and HTTPS to ensure secure communication with Minio.
- Validation: Restrict file uploads to supported formats (e.g., JPG, PNG) and enforce size limits.
- Performance: Use buffering and optional picture scaling to improve image retrieval and speed up load times.
- Scalability: Design the storage and retrieval logic to support high traffic and large file volumes.
- Alternative Process: To improve user experience, set a default profile image.

### Key Validation Benefits
- Improves reliability by ensuring that only valid files are processed.
- Enhances user experience with clear error messages for invalid uploads.
- Prevents unnecessary storage usage by rejecting oversized or unsupported files.
- Supports scalable and maintainable code through automated test coverage.

- Output:
```WARN[0000] /home/hpatel/API/IS601_final_user_management/docker-compose.yml: the attribute 'version' is obsolete, it will be ignored, please remove it to avoid potential confusion 
Bucket 'demo' already exists.
File 'njit.jpeg' successfully uploaded to bucket 'demo'.
Generated presigned URL for 'njit.jpeg': http://localhost:9000/demo/india.jpeg
Presigned URL: http://localhost:9000/demo/india.jpeg```





