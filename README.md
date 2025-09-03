#  SkinWizardAWS - Graduation Project

SkinWizardAWS is a Django-based web application for **AI-powered skin disease detection** and **patient–doctor interaction**.  
It combines medical image diagnosis with patient history forms, consultations, and pharmacy integration, making it a complete solution for dermatology support.

---

## Features

-  **User Authentication** – Secure login and registration system.  
-  **Patient Forms** – Patients fill out medical history before diagnosis.  
-  **AI Diagnosis** – Upload or scan skin images to receive AI-based predictions.  
-  **Consultations** – Redirect patients to doctors for further advice.  
-  **Content Management** – Educational content & resources for patients.  
-  **Pharmacy Module** – Manage prescriptions and treatments.  
- **AWS Integration** – Supports AWS for storage and deployment.  

---

## Project Structure

skinwizardAWS/
accounts/ # User authentication & profiles
consultation/ # Patient consultation workflows
 content/ # Educational content management
diagnosis/ # AI model integration & diagnosis logic
 media/ # File & image uploads
 patient_form/ # Patient medical history forms
pharmacy/ # Pharmacy & prescriptions
 skinwizard/ # Core project settings
manage.py # Django management script
requirements.txt # Python dependencies



---

## ⚙️ Getting Started

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Mennahady/skinwizardAWS.git
cd skinwizardAWS
2️⃣ Create & activate a virtual environment

python -m venv venv
# On Linux/Mac
source venv/bin/activate
# On Windows
venv\Scripts\activate
3️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Apply database migrations

python manage.py migrate
5️⃣ Run the development server

python manage.py runserver
Now open http://127.0.0.1:8000/ 🎉

🔑 Environment Variables
Create a .env file in the project root and configure:

env
Copy code
SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_URL=your_database_url
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_STORAGE_BUCKET_NAME=your_bucket_name
🧪 Running Tests
bash
Copy code
python manage.py test
📌 Future Improvements
Doctor notes & recommendations

Real-time chat between doctors and patients

Mobile app integration (Flutter)

 Authors
Zakya Akram
Barbara Youssef
Menna Abdelhady


📜 License
This project is developed for academic purposes as part of a graduation project.
You may use or extend it with proper attribution.

