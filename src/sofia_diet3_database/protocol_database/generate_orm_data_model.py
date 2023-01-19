from typing import List, Any
from src.jaguar_backend.file import File
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class ORMClassBuilder:
    """
    ```python
    from sqlalchemy import Column, Integer, ForeignKey
    from sqlalchemy.orm import relationship

    class User(Base):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True)

    class Order(Base):
        __tablename__ = "orders"
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey("users.id"))
        user = relationship("User", back_populates="orders")

    User.orders = relationship("Order", order_by=Order.id, back_populates="user")
    ```

    SQLAlchemy supports several types of columns in its ORM:
    ```txt
    Integer: For integer values
    String: For character or string values
    Date: For date values
    DateTime: For datetime values
    Float: For floating point values
    Boolean: For boolean values
    Enum: For enumerated values
    LargeBinary: For binary data
    PickleType: For storing Python objects using pickling
    Interval: For storing timedelta values
    Numeric: For storing decimal values
    Text: For storing large text values
    Time: For storing time values
    Unicode: For storing Unicode string values
    UnicodeText: For storing large Unicode text values
    BigInteger: For storing large integer values
    SmallInteger: For storing small integer values
    ARRAY: For storing arrays of values
    JSON: For storing JSON objects
    JSONB: For storing binary JSON objects
    UUID: For storing universally unique identifiers (UUIDs)
    ```
    """
    model: str = ""
    __orm_types: List[str] = field(default_factory=lambda: ["Integers", "String", "Date", "DateTime", "Float", "Boolean", "LargeBinary",
                                   "PickleType", "JSON", "UUID", "JSONB", "Numeric", "Interval", "Enum", "Text", "Time", "Unicode", "UnicodeText", "SmallInteger", "ARRAY"])

    def __convert_type_to_orm_type(self, type: str) -> str:
        pass

    def generate_class(self, name: str, types: List[Any], ) -> None:

        self.model += '''
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://username:password@localhost:5432/mydatabase')

Session = sessionmaker(bind=engine)
session = Session()

# Create a base class for defining the structure of our objects
Base = declarative_base()

class {}(Base):
  __tablename__ = {}
  id = Column(Integer, primary_key=True)
    '''.format(name, name.lower())

    # fk_name is like "User" and fk is like users.id where users is the __tablename__ of the user table
        for variable, _type, default_value, fk, fk_name in types:
            if fk:
                self.model += '''
  {} = Column({},ForeignKey({}),ondelete="CASCADE")
  {} = relationship({}, back_populates={})
  '''.format(variable, self.__convert_type_to_orm_type(_type), fk, fk_name.lower(), fk_name, name)
            else:
                self.model += '''
  {} = Column({},nullable=False,default={})'''.format(variable, self.__convert_type_to_orm_type(_type), default_value)

    def build_class(self, filename="data_model.py") -> None:
        File(Path(filename)).append(self.model)
