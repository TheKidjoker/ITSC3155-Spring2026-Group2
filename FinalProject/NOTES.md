# Database Setup Notes

## IMPORTANT: Each developer must set their own database password locally

The database password is **not** stored in the code. You must set it as an environment variable before running the app.

---

## Option 1: Set DB_PASSWORD in PowerShell (Quick)

Open PowerShell and run:

```powershell
$env:DB_PASSWORD="yourpassword"
```

Then start the app from the **same terminal**:

```powershell
python -m uvicorn api.main:app --reload
```

**Note:** This only lasts for the current terminal session. You must set it again each time you open a new terminal.

---

## Option 2: Use a .env file (Recommended for convenience)

1. Create a file called `.env` in the `FinalProject/` directory:

```
DB_HOST=localhost
DB_NAME=sandwich_maker_api
DB_PORT=3306
DB_USER=root
DB_PASSWORD=yourpassword
```

2. Install python-dotenv:

```powershell
pip install python-dotenv
```

3. The app will pick up the values automatically if python-dotenv is configured.

---

## .gitignore

Make sure `.env` is listed in your `.gitignore` so passwords are never pushed to GitHub:

```
.env
```

---

## Other Environment Variables (Optional)

| Variable      | Default              | Description          |
|---------------|----------------------|----------------------|
| DB_HOST       | localhost            | Database host        |
| DB_NAME       | sandwich_maker_api   | Database name        |
| DB_PORT       | 3306                 | Database port        |
| DB_USER       | root                 | Database user        |
| DB_PASSWORD   | (empty)              | Database password    |
| APP_HOST      | localhost            | App host             |
| APP_PORT      | 8000                 | App port             |

---

## Running the App

From the `FinalProject/` directory:

```powershell
$env:DB_PASSWORD="yourpassword"
python -m uvicorn api.main:app --reload
```

Swagger docs will be available at: http://localhost:8000/docs
