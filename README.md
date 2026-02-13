# 🚀 Setu Form Backend (DaskForm & Shifu)

A robust, multi-service backend system built with **Flask** and **PostgreSQL** to handle form submissions for two distinct platforms: **DaskForm** and **Shifu**.

This project uses a microservice-inspired architecture where two independent Flask applications run on different ports, sharing a PostgreSQL database but managing separate data models.

---

## 🏗️ Architecture Overview

The system consists of two primary services:

1.  **DaskForm (Port 5000):** Handles "Let's Connect" inquiries focused on hiring and talent needs.
2.  **Shifu (Port 5001):** Handles "Let's Get Started" business inquiries (Demos, Pilots, Briefings).

### Tech Stack
*   **Backend:** Python / Flask
*   **ORM:** SQLAlchemy
*   **Database:** PostgreSQL
*   **CORS:** Flask-CORS (Enabled for cross-origin frontend requests)
*   **Environments:** Dotenv for configuration management

---

## 🛠️ Getting Started

### 1. Prerequisites
*   Python 3.10+
*   PostgreSQL installed and running
*   A database named `postgres` (or as configured in `config.py`)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/rohanwadadar/setu_form_daskh_shifu.git
cd setu_form_daskh_shifu

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Configuration
Update `config.py` with your PostgreSQL credentials:
```python
DATABASE_URL = 'postgresql://username:password@localhost:5432/database_name'
```

### 4. Running the Servers
You need to run both servers in separate terminal windows:

**Start DaskForm (Port 5000):**
```bash
python run_daskform.py
```

**Start Shifu (Port 5001):**
```bash
python run_shifu.py
```

---

## 📡 API Documentation

### 🔹 DaskForm Service (`http://localhost:5000/api/daskform`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/` | Submit a new form entry |
| **GET** | `/` | Retrieve all submissions |
| **GET** | `/<id>` | Get a single entry by ID |
| **PUT** | `/<id>` | Update an entry |
| **DELETE** | `/<id>` | Delete an entry |

**Sample POST Body:**
```json
{
    "your_email": "user@example.com",
    "what_best_describes_you": "Software Engineer",
    "what_are_you_hoping_to_achieve": "Improve hiring workflow",
    "tell_us_more": "Specific details here (optional)"
}
```

---

### 🔹 Shifu Service (`http://localhost:5001/api/shifu`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/` | Submit a business inquiry |
| **GET** | `/` | Retrieve all requests |

**Sample POST Body:**
```json
{
    "name": "John Doe",
    "work_email": "john@company.com",
    "company": "Acme Corp",
    "role": "CTO",
    "looking_for": "Request a Demo",
    "goals": "Scale our AI training"
}
```
*Valid `looking_for` values: Request a Demo, Start a Pilot Program, General Inquiry, Schedule a Briefing.*

---

## ⚛️ Connecting with React

To connect your React application to this backend, you can use the native `fetch` API or `axios`.

### 1. Simple Axios Example
```javascript
import axios from 'axios';

const submitDaskForm = async (formData) => {
  try {
    const response = await axios.post('http://localhost:5000/api/daskform', {
      your_email: formData.email,
      what_best_describes_you: formData.role,
      what_are_you_hoping_to_achieve: formData.goal,
      tell_us_more: formData.details
    });
    console.log('Success:', response.data);
  } catch (error) {
    console.error('Error submitting form:', error.response?.data || error.message);
  }
};
```

### 2. Handling CORS in React
The backend is already configured with `Flask-CORS`. However, ensure your React app (usually on port 3000) is allowed to make requests. In development, this works automatically with the current setup.

### 3. Environment Variables in React
Create a `.env` file in your React project:
```env
REACT_APP_DASK_API=http://localhost:5000/api/daskform
REACT_APP_SHIFU_API=http://localhost:5001/api/shifu
```

---

## 🗄️ Database Schema

### `daksh_form` Table
*   `id`: Primary Key (Integer)
*   `your_email`: String (255)
*   `what_best_describes_you`: String (500)
*   `what_are_you_hoping_to_achieve`: String (500)
*   `tell_us_more`: Text (Optional)
*   `created_at`: DateTime

### `shifu_form` Table
*   `id`: Primary Key (Integer)
*   `name`: String (255)
*   `work_email`: String (255)
*   `company`: String (255)
*   `role`: String (255)
*   `looking_for`: String (255)
*   `goals`: Text (Optional)
*   `created_at`: DateTime

---

## 📜 License
Internal Project - Setu
