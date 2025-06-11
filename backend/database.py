import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL が環境変数に設定されていません。")

# 証明書パス
ssl_cert_path = str(Path(__file__).parent / "DigiCertGlobalRootG2.crt.pem")

# 正しいssl接続パラメータ形式（PyMySQL向け）
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

print("✅ database.py: DATABASE_URL =", DATABASE_URL)
print("📄 証明書パス:", ssl_cert_path)
print("📄 証明書ファイル存在確認:", os.path.exists(ssl_cert_path))
