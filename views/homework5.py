from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
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
        raise HTTPException(status_code=404, detail="SupplierID not found")
    return db_supplier


@homework5.get("/suppliers/{supplier_id}/products", response_model=List[schemas.Product])
async def get_suppliers_products(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    products = crud.get_suppliers_products(supplier_id, db)
    if not products:
        raise HTTPException(status_code=404, detail="SupplierID not found")
    return products


@homework5.post("/suppliers", response_model=schemas.SupplierAdded, status_code=201)
async def post_supplier(supplier: schemas.SupplierToAdd, db: Session = Depends(get_db)):
    return crud.post_suppliers(supplier, db)


@homework5.put("/suppliers/{supplier_id}", response_model=schemas.SupplierAdded)
async def put_supplier(supplier_id: PositiveInt, supplier: schemas.SupplierToUpdate, db: Session = Depends(get_db)):
    put_sup = crud.put_supplier(supplier_id, supplier, db)
    if not put_sup:
        raise HTTPException(status_code=404, detail="SupplierID not found")
    return put_sup


@homework5.delete("/suppliers/{supplier_id}", status_code=204)
async def delete_suppliers(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    del_sup = crud.delete_supplier(supplier_id, db)
    if not del_sup:
        raise HTTPException(status_code=404, detail="SupplierID not found")
    return Response(status_code=204)
