
## The User Management System Is601-Final Project: 

### Setup and Preliminary Steps: 

1. Fork the Project Repository: Fork the project repository to my own GitHub account.

2. Clone the repository to your local machine: Clone the forked repository to our local machine using the git clone command. This    
   creates a local copy of the repository on our computer, enabling we make changes and run the project locally.

git clone git@github.com:nisha2110/IS601_final_user_management.git

# Change directory to the project
cd IS601_final_user_management and open code in  vistual studio write cmd: code .

# Install and Setup Docker [compulsory]

3. Verify the Project Setup: Follow the steps in the instructor video to set up the project using Docker. Docker allows our to package the application with all its dependencies into a standardized unit called a container. Verify that you can access the API documentation at http://localhost/docs and the database using PGAdmin at http://localhost:5050.

## Commands:
- docker compose up --build
- Running tests using pytest
- docker compose exec fastapi pytest
- docker compose exec fastapi pytest tests/test_services/test_user_service.py::test_list_users
- Need to apply database migrationss: docker compose exec fastapi alembic upgrade head

# Access various components
PgAdmin
http://localhost:5050
FastAPI Swagger UI
http://localhost/docs

# Issues Resolved:

- Resolved 5 key issues to improve the project::

    1.  Fix issue in Docker File to allow build : [Issue-1 link](https://github.com/nisha2110/IS601_final_user_management/issues/1)
    • --allow-downgrades: Ensures that the package manager permits downgrading libc-bin to the specified version (2.36-9+deb12u7).
    • Updated the Docker File to allow build.
    • Resolved Application Errors: Fixed issues caused by mismatched library versions to ensure smooth application functionality.
    
    2. Profile picture URL validation: [Issue-2 Link](https://github.com/nisha2110/IS601_final_user_management/issues/3)
    • Ensured the provided URL is well-formed and points to an image file by validating that it ends with standard image extensions    
      such as .jpg, .jpeg or .png.
    • Implemented robust URL validation mechanisms to ensure secure and valid profile picture uploads. This includes verifying that the 
      URL is properly structured, ends with acceptable image file extensions, and optionally confirming the URL's accessibility and that it references a valid image resource.

