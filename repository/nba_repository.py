#!/user/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, Integer, String, DATETIME
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
class MatchInfo(Base):
	__tablename__ = "match_info"
	id = Column("id", Integer, primary_key=True, autoincrement=True)
	season = Column("season", String(255))
	match_id = Column("match_id", String(255))
	game_start_time = Column("game_start_time", DATETIME)
	date_game_href = Column("date_game_href", String(255))
	visitor_team_name_acronym = Column("visitor_team_name_acronym", String(255))
	visitor_team_name = Column("visitor_team_name", String(255))
	visitor_team_name_href = Column("visitor_team_name_href", String(255))
	visitor_first_pts = Column("visitor_first_pts", Integer)
	visitor_second_pts = Column("visitor_second_pts", Integer)
	visitor_third_pts = Column("visitor_third_pts", Integer)
	visitor_fourth_pts = Column("visitor_fourth_pts", Integer)
	visitor_over_time_pts = Column("visitor_over_time_pts", Integer)
	visitor_total_pts = Column("visitor_total_pts", Integer)
	home_team_name_acronym = Column("home_team_name_acronym", String(255))
	home_team_name = Column("home_team_name", String(255))
	home_team_name_href = Column("home_team_name_href", String(255))
	home_first_pts = Column("home_first_pts", Integer)
	home_second_pts = Column("home_second_pts", Integer)
	home_third_pts = Column("home_third_pts", Integer)
	home_fourth_pts = Column("home_fourth_pts", Integer)
	home_over_time_pts = Column("home_over_time_pts", Integer)
	home_total_pts = Column("home_total_pts", Integer)
	box_score_text = Column("box_score_text", String(255))
	box_score_text_href = Column("box_score_text_href", String(255))
	overtimes = Column("overtimes", String(255))
	attendance = Column("attendance", String(255))
	game_remarks = Column("game_remarks", String(255))


def init_db():
	Base.metadata.create_all(engine)


def drop_db():
	Base.metadata.drop_all(engine)


class MatchInfoRepository:
	# Base.metadata.drop_all(engine)
	# Base.metadata.create_all(engine)

	Session = sessionmaker(bind=engine)
	session = Session()

	def save(self, obj):
		self.session.add(obj)
		self.session.commit()

	def save_all(self, obj_list):
		self.session.add_all(obj_list)
		self.session.commit()

	# "SELECT * FROM users where name=:name"
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
# 3.
# 4.
# 5.
# 6.
# 7.
