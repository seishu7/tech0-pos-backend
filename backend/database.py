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
ssl_cert_path = "/home/site/wwwroot/backend/DigiCertGlobalRootG2.crt.pem"

# DB接続URL構築
DATABASE_URL = "mysql+pymysql://tech0sql1:step4pos-2@rdbs-step4-australia-east.mysql.database.azure.com:3306/posdb?ssl_ca=/home/site/wwwroot/backend/DigiCertGlobalRootG2.crt.pem"

# エンジン作成
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={
        "ssl_ca": ssl_cert_path
    }
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

print("✅ DATABASE_URL =", DATABASE_URL)
print("📄 SSL証明書:", ssl_cert_path)
print("📄 証明書存在確認:", os.path.exists(ssl_cert_path))
