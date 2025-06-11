import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# .envファイル読み込み（ローカル開発用のみ）
load_dotenv()

# 環境変数から接続URLを取得（AzureではApp Settingsで設定）
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL が環境変数に設定されていません。")

# DigiCertのルート証明書（backend/ 配下に配置すること）
ssl_cert_path = str(Path(__file__).parent / "DigiCertGlobalRootG2.crt.pem")

# SQLAlchemyエンジンの作成
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={
        "ssl": {
            "ssl_ca": ssl_cert_path
        }
    }
)

# セッション作成用ファクトリ
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースクラス（モデル定義用）
Base = declarative_base()

# 確認用ログ（任意）
print("✅ database.py: DATABASE_URL =", DATABASE_URL)
print("📄 証明書パス:", ssl_cert_path)
print("📄 証明書ファイル存在確認:", os.path.exists(ssl_cert_path))
