# Django Project

This project is a Django application designed to [describe your project's purpose or functionality]. This README will guide you through the process of setting up and running the project on a remote device.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Environment Variables](#environment-variables)
- [Running the Project](#running-the-project)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your machine.
- `pip` (Python package installer).
- PostgreSQL or another database if using a custom database setup.

## Installation

### 1. Clone the Repository

Clone the project repository from GitHub to your local machine using the following command:

```bash
git clone https://github.com/mriitian/backend.git
```
### 2. Navigate to the project directory

```bash
cd backend
```

### 3. Create virtual environment

```bash
python -m venv venv
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Start Server

```bash
python manage.py runserver
```


