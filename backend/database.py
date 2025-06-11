import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# ローカル用 .env 読み込み
load_dotenv()

# 環境変数（ID/PWなど）取得
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DB = os.getenv("MYSQL_DB")

# 証明書を絶対パスで指定
ssl_cert_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "DigiCertGlobalRootG2.crt.pem"))

# DB接続URL構築
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

# エンジン作成
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={
        "ssl": {
            "ca": ssl_cert_path
        }
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

print("✅ DATABASE_URL =", DATABASE_URL)
print("📄 SSL証明書:", ssl_cert_path)
print("📄 証明書存在確認:", os.path.exists(ssl_cert_path))
