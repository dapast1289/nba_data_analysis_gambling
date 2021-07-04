#!/user/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, Integer, String, DATETIME, func, Date, FLOAT, Float
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from util import auto_str

Base = declarative_base()


@auto_str
class AnalysisRecord(Base):
	__tablename__ = "analysis_record"
	id = Column("id", Integer, primary_key=True, autoincrement=True)
	season = Column("season", String(255), nullable=False)
	period_days = Column("period_days", Integer, nullable=False)
	thread_id = Column("thread_id", String(255), nullable=False)
	sub_thread_id = Column("sub_thread_id", String(255), nullable=False)
	lose_keyword = Column("lose_keyword", String(255), nullable=False)
	continue_lose_num = Column("continue_lose_num", Integer, nullable=False)
	sample_count = Column("sample_count", Integer, nullable=False)
	sample_count_of_thread = Column("sample_count_of_thread", Integer, nullable=False)
	sample_start_date = Column("sample_start_date", Date, nullable=False)
	sample_end_date = Column("sample_end_date", Date, nullable=False)
	win_count = Column("win_count", Integer, nullable=False)
	lose_count = Column("lose_count", Integer, nullable=False)
	lose_percent = Column("lose_percent", FLOAT, nullable=False)
	win_percent = Column("win_percent", FLOAT, nullable=False)
	cost_of_seconds = Column("cost_of_seconds", FLOAT, nullable=False)
	cost_of_seconds_of_thread = Column("cost_of_seconds_of_thread", FLOAT, nullable=False)
	create_time = Column("create_time", DATETIME, server_default=func.now(), nullable=False)
	update_time = Column("update_time", DATETIME, server_default=func.now(), onupdate=func.now(), nullable=False)
