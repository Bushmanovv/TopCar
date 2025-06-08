# 🚗 TopCar Vehicle Management System

TopCar is a web-based vehicle management system developed using **Streamlit** and **MySQL**. It allows users to manage car listings, view client data, track bookings, and handle administrative tasks in an intuitive and interactive dashboard.

## ✨ Features

* 🧾 **Vehicle Listings**: Add, edit, or delete cars with details like model, year, price, and availability.
* 📊 **Client Management**: Store and view customer information and sales records.
* 📆 **Booking System**: Track which vehicles are booked or available.
* 🔎 **Search & Filter**: Filter cars by type, price range, brand, and availability.
* 🔐 **Authentication (optional)**: Admin login support for managing system access.

## 🛠️ Tech Stack

* **Frontend**: Streamlit (Python)
* **Backend**: MySQL Database
* **ORM**: Raw SQL or MySQL connector for Python

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/topcar-management.git
cd topcar-management
```

### 2. Set Up Virtual Environment (optional)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Configure Database

* Create a MySQL database called `topcar_db`.
* Import the provided schema in `topcar_schema.sql`.
* Update your DB credentials in `config.py` or `db_connection.py` file.

### 5. Run the App

```bash
streamlit run app.py
```

## 📂 Project Structure

```bash
topcar-management/
├── app.py                 # Main Streamlit app
├── db_connection.py       # MySQL connection setup
├── views/                 # Streamlit pages (e.g., add car, view cars, etc.)
├── utils/                 # Helper functions
├── topcar_schema.sql      # MySQL schema
├── requirements.txt       # Python dependencies
└── README.md              # Project info
```

## 🧪 Sample SQL Schema (Excerpt)

```sql
CREATE TABLE vehicles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    make VARCHAR(100),
    model VARCHAR(100),
    year INT,
    price DECIMAL(10, 2),
    status ENUM('available', 'booked')
);
```

## 📸 Screenshots

*Coming soon...*

## 🤝 Contributing

Feel free to fork the repo, suggest features, or submit pull requests!

## 📄 License

This project is licensed under the MIT License.

---

> Created by BUSHMANOVV — Vehicle inventory, simplified.
