#  On-board  

A web-based job portal that connects job seekers with employers, allowing users to register, search for jobs, apply, and manage profiles while enabling employers to post job listings and review resumes.  

##  Features  

###  For Job Seekers  
- **User Registration & Profile Management** – Sign up, log in, and update profiles.  
- **Resume Upload** – Upload resumes for employers to review.  
- **Job Search & Application** – Search jobs by keywords (e.g., city, job title) and apply directly.  

###  For Employers  
- **Job Posting** – Post job listings with detailed requirements.  
- **Resume Review** – Access and generate PDF resumes uploaded by job seekers.  

## 🛠 Tech Stack  

### **Backend:**  
- **Django 5.1.2** – Web framework for backend logic and APIs  
- **Django REST Framework (if applicable)** – For building RESTful APIs  
- **WSGI** – For deploying the application  

### **Frontend:**  
- **HTML, CSS, JavaScript** – For templates and user interface  
- **Django Templates** – For rendering dynamic content  

### **Database:**  
- **SQLite** – Default database for storing user and job data  

### **Authentication & Security:**  
- **Django Authentication System** – User authentication and session management  
- **Password Validators** – Enforce strong password policies  
- **CSRF & XFrame Middleware** – Security against cross-site attacks  

### **File Management:**  
- **Static & Media Files** – Managed using **WhiteNoise**  
- **PDF Resume Handling** – If using ReportLab/PyPDF2 for PDF generation  

### **Deployment & Performance:**  
- **WhiteNoise** – Efficient static file serving  
- **Environment Variables** – Managed with **dotenv** for security  

### **Email Service:**  
- **SMTP (Gmail)** – Configured for email notifications  
- **TLS Encryption** – Secure email communication

### **Usage:**
-**Job Seekers:** Register, update profiles, search & apply for jobs.
-**Employers:** Post jobs, review applicants, and generate PDF resumes.

### **Screenshot:**

![job-final](https://github.com/user-attachments/assets/e539e541-29e4-4904-9e48-f4fb562d9dd0)


##  Installation & Setup  

1. **Clone the repository:**  
   ```sh
   git clone https://github.com/your-repo/job-portal.git
   cd job-portal

2 . **Create a virtual environment:**
    ```sh
    
    python -m venv venv
      source venv/bin/activate

3  . **Install dependencies:**
    ```sh
    
    pip install -r requirements.txt

4.    **Apply migrations:**
    ```sh
  
    python manage.py migrate

5 . **Run the development server:** 
    ```sh
    
    python manage.py runserver

6 . Access the portal at:

     http://127.0.0.1:8000/
