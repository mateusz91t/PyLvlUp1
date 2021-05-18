from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from db.sqlalchemy import schemas, crud
from db.sqlalchemy.database import get_db

homework5 = APIRouter()


@homework5.get("/suppliers", response_model=List[schemas.SupplierIdName])
async def get_suppliers(db: Session = Depends(get_db)):
    return crud.get_suppliers(db)


@homework5.get("/suppliers/{supplier_id}", response_model=schemas.SupplierAll)
async def get_supplier(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(supplier_id, db)
    if not db_supplier:
        raise HTTPException(status_code=404, detail="SupplierAll not found")
    return db_supplier


@homework5.get("/suppliers/{supplier_id}/products", response_model=List[schemas.Product])
async def get_suppliers_products(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    products = crud.get_suppliers_products(supplier_id, db)
    if not products:
        raise HTTPException(status_code=404, detail="SupplierAll not found")
    return products


@homework5.post("/suppliers", response_model=schemas.SupplierAdded)
async def post_supplier(supplier: schemas.SupplierToAdd, db: Session = Depends(get_db)):
    return crud.post_suppliers(supplier, db)
