from backend import models, schemas, crud
from backend.database import SessionLocal, engine
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend import crud
import os
from datetime import datetime  # ← こちらも重複してOK


app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# モデルのテーブルをDBに作成
models.Base.metadata.create_all(bind=engine)

# DBセッションを取得
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 商品情報取得API
@app.get("/product", response_model=schemas.ProductOut)
def get_product(code: str, db: Session = Depends(get_db)):
    product = crud.get_product_by_code(db, code)
    if not product:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    return product

# 購入登録API
@app.post("/purchase")
def purchase(data: schemas.TransactionIn, db: Session = Depends(get_db)):
    

    try:
        print("=== purchase endpoint reached ===")
        print("datetime now:", datetime.now())  # ここでエラーが出るならインポートが失敗している
        total = 0
        transaction = models.Transaction(
            DATETIME=datetime.now(),
            EMP_CD=data.emp_cd or "9999999999",
            STORE_CD="30",
            POS_NO="90",
            TOTAL_AMT=0,
            TTL_AMT_EX_TAX=0
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        for idx, item in enumerate(data.products):
            detail = models.TransactionDetail(
                TRD_ID=transaction.TRD_ID,
                DTL_ID=idx + 1,
                PRD_ID=item.PRD_ID,
                PRD_CODE=item.CODE,
                PRD_NAME=item.NAME,
                PRD_PRICE=item.PRICE,
                TAX_CD="01"  # 仮に"01"を使用
            )
            db.add(detail)
            total += item.PRICE

        transaction.TOTAL_AMT = total
        transaction.TTL_AMT_EX_TAX = total  # 本来は税抜処理を追加してもOK
        db.commit()
        return {"success": True, "total_amount": total}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"購入処理に失敗しました: {str(e)}")
       
    
