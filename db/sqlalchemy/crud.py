from sqlalchemy.orm import Session

from db.sqlalchemy import models


def get_shippers(db: Session):
    return db.query(models.Shipper).all()


def get_shipper(shipper_id: int, db: Session):
    return db.query(models.Shipper).filter(models.Shipper.ShipperID == shipper_id).first()


def get_suppliers(db: Session):
    return db.query(models.Supplier.SupplierID, models.Supplier.CompanyName).order_by(models.Supplier.SupplierID).all()


def get_supplier(supplier_id: int, db: Session):
    return db.query(models.Supplier).filter(models.Supplier.SupplierID == supplier_id).first()


def get_suppliers_products(supplier_id: int, db: Session):
    o = db.query(
        models.Product.ProductID,
        models.Product.ProductName,
        models.Category.CategoryID,
        models.Category.CategoryName,
        models.Product.Discontinued
    ).join(models.Category, models.Supplier).\
        filter(models.Supplier.SupplierID == supplier_id).\
        order_by(models.Product.ProductID).all()
    # print(o)
    # print(type(o))
    # print(o[0])
    # print(o[0]['ProductID'])
    # print(type(o[0]))
    o = db.query(
        models.Product,
        models.Product.ProductID
    ).all()
    print(o)
    print(type(o))
    print(o[0])
    print(o[0]['ProductID'])
    print(type(o[0]))
    return o
