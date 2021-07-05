#!/user/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Integer, Column, String, Date, func, BOOLEAN
from sqlalchemy.dialects.mysql import FLOAT, DATETIME
from sqlalchemy.orm import declarative_base

from util import auto_str

Base = declarative_base()


@auto_str
class PerRecord(Base):
	__tablename__ = "per_record"
	id = Column("id", Integer, primary_key=True, autoincrement=True)
	process_id = Column("process_id", String(255), nullable=False)
	season = Column("season", String(255), nullable=False)
	period_days = Column("period_days", Integer, nullable=False)
	lose_keyword = Column("lose_keyword", String(255), nullable=False)
	continue_lose_num = Column("continue_lose_num", Integer, nullable=False)
	sample_start_date = Column("sample_start_date", Date, nullable=False)
	sample_end_date = Column("sample_end_date", Date, nullable=False)
	is_loss = Column("is_loss", BOOLEAN, nullable=False)
	init_money = Column("init_money", Integer, nullable=False)
	balance_money = Column("balance_money", Integer, nullable=False)
	finally_money = Column("finally_money", Integer, nullable=False)
	cost_of_seconds = Column("cost_of_seconds", FLOAT, nullable=False)
	create_time = Column("create_time", DATETIME, server_default=func.now(), nullable=False)
	update_time = Column("update_time", DATETIME, server_default=func.now(), onupdate=func.now(), nullable=False)