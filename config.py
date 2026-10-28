import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'yuvashakti_secure_secret_key_2026_!@#$')
    
    # Database Configuration:
    # If MYSQL_URL or DATABASE_URL is set, use MySQL/configured DB.
    # Otherwise, default to SQLite in database/ngo_management.db for seamless zero-setup execution.
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'ngo_management')
    
    USE_MYSQL = os.environ.get('USE_MYSQL', 'false').lower() in ('true', '1', 'yes')
    
    if USE_MYSQL:
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
            "?charset=utf8mb4"
        )
    else:
        # Default zero-configuration SQLite database
        db_path = os.path.join(BASE_DIR, 'database', 'ngo_management.db')
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{db_path}')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
