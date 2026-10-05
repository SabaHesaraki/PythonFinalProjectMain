# Saba Data Entry App

A simple desktop application to manage plant and environmental records using Python and PostgreSQL.

## Features
- User login system.
- Add, view, edit, and delete records (CRUD).
- Data validation for numeric inputs.
- Export data to CSV files.

## Requirements
- Python 3.10+
- PostgreSQL
- `psycopg2-binary` library

## Application Screenshots

### Login Window
The app starts with a simple login screen.

<p align="center">
  <img src="https://github.com/user-attachments/assets/0c3fc70b-dc03-41c9-85c4-14b7415f34eb" alt="Login Window" width="300"/>

</p>

---

### Saving Records

<p align="center">
  <img src="https://github.com/user-attachments/assets/34a44538-d19b-45b1-9a4d-6ddc47c4dc5b" alt="Login Window" width="600"/>

</p>

---

### Updating Records

<p align="center">
  <img src="https://github.com/user-attachments/assets/98e08b68-e108-4cdd-b490-5f9ca1d23eb6" alt="Login Window" width="600"/>

</p>

---

### Validating Records

<p align="center">
  <img src="https://github.com/user-attachments/assets/9b58c680-3e16-4772-93a0-cee471be5951" alt="Login Window" width="600"/>

</p>


---

### Export CSV

<p align="center">
  <img src="src="https://github.com/user-attachments/assets/34527197-e241-41ea-929b-bf87deb32d5d"  alt="Login Window" width="600"/>

</p>

<p align="center">
  <img src="src=https://github.com/user-attachments/assets/ed108468-70f6-4341-a5b3-e0b4874be9e1" alt="Login Window" width="600"/>

</p>

---

## How to Run
1. Set up your PostgreSQL database using the `database.sql` script.
2. Install the required dependency:
```bash
   pip install psycopg2-binary
```   

Run the application:
bash
   python view.py
   
## Project Structure
- database.sql: Database schema and table definitions.
- model.py: Database connection and SQL operations.
- controller.py: Business logic and input validation.
- view.py: Tkinter user interface.
