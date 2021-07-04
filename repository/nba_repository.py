#!/user/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, Integer, String, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from util import auto_str

Base = declarative_base()


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
