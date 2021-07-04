#!/user/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import repository
from repository.nba_repository import MatchInfo

# engine = create_engine("mysql+pymysql://root:root@localhost:3306/nba_db_test", echo=True)
engine = create_engine("mysql+pymysql://root:root@localhost:3306/nba_db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()


def init_db():
	repository.analysis_record_repository.Base.metadata.create_all(engine)


def drop_db():
	repository.analysis_record_repository.Base.metadata.drop_all(engine)


class MatchInfoRepository:

	def save(self, obj):
		session.add(obj)
		session.commit()

	def save_all(self, obj_list):
		session.add_all(obj_list)
		session.commit()

	def query_from_statement(self, season):
		data_list = session.query(MatchInfo).filter(MatchInfo.season == season) \
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

	def save(self, obj):
		session.add(obj)
		session.commit()

	def save_all(self, obj_list):
		session.add_all(obj_list)
		session.commit()
