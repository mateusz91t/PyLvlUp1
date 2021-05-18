from sqlalchemy import select
from sqlalchemy.dialects import postgresql
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
        models.Product.Discontinued,
        models.Category,
        # models.Category.CategoryID,
        # models.Category.CategoryName
    ).join(models.Category, models.Supplier).\
        filter(models.Supplier.SupplierID == supplier_id).\
        order_by(models.Product.ProductID)

    # print(str(o.statement.compile(dialect=postgresql.dialect())))

    return o.all()
