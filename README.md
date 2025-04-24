# 📦 1. Clone the repository
git clone https://github.com/yourusername/videoflix-backend.git
cd videoflix-backend

# 🐍 2. Create and activate virtual environment
python3 -m venv env
source env/bin/activate

# 📥 3. Install Python dependencies
pip install -r requirements.txt

# ⚙️ 4. Set up the database (PostgreSQL must be running)
You can skip if DB already exists
psql -U postgres
In the psql shell, run:
CREATE DATABASE videoflix_db;
\q

# 🛠️ 5. Run migrations
python manage.py migrate

# 👤 6. Create superuser (admin login)
python manage.py createsuperuser

# 🏗️ 7. Collect static files (optional for dev)
python manage.py collectstatic --noinput

# 🚀 8. Start the Django development server
python manage.py runserver

# 📂 9. (Optional) Start the Redis queue worker in a new terminal
source env/bin/activate
python start_worker.py
