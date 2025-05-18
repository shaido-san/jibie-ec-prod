import os
from pathlib import Path
from dotenv import load_dotenv

# .env の読み込み（ローカル用）
load_dotenv()

# プロジェクトのベースディレクトリ
BASE_DIR = Path(__file__).resolve().parent.parent

# セキュリティキー（ローカルはテスト用でもOK）
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-default")

# デバッグモード（ローカルはTrue、本番はFalse）
DEBUG = os.getenv("DEBUG", "False") == "True"

# アクセス許可するホスト名
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1 localhost").split()

# Stripe APIキー（ローカルはテスト用キー、今回は本番もテストキーにしてある。）
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY", "")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")

# インストールされるアプリケーション
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "base",  # ここにアプリ名を入れる
    "rest_framework", # インストールしたdjangoのrestフレームワーク
    "corsheaders",
]

# ミドルウェア
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "jibie_ec.urls"

# テンプレート設定
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # テンプレートディレクトリ
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "jibie_ec.wsgi.application"

# データベース設定（ローカルは SQLite でOK）
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.getenv("DB_NAME", BASE_DIR / "db.sqlite3"),
        "USER": os.getenv("DB_USER", ""),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", ""),
        "PORT": os.getenv("DB_PORT", ""),
    }
}

# パスワードバリデータ
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ロケール
LANGUAGE_CODE = "ja"
TIME_ZONE = "Asia/Tokyo"
USE_I18N = True
USE_TZ = True

# 認証設定
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/index/"
LOGOUT_REDIRECT_URL = "/login/"

# スタティックファイルとメディアファイル（ローカルと本番で同じでOK）
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STATICFILES_DIRS = [
    BASE_DIR / "static",  
]

# カスタムユーザーモデル
AUTH_USER_MODEL = "base.User"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# セキュリティ（ローカルはセキュアをOFF）
SESSION_COOKIE_SECURE = False  # 本番は True にする
CSRF_COOKIE_SECURE = False     # 本番は True にする
X_FRAME_OPTIONS = "DENY"

# メール送信（ローカルは設定済み or ダミー）
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "hiroto.saitou1201@gmail.com")

# ログ設定（ローカルはファイルにエラーを書き出す）
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/error.log",  # ログファイル出力先
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
CORS_ALLOW_ALL_ORIGINS = True