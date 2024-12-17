
  # Resolved 5 key issues to improve the project::

  1.  Fix issue in Docker File to allow build : [Issue-1 link](https://github.com/nisha2110/IS601_final_user_management/issues/1)

  - --allow-downgrades: Ensures that the package manager permits downgrading libc-bin to the specified version (2.36-9+deb12u7).
  - Updated the Docker File to allow build.
  - Resolved Application Errors: Fixed issues caused by mismatched library versions to ensure smooth application functionality.
    
  2. Profile picture URL validation: [Issue-2 Link](https://github.com/nisha2110/IS601_final_user_management/issues/3)

  - Ensured the provided URL is well-formed and points to an image file by validating that it ends with standard image extensions    
    such as .jpg, .jpeg or .png.
  - Implemented robust URL validation mechanisms to ensure secure and valid profile picture uploads. This includes verifying that the 
    URL is properly structured, ends with acceptable image file extensions, and optionally confirming the URL's accessibility and that it references a valid image resource.
    
  3. User ID being passed as None in the user verification email has been resolved: [Issue-3 Link](https://github.com/nisha2110/IS601_final_user_management/issues/5)

  - The problem of the User ID being None in the email verification process has been fixed.
  - The email is now sent only once, when the user is either created or updated in the database.
  - The code has been updated to ensure that the correct User ID is passed and displayed in the email verification, eliminating the  
    issue of None being shown.  
    
  4. Nickname Assign and Uniqueness in User Registration: [Issue-4 Link](https://github.com/nisha2110/IS601_final_user_management/issues/7)

  - Removed the call to the generate_nickname() function when assigning a new user's nickname.
  - Instead, the nickname is now directly set using the provided user data (user_data["nickname"]).
  - The system checks for uniqueness of the provided nickname in the database. 

  5. Password Validation in User Registration: [Issue-5 Link](https://github.com/nisha2110/IS601_final_user_management/issues/9)

  -  The implementation of password validation logic used during user registration to ensure strong and secure passwords.
  - Key Features of the Validation:
    1. Minimum Length Requirement:  Passwords must be at least 8 characters long.
    2. Uppercase Letter Check:  Passwords must include at least one uppercase letter (A-Z).
    3. Lowercase Letter Check: Passwords must include at least one lowercase letter (a-z).
    4. Digit Check: Passwords must include at least one numeric digit (0-9).
    5. Special Character Requirement: Passwords must contain at least one special character from the set !@#$%^&*(),.?":{}|<>.
