# Book Management System API

This is a Book Management System API that allows users to borrow and return books from the library. It includes features such as user authentication using JWT, tracking borrowed books, enforcing borrowing limits, calculating fines for overdue books, and viewing available books for borrowing.

## Features

### 1. **User Management**:
   - Register a new user.
   - Login to obtain a JWT token for authentication.

### 2. **Book Management**:
   - **Admin**: Full CRUD permissions for managing books in the library.
   - **Member**: View available books only.

### 3. **Borrowing Books**:
   - Borrow books from the library.
   - Enforce borrowing limits (max 5 books per user).
   - Set a return deadline for borrowed books (14 days).

### 4. **Returning Books**:
   - Return borrowed books.
   - Update the book status to available.
   - Automatically calculate overdue fines after return the book.

### 5. **Admin Features**:
   - Admin users can see all borrowed books and manage borrowing records.
   - Track borrowed books and their deadlines for all members.

---

## API Endpoints

### **User Endpoints**

#### 1. **Register**

- **POST** `/api/user/register/`
  - **Description**: Register a new user.


#### 2. **Login**

- **POST** `/api/user/login/`
  - **Description**: Login to the API and receive a JWT token.


---

### **Book Endpoints**

#### 1. **Available Books**

- **GET** `/api/book/available-books/`
  - **Description**: Retrieve a list of books that are currently available for borrowing.

#### 2. **Borrow Books**

- **POST** `/api/book/borrow/`
  - **Description**: Borrow books from the library.

#### 3. **Return Books**

- **POST** `/api/book/borrow/<id>/return/`
  - **Description**: Return borrowed books.

#### 4. **Borrowed Books**

- **GET** `/api/book/borrowed-list/`
  - **Description**:
    - Admin: View a list of all borrowed books with user details.
    - Member: View the list of books borrowed by the authenticated user.
  
#### 5. **CRUD Operations for Admin**

- **GET** `/api/book/`
  - Retrieve all books in the library.
  - **Permission**: Admin only.

- **POST** `/api/book/`
  - Add a new book to the library.
  - **Permission**: Admin only.

- **PUT** `/api/book/<id>/`
  - Update details of a specific book.
  - **Permission**: Admin only.

- **DELETE** `/api/book/<id>/`
  - Delete a book from the library.
  - **Permission**: Admin only.
---

## Technologies Used

- **Django**: Web framework for building the API.
- **Django REST Framework (DRF)**: For creating RESTful APIs.
- **Django Spectacular**: For generating OpenAPI schema and Swagger UI documentation.
- **Django ORM**: For interacting with the database models.
- **JWT Authentication**: For securing the API.
- **SQLite**: Database for storing books, users, and borrowing records.

---

## Setup Instructions

### 1. **Clone the Repository**

```bash
git clone https://github.com/s-nishad/Library-Management-API.git
cd Library-Management-API
