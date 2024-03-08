Personal Library Management System API
Overview
The Personal Library Management System API is a RESTful API built using Django and Django REST Framework. It allows users to manage their personal library of books, including features for listing, adding, updating, and deleting books. The API integrates with a third-party service to retrieve book information using ISBN.

Features
Initialize a new Django project with the Django REST framework.
Define models for books and users, with features such as authentication, authorization, and data storage in PostgreSQL.
Implement token-based authentication to secure the API, ensuring that users can only access and modify their own book entries.
Create endpoints for listing, adding, updating, and deleting books, along with pagination for the book list endpoint.
Integrate with the Open Library API to fetch book details using ISBN.
Write unit tests for each API endpoint to ensure functionality, including tests for authentication, authorization, and rate limiting.
Handle error cases and edge cases appropriately.
Optimize queries to the database to avoid N+1 problems.
Document the API endpoints using Swagger.
Installation
Clone this repository to your local machine.
Install the required dependencies using pip install -r requirements.txt.
Set up a PostgreSQL database and configure the database settings in settings.py.
Apply migrations using python manage.py migrate.
Run the development server using python manage.py runserver.
Usage
Access the API endpoints using the provided URLs:
/createbooks/: Endpoint for creating new books.
/listbooks/: Endpoint for listing all books.
/books/<int:pk>/: Endpoint for retrieving, updating, or deleting a specific book by its primary key.
/user/: Endpoint for user registration and authentication.
/fetch/: Endpoint for fetching book details using ISBN.
Use tools like Postman or Swagger UI to interact with the API endpoints.
Ensure proper authentication by providing valid user credentials or tokens when required.
Testing
Run unit tests using python manage.py test to ensure the correctness of each API endpoint.
Include tests for authentication, authorization, rate limiting, and error handling to cover all scenarios.
Contributing
Fork the repository.
Create a new branch (git checkout -b feature/my-feature).
Make your changes and commit them (git commit -am 'Add new feature').
Push to the branch (git push origin feature/my-feature).
Create a new pull request.
Credits
This project was developed by Edafe Emmanuel Oghogho as part of E-library Project.
