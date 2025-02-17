from typing import List
from sqlalchemy.orm import declarative_base, Mapped
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

Base = declarative_base()

class ReportOperationsArguments(Base):
    __tablename__ = 'report_operations_arguments'
    __table_args__ = {'schema': 'analytical_platform'}
    argument_id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey('analytical_platform.report_operations.report_id'))
    argument_name = Column(String)
    argument_position = Column(Integer)
    associated_field = Column(String)
    argument_description = Column(String)
    default_value = Column(String)
    embedded = Column(Boolean)
    optional = Column(Boolean)
    block = Column(String)
    example = Column(String)
    operation : Mapped["ReportOperations"] = relationship(back_populates="arguments")

class ReportOperations(Base):
    __tablename__ = 'report_operations'
    __table_args__ = {'schema': 'analytical_platform'}
    report_id = Column(Integer, primary_key=True)
    report_description = Column(String)
    report_long_description = Column(String)
    enabled = Column(Boolean)
    query = Column(String)
    argument_usage = Column(String)
    arguments: Mapped[List["ReportOperationsArguments"]] = relationship(back_populates="operation", order_by=ReportOperationsArguments.argument_position, cascade="all, delete-orphan")






