from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from db.sqlalchemy import schemas, crud
from db.sqlalchemy.database import get_db

homework5 = APIRouter()


@homework5.get("/suppliers", response_model=List[schemas.SupplierAll])
async def get_suppliers(db: Session = Depends(get_db)):
    o = crud.get_suppliers(db)
    return o


@homework5.get("/suppliers/{supplier_id}", response_model=schemas.Supplier)
async def get_supplier(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(supplier_id, db)
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier
