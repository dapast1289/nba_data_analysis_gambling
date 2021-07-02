#!/user/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, Float, DATETIME, func, Date
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# engine = create_engine("mysql+pymysql://root:root@localhost:3306/nba_db_test", echo=True)
engine = create_engine("mysql+pymysql://root:root@localhost:3306/nba_db", echo=True)
Base = declarative_base()

def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
    cls.__str__ = __str__
    return cls

@auto_str
class AnalysisRecord(Base):
	__tablename__ = "analysis_record"
	id = Column("id", Integer, primary_key=True, autoincrement=True)
	season = Column("season", String(255), nullable=False)
	period_days = Column("period_days", Integer, nullable=False)
	uuid = Column("uuid", String(255), nullable=False)
	lose_keyword = Column("lose_keyword", String(255), nullable=False)
	continue_lose_num = Column("continue_lose_num", Integer, nullable=False)
	sample_count = Column("sample_count", Integer, nullable=False)
	sample_start_date = Column("sample_start_date", Date, nullable=False)
	sample_end_date = Column("sample_end_date", Date, nullable=False)
	win_count = Column("win_count", Integer, nullable=False)
	loss_count = Column("loss_count", Integer, nullable=False)
	lose_percent = Column("lose_percent", DOUBLE, nullable=False)
	win_percent = Column("win_percent", DOUBLE, nullable=False)
	cost_of_seconds = Column("cost_of_seconds", Integer, nullable=False)
	create_time = Column("create_time", DATETIME, server_default=func.now(), nullable=False)
	update_time = Column("update_time", DATETIME, server_default=func.now(), onupdate=func.now(), nullable=False)

def init_db():
	Base.metadata.create_all(engine)


def drop_db():
	Base.metadata.drop_all(engine)


class AnalysisRecordRepository:

	Session = sessionmaker(bind=engine)
	session = Session()

	def save(self, obj):
		self.session.add(obj)
		self.session.commit()

	def save_all(self, obj_list):
		self.session.add_all(obj_list)
		self.session.commit()
