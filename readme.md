
## The User Management System IS601-Final Project: 
- The project for the User Management System gave participants excellent practical experience in the field of professional software     development. I focused on enhancing user profile functionality by integrating a Profile Picture Upload feature using Minio.To ensure efficient user interactions, I also included strong validation and handled edge cases. 

### The submission meets the following goals:
- Fixed five QA Issues/Bugs across the code.
- Implements a NEW feature-1Profile Picture Upload with Minio  into the existing code.
- Created 10 NEW Tests for the new feature implemented.
- Includes a Reflection Document for the course.

### Setup and Preliminary Steps: 

1. Fork the Project Repository: Fork the project repository to my own GitHub account.

2. Clone the repository to your local machine: Clone the forked repository to our local machine using the git clone command. 
  This creates a local copy of the repository on our computer, enabling we make changes and run the project locally.

   ```git clone git@github.com:nisha2110/IS601_final_user_management.git ```

## Change directory to the project
 ``` cd IS601_final_user_management and open code in  vistual studio write cmd: code . ``` 

## Install and Setup Docker [compulsory]

3. Verify the Project Setup: Follow the steps in the instructor video to set up the project using Docker. Docker allows our to package the application with all its dependencies into a standardized unit called a container. Verify that you can access the API documentation at http://localhost/docs and the database using PGAdmin at http://localhost:5050.

## Commands:
  - docker compose up --build
  - Running tests using pytest
  - docker compose exec fastapi pytest
  - docker compose exec fastapi pytest tests/test_services/test_user_service.py::test_list_users
  - Need to apply database migrationss: docker compose exec fastapi alembic upgrade head
  - Upload Image to minIO : docker compose exec fastapi python3 -m app.utils.minio_client

# Access various components
- PgAdmin:  http://localhost:5050
- FastAPI Swagger UI: http://localhost/docs
- MinIO console app open : http://localhost:9001
- MinIO API : http://localhost:9000


##  Feature-1 Implemented: Profile Picture Upload with Minio :
- This feature enhances the user profile management system by enabling users to upload and store profile pictures using Minio, a distributed object storage system. By personalizing their accounts with profile pictures, users gain a more engaging and tailored experience. The functionality focuses on secure storage, efficient retrieval, and seamless integration with the existing user profile management system.

### Five QA Issues/Bugs Resolved - [Link here](https://github.com/nisha2110/IS601_final_user_management/blob/main/documentation/Issue.md)

### Feature-1 Profile Picture Upload with Minio - [Link here](https://github.com/nisha2110/IS601_final_user_management/blob/main/documentation/feature-1_upload_picture.md)

### Test cases - [Link here](https://github.com/nisha2110/IS601_final_user_management/blob/main/documentation/Testcases.md)

### DockerHub Repository - [Link here](https://hub.docker.com/repository/docker/nishi2110/is601_final_api/general)

### GitHub Repository - [Link here](https://github.com/nisha2110/IS601_final_user_management/)

### Document Reflection File - [Link here](https://github.com/nisha2110/IS601_final_user_management/blob/main/documentation/Document_reflection.docx)
