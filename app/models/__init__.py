from sqlalchemy.ext.declarative import declarative_base

class_reg_postgres = {}
BasePostgres = declarative_base(class_registry=class_reg_postgres)
