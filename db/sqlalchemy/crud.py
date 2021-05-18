from sqlalchemy import update, insert, delete
from sqlalchemy.orm import Session

from db.sqlalchemy import models, schemas


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
        # Is there a better solution to SELECT * FROM categories; ??
        models.Category,
        # models.Category.CategoryID,
        # models.Category.CategoryName
    ).join(models.Category, models.Supplier). \
        filter(models.Supplier.SupplierID == supplier_id). \
        order_by(models.Product.ProductID.desc())

    # print(str(o.statement.compile(dialect=postgresql.dialect())))

    return o.all()


def post_suppliers(supplier, db: Session):
    db_insert = (
        insert(models.Supplier).values(**supplier.dict()).returning(models.Supplier)
    )
    result = db.execute(db_insert)
    db.commit()
    return next(result)


def put_supplier(supplier_id: int, supplier: schemas.SupplierToUpdate, db: Session):
    db_update = (
        update(models.Supplier).\
            where(models.Supplier.SupplierID == supplier_id).\
            values(**supplier.dict(exclude_none=True)).returning(models.Supplier)
    )
    result = db.execute(db_update)
    output = list()
    for el in result:
        output.append(el)
    db.commit()
    if output:
        return output[0]
    else:
        return output


def delete_supplier(supplier_id: int, db: Session):
    db_delete = (
        delete(models.Supplier).where(models.Supplier.SupplierID == supplier_id).returning(models.Supplier.SupplierID)
    )
    result = db.execute(db_delete)
    output = list()
    for el in result:
        output.append(el)
    db.commit()
    return output
