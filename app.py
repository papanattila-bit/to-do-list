# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import requests
from dotenv import load_dotenv

# Load .env in local dev only
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "change-me-locally")

# Environment variables
MONGODB_URI = os.getenv("MONGODB_URI") or os.getenv("MONGODB_URI".upper())
DB_NAME = os.getenv("DB_NAME", "todo_db")
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")  # optional

if not MONGODB_URI:
    raise RuntimeError("MONGODB_URI is not set. Add it to .env (local) or add env var in Vercel/Heroku.")

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
tasks_col = db["tasks"]

def upload_image_to_imgbb(file_obj):
    """Upload and return public URL from ImgBB. Returns None on failure or if key not provided."""
    if not IMGBB_API_KEY or file_obj.filename == "":
        return None
    upload_url = "https://api.imgbb.com/1/upload"
    # file_obj is a FileStorage - send raw file
    try:
        response = requests.post(
            upload_url,
            params={"key": IMGBB_API_KEY},
            files={"image": (file_obj.filename, file_obj.stream, file_obj.mimetype)}
        )
        data = response.json()
        if response.status_code == 200 and data.get("data", {}).get("url"):
            return data["data"]["url"]
    except Exception as e:
        app.logger.error("ImgBB upload failed: %s", e)
    return None

@app.template_filter("strid")
def _strid(oid):
    # Helpful in templates: convert ObjectId to string
    try:
        return str(oid)
    except Exception:
        return oid

@app.route("/")
def index():
    tasks = db.tasks.find()
    # Convert ObjectIds to strings before rendering
    todos = []
    for t in tasks:
        t["_id"] = str(t["_id"])
        todos.append(t)
    return render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    if not title:
        flash("Title is required", "danger")
        return redirect(url_for("index"))

    doc = {"title": title, "description": description}
    # optional image
    image = request.files.get("image")
    if image and image.filename:
        url = upload_image_to_imgbb(image)
        if url:
            doc["image_url"] = url

    tasks_col.insert_one(doc)
    flash("Task added", "success")
    return redirect(url_for("index"))

@app.route("/delete/<task_id>", methods=["POST"])
def delete_task(task_id):
    try:
        oid = ObjectId(task_id)
    except Exception:
        flash("Invalid id", "danger")
        return redirect(url_for("index"))
    tasks_col.delete_one({"_id": oid})
    flash("Task deleted", "success")
    return redirect(url_for("index"))

@app.route("/edit/<task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    try:
        oid = ObjectId(task_id)
    except Exception:
        flash("Invalid id", "danger")
        return redirect(url_for("index"))

    if request.method == "GET":
        task = tasks_col.find_one({"_id": oid})
        if not task:
            flash("Task not found", "danger")
            return redirect(url_for("index"))
        return render_template("edit.html", task=task)

    # POST -> update
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    if not title:
        flash("Title required", "danger")
        return redirect(url_for("edit_task", task_id=task_id))

    update = {"title": title, "description": description}
    image = request.files.get("image")
    if image and image.filename:
        url = upload_image_to_imgbb(image)
        if url:
            update["image_url"] = url

    tasks_col.update_one({"_id": oid}, {"$set": update})
    flash("Task updated", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    # Local dev
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
