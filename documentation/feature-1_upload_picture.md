### Overview of feature1  Profile Picture Upload with Minio:
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

### GitHub Issue Link:
- **Install and config minIO - [here](https://github.com/nisha2110/IS601_final_user_management/issues/13)**
- **Code integration - [here](https://github.com/nisha2110/IS601_final_user_management/issues/15)**
- **Test and fix Profile url fetch and retrieve minIO - [here](https://github.com/nisha2110/IS601_final_user_management/issues/27)**

### To implement a Profile Picture Upload with Minio in project,follow these steps:

1. **Set Up Minio with Docker:** Make sure Minio is up and running by executing docker-compose up from the root of  project directory.
2. **Install Required Libraries:**
   ```pip install minio```
  ```pip install fastapi uvicorn python-multipart```

3. **Create a Minio Client:**  we are configuring the Minio client to connect to our minio service and making sure the bucket exists.

4. **Create Profile Picture Upload Endpoint:** add an API endpoint to handle the profile picture upload. This will allow users to upload   their profile pictures to the Minio bucket:
  - **Explanation:**
  - upload-profile-picture/ is a POST endpoint that accepts a file upload.
  - The file is stored in the demo bucket.
  - The function returns the URL where the profile picture is accessible.

5. **Add Profile Picture URL to User Model:** Update the user model to include a field for the profile picture URL.

6. **Update User Profile API to Include Profile Picture URL:** Modify the existing user profile API endpoints to allow updating the profile picture URL.

7. **Retrieve Profile Picture URL:** In the user profile view endpoint, retrieve the URL of the profile picture from Minio. 

8. **Optional Enhancements and Write Unit Tests:** 
  -  resize images before uploading them to Minio to ensure consistent image sizes and optimize loading times.
  -  File Format and Size Validation: Validate the file format and size before uploading to Minio.
  - Set a default profile picture.
  - Create unit tests to verify that the profile picture upload and retrieval functionalities work as expected.

- ### Output:
- **Run command and store jpeg file in minIO server demo bucket you can see image in miniIO bucket**
  ```WARN[0000] /home/hpatel/API/IS601_final_user_management/docker-compose.yml: the attribute 'version' is obsolete, it will be ignored, please remove it to avoid potential confusion 
  Bucket 'demo' already exists.
  File 'india.jpeg' successfully uploaded to bucket 'demo'.
  Generated presigned URL for 'india.jpeg': http://localhost:9000/demo/india.jpeg
  Presigned URL: http://localhost:9000/demo/india.jpeg

- ### Open FastAPI and get image and you can see iamge url:
 ![screenshot](https://github.com/nisha2110/IS601_final_user_management/blob/main/documentation/india_url.PNG)

- ### FastAPI copy and paste Url in console show result:
  ![Image open in console](https://github.com/nisha2110/IS601_final_user_management/blob/main/documentation/openimage.PNG)

- ### MinIO Bucket:
  ![MinIO Bucket](https://github.com/nisha2110/IS601_final_user_management/blob/main/documentation/minio_console.PNG)

- ### Profile picture Preview in MinIO:
  ![Profile picture Preview in MinIO](https://github.com/nisha2110/IS601_final_user_management/blob/main/documentation/preview.PNG) 

- ### This image store in my project 
  ![Image store in minio_data folder](https://github.com/nisha2110/IS601_final_user_management/blob/main/documentation/minio_data%20store.PNG) 







