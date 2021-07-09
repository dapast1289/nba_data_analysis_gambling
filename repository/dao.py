#!/user/bin/env python3
# -*- coding: utf-8 -*-
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from repository.nba_repository import MatchInfo
from repository import analysis_record_repository
from repository import per_record_repository
from repository import process_record_repository

# engine = create_engine("mysql+pymysql://root:root@localhost:3306/nba_db_test", echo=True)
engine = create_engine("mysql+pymysql://root:root@localhost:3306/nba_db", echo=False, pool_size=100, max_overflow=2000)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

def init_db():
	analysis_record_repository.Base.metadata.create_all(engine)
	per_record_repository.Base.metadata.create_all(engine)
	process_record_repository.Base.metadata.create_all(engine)


def drop_db():
	analysis_record_repository.Base.metadata.drop_all(engine)
	per_record_repository.Base.metadata.drop_all(engine)
	process_record_repository.Base.metadata.drop_all(engine)


class NbaDao:
	# session = Session()

	# def __init__(self):
		# self.session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
		# self.session = scoped_session(Session())

	def save(self, obj):
		session = Session()
		session.add(obj)
		session.commit()

	def save_all(self, obj_list):
		start_time = time.time()
		session = Session()
		session.add_all(obj_list)
		session.commit()
		end_time = time.time()
		print("spend time to save_all: ", end_time - start_time, "list size:", len(obj_list))
		Session.remove()
	# def close(self):
	# 	self.session.remove()


class MatchInfoRepository:
	session = session_factory()

	def save(self, obj):
		self.session.add(obj)
		self.session.commit()

	def save_all(self, obj_list):
		self.session.add_all(obj_list)
		self.session.commit()

	def query_from_statement(self, season):
		data_list = self.session.query(MatchInfo).filter(MatchInfo.season == season) \
			.order_by(MatchInfo.game_start_time.asc(), MatchInfo.id).all()
		result = []
		index_dic = {}
		temp_result = []
		for idx, data in enumerate(data_list):
			date = data.game_start_time.date()
			if index_dic.get(str(date)) is None:
				# 切換到新日期時，把前一個日期的資料 list 加入 result
				if idx != 0:
					result.append(temp_result)
				temp_result = []
				index_dic[str(date)] = 1
			else:
				# print("index_dic[", str(date), "]:", index_dic[str(date)])
				index_dic[str(date)] = index_dic[str(date)] + 1
			temp_result.append(data)

			if idx == len(data_list) - 1:
				result.append(temp_result)
		return result

# def tt(self):
# 	self.session.query(func.sum(MatchInfo.))

# 1. 撈出該季所有比賽日期，依日期做從小到大排序
# 2. 每日先挑一場比賽做預測數據，如比賽時間兩個半小時後仍有比賽，則納入測量，需做出各種組合測試


class AnalysisRecordRepository:
	session = session_factory()

	def save(self, obj):
		self.session.add(obj)
		self.session.commit()

	def save_all(self, obj_list):
		self.session.add_all(obj_list)
		self.session.commit()
