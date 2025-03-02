---

# Loan Management System

A Django-based Loan Management System that allows users to register, verify their email, and manage loans. Admins can view and manage all loans in the system.

---

## Features

- **User Authentication**:
  - Register with email and password.
  - Verify email using OTP.
  - Login with JWT-based authentication.
  - Refresh access tokens.
  - Logout with token blacklisting.

- **Loan Management**:
  - Users can apply for loans.
  - View their loan details and payment schedules.
  - Foreclose loans with a 10% interest discount.

- **Admin Features**:
  - View all loans in the system.
  - View loans for a specific user.
  - Delete loans.

---

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **Email Service**: Node.js (for sending OTPs)

---

## Setup Instructions

### Prerequisites

1. **Python** (version 3.8 or higher)
2. **PostgreSQL** (for the database)
3. **pip** (Python package manager)
4. **Git** (optional, for cloning the repository)

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/AdarshR268/Loan-Management-System.git
cd loan-management-system
```

---

### Step 2: Set Up a Virtual Environment

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

---

### Step 3: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

### Step 4: Set Up Environment Variables

Create a `.env` file in the root of your project and add the following:

```env
# Django Settings
SECRET_KEY=your-secret-key
DEBUG=True

# Database Configuration
DATABASE_NAME=your-db-name
DATABASE_USER=your-db-user
DATABASE_PASSWORD=your-db-password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

Replace the placeholders with your actual values.

---

### Step 5: Configure the Database

1. **Create a PostgreSQL Database**:
   - Open PostgreSQL and create a new database:
     ```sql
     CREATE DATABASE your-db-name;
     ```
   - Ensure the database user has the necessary permissions.

2. **Update Database Settings**:
   The database configuration is already set up in `settings.py` to use PostgreSQL. Ensure the `.env` file has the correct database credentials.

---

### Step 6: Run Migrations

Apply the database migrations to set up the required tables:

```bash
python manage.py migrate
```

---

### Step 7: Create a Superuser

Create a superuser to access the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to enter an email and password.

---

### Step 8: Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

The server will run at `http://127.0.0.1:8000/`.

---

### Step 9: Access the Admin Panel

1. Open your browser and go to `http://127.0.0.1:8000/admin/`.
2. Log in using the superuser credentials you created earlier.

---

### Step 10: Test the API Endpoints

You can use tools like **Postman** to test the API endpoints.

---

## API Documentation

### **Users App API Endpoints**

| Endpoint               | Method | Description                          |
|------------------------|--------|--------------------------------------|
| `/api/users/`          | POST   | Register a new user                  |
| `/api/users/verify-otp/` | POST   | Verify OTP sent to email             |
| `/api/users/login/`    | POST   | Login and get JWT tokens             |
| `/api/users/logout/`   | POST   | Logout and blacklist refresh token   |
| `/api/users/profile/`  | GET    | Get user profile details             |
| `/api/users/refresh-token/` | POST | Refresh access token                |

### **Loans App API Endpoints**

| Endpoint                          | Method | Description                          |
|-----------------------------------|--------|--------------------------------------|
| `/api/loans/`                     | POST   | Create a new loan                    |
| `/api/loans/`                     | GET    | Get all loans for the user           |
| `/api/loans/<loan_id>/foreclose/` | POST   | Foreclose a loan                     |
| `/api/loans/admin/`               | GET    | Get all loans (admin only)           |
| `/api/loans/admin/`               | POST   | Get loans for a specific user (admin)|
| `/api/loans/admin/`               | DELETE | Delete a loan (admin only)           |


---

## Running Tests

To run the tests for the project:

```bash
python manage.py test
```

---

## Deployment

For deployment:
- **Render**


Ensure you:
1. Set environment variables in the production environment.
2. Disable `DEBUG` mode in production.
3. Use a production-ready database (e.g., AWS RDS, Render Postgres).

---

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Submit a pull request.

---

## Contact

For questions or feedback, please contact:
- **ADARSH R**
- **Email**: adarshofficial268@gmail.com

- **GitHub**: [AdarshR268](https://github.com/AdarshR268/)

---
