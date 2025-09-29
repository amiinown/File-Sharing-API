# FileSharing API — README

![Python](https://img.shields.io/badge/Python-3.12.3-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2.4-green?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.16-red?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17.5-blue?logo=postgresql&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-5.5.3-green?logo=celery&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-4.1.2-orange?logo=rabbitmq&logoColor=white)
![S3](https://img.shields.io/badge/boto3-1.39.13-blue?logo=amazonaws&logoColor=white)


**Overview**

This project is a **File Sharing API** built with **Django + Django REST Framework**. It uses **PostgreSQL** as the database and **RabbitMQ + Celery** for background task processing (sending password reset emails). Below are the installation and setup instructions for both **Linux** and **Windows**, along with the required steps to run the project.

---

## Requirements

* Python 3.8+
* pip
* virtualenv or venv
* Git (optional, for cloning the repository)

Additionally, the following services must be installed and running:

* PostgreSQL
* RabbitMQ

All Python dependencies are listed in `requirements.txt`.

---

## General Setup Steps (Development Environment)

1. Clone the repository:

```bash
git clone https://github.com/amiinown/File-Sharing-API.git
cd File-Sharing-API
```

2. Create and activate a virtual environment:

* Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

* Windows (PowerShell):

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
```

3. Install Python dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## PostgreSQL Installation

**Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib

# Enable and start the service
sudo systemctl enable --now postgresql

# Create a user and database (example)
sudo -u postgres createuser -P filesharing_user
sudo -u postgres createdb -O filesharing_user filesharing_db
```

**Windows:**

1. Download and install PostgreSQL from the [official website](https://www.postgresql.org/download/windows/).
2. Set a superuser (e.g., `postgres`) and password during installation.
3. Use pgAdmin or `psql` to create a database and user, then assign privileges.

---

## RabbitMQ Installation

**Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install -y rabbitmq-server

# Enable and start the service
sudo systemctl enable --now rabbitmq-server
```

**Windows:**

1. Install **Erlang** (required by RabbitMQ).
2. Download and install **RabbitMQ** from the official website.
3. Start RabbitMQ from the Windows Services panel.

---

## Running the Project

1. Copy `.env_sample` from the `filesharing/` folder to a new `.env` file and fill in the correct values:

```bash
cp filesharing/.env_sample filesharing/.env
```

2. Apply Django migrations:

```bash
python manage.py migrate
```

1. Create a superuser:

```bash
python manage.py createsuperuser
```

4. Start the Django development server:

```bash
python manage.py runserver
```

5. Start Celery workers (separate terminal):

```bash
celery -A filesharing worker -l info
```

---

## Important Notes

* For email-related features (like password reset), **Django**, **RabbitMQ**, and **Celery** must be running at the same time.
* Ensure `.env` contains correct values for database, s3, and email service.
* The project uses **ArvanCloud S3** for file storage. You can change the settings in `settings.py` to use a different S3-compatible service if needed.
* 
---

### Available documentation UIs:

* **Swagger UI:** [http://localhost:8000/schema/swagger-ui/](http://localhost:8000/schema/swagger-ui/)
* **Redoc:** [http://localhost:8000/schema/redoc/](http://localhost:8000/schema/redoc/)
* **Raw OpenAPI schema (YAML/JSON):** [http://localhost:8000/schema/](http://localhost:8000/schema/)

These tools are especially useful for **frontend developers** to easily explore available endpoints, parameters, and response formats.
