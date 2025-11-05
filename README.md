# Flask To-Do Web App

A simple cloud-deployable To-Do List web application built with **Flask**, **Jinja2**, and **MongoDB Atlas**.  
The app allows users to add, edit, and delete tasks, with optional image upload via **ImgBB API**.  
It can be deployed easily on **Vercel** or **Heroku**.

---

## Features

- Add, edit, and delete to-do tasks
- Persistent storage using MongoDB Atlas
- Optional image uploads via ImgBB
- Flask + Jinja2 templating
- Deployable on Vercel or Heroku

---

## Project Structure

```
flaskProject/
├── app.py
├── requirements.txt
├── vercel.json
├── Procfile
├── .env.example
├── templates/
│   ├── base.html
│   ├── index.html
│   └── edit.html
├── static/
│   ├── css/style.css
│   └── js/tiny.js
```

---

## Local Setup

1. **Clone the repository**
   ```bash
   git clone <your_repo_url>
   cd flaskProject
   ```

2. **Set up a virtual environment and install dependencies**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: .\env\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   - Duplicate `.env.example` and rename it to `.env`
   - Fill in your credentials:
     ```text
     MONGODB_URI="mongodb+srv://<user>:<password>@cluster0.../?retryWrites=true&w=majority"
     DB_NAME="todo_db"
     IMGBB_API_KEY="your_imgbb_api_key_here"  # optional
     FLASK_SECRET="your-random-secret-key"
     ```

4. **Run locally**
   ```bash
   python app.py
   ```
   Then open http://127.0.0.1:5000 in your browser.

---

## Deployment on Vercel

1. Push your project to GitHub.
2. Go to [https://vercel.com](https://vercel.com) → **Import Project**.
3. Add the following environment variables in project settings:
   - `MONGODB_URI`
   - `DB_NAME` (default: todo_db)
   - `FLASK_SECRET`
   - `IMGBB_API_KEY` (optional)
4. Deploy — Vercel will automatically build and host your Flask app.

Your app will be available at:
```
https://<your-project-name>.vercel.app
```

---

## Deployment on Heroku (optional)

1. Install the Heroku CLI and log in:
   ```bash
   heroku login
   ```
2. Create a new Heroku app:
   ```bash
   heroku create my-flask-todo
   ```
3. Push the code to Heroku:
   ```bash
   git push heroku main
   ```
4. Add configuration variables:
   ```bash
   heroku config:set MONGODB_URI="mongodb+srv://..."
   heroku config:set FLASK_SECRET="your-secret"
   heroku config:set IMGBB_API_KEY="your-imgbb-key"
   ```

---

## Getting MongoDB Credentials

1. Visit [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Create a free cluster.
3. Add a database user (username & password).
4. Allow network access for your IP or `0.0.0.0/0` (for development).
5. Get your connection string under **Connect → Drivers → Python**.

Example:
```
mongodb+srv://flask_user:MyPass123@cluster0.mongodb.net/?retryWrites=true&w=majority
```

---

## License

This project is open for educational use and deployment demonstrations.
