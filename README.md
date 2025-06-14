# 🩺 Doctor FastAPI - CRUD Practice API

This is a **practice project** built using **FastAPI** to simulate a simple **Patient Management System** with full **CRUD** functionality.

## 📌 Features

* 🟢 **Create** patient records
* 🟡 **Read** patient data (view all or by ID)
* 🔵 **Update** existing patient information
* 🔴 **Delete** patient records
* 📊 **Sort** patient data by various parameters
* 🧠 Automatically computes **BMI** and provides a health **verdict**

## 🛠️ Tech Stack

* **FastAPI** – High-performance web framework for building APIs
* **Pydantic** – Data validation and parsing
* **JSON** – Used for local data storage

## 🚀 How to Run

1. Clone this repository
2. Install required dependencies
3. Start the FastAPI server using `uvicorn`
4. Access and test the API via Swagger UI at `http://127.0.0.1:8000/docs`

## 📁 Project Structure

```
📦doctor-api
 ┣ 📄 main.py            # FastAPI app with all CRUD routes
 ┣ 📄 patients.json      # Stores patient records
 ┗ 📄 README.md          # Project documentation
```

## ⚠️ Notes

* This project was created **purely for practice and learning purposes**.
* It does **not** include authentication, database integration, or production-level features.

## 📬 Feedback

If you have any feedback or suggestions, feel free to reach out or open an issue!

---
