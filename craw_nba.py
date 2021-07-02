#!/user/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import time
from concurrent.futures import as_completed, ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup, Comment

from repository.nba_repository import MatchInfo, MatchInfoRepository

domain = "https://www.basketball-reference.com"
season_list = [{"season": "2018", "url": "https://www.basketball-reference.com/leagues/NBA_2018_games.html"},
            {"season": "2019", "url": "https://www.basketball-reference.com/leagues/NBA_2019_games.html"},
            {"season": "2020", "url": "https://www.basketball-reference.com/leagues/NBA_2020_games.html"},
            {"season": "2021", "url": "https://www.basketball-reference.com/leagues/NBA_2021_games.html"}]


def get_page_link_list(soup):
    page_link_list_soup = soup.find(class_="filter").find_all("div")
    page_link_list = []
    for data in page_link_list_soup:
        url = domain + data.a["href"]
        page_link_list.append(url)
    return page_link_list

def get_boxscores_list(url, home_team_name_acronym, visitor_team_name_acronym):
    id = "201804010GSW"
    season = "2018"
    # home_team_name_acronym = "GSW"
    # visitor_team_name_acronym = "IND"
    # request_html = requests.get("https://www.basketball-reference.com/boxscores/201804050IND.html")
    # print("boxerscores", url)
    request_html = requests.get(url)
    soup = BeautifulSoup(request_html.content, "html.parser")
    # print("soup:", soup.prettify())
    data_list_soup = soup.body.find(id="content").find(class_="content_grid").find(id="all_line_score")
    # print("data_list_soup", data_list_soup)
    table_soup = None
    for element in data_list_soup(text=lambda it: isinstance(it, Comment)):
        table_soup = BeautifulSoup(element.extract(), "html.parser").table.tbody.find_all("tr")
    result = {}
    for data in table_soup:
        # print("data", data)
        team_acronym = data.find(attrs={"data-stat": "team"}).string
        team_type = None
        if team_acronym == home_team_name_acronym:
            team_type = "home_"
        elif team_acronym == visitor_team_name_acronym:
            team_type = "visitor_"
        team_href = data.find(attrs={"data-stat": "team"}).a["href"]
        first = data.find(attrs={"data-stat": "1"}).string
        second = data.find(attrs={"data-stat": "2"}).string
        third = data.find(attrs={"data-stat": "3"}).string
        fourth = data.find(attrs={"data-stat": "4"}).string
        over_time_soup = data.find(attrs={"data-stat": "1OT"})
        over_time = None
        if over_time_soup is not None:
            over_time = over_time_soup.string
        total = data.find(attrs={"data-stat": "T"}).string

        result[team_type+"first_pts"] = first
        result[team_type+"second_pts"] = second
        result[team_type+"third_pts"] = third
        result[team_type+"fourth_pts"] = fourth
        result[team_type+"over_time_pts"] = over_time
        result[team_type+"total_pts"] = total
    #     print(id, season, team_acronym, team_href, first, second, third, fourth, over_time, total)
    # print(result)
    return result


def get_data_list(season, soup):
    data_list_soup = soup.find(id="schedule").tbody.find_all("tr")

    nba_entity_list = []
    x = 1
    for data in data_list_soup:
        # print(x, ": ", data)
        if data.th.string == "Playoffs":
            continue
        match_id = data.find(attrs={"data-stat": "date_game"})["csk"]
        year = match_id[0:4]
        month = match_id[4:6]
        day = match_id[6:8]
        date_game_href = data.find(attrs={"data-stat": "date_game"}).a["href"]

        # datetime()
        game_start_time = None
        time_ori = data.find(attrs={"data-stat": "game_start_time"}).string
        if time_ori is not None:
            time_arr = time_ori[0:len(time_ori)-1].split(":")
            hour = time_arr[0]
            minute = time_arr[1]
            game_start_time = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), 0, 0)

        visitor_team_name_href = data.find(attrs={"data-stat": "visitor_team_name"}).a["href"]
        visitor_team_name = data.find(attrs={"data-stat": "visitor_team_name"}).a.string
        visitor_team_name_acronym = visitor_team_name_href.split("/")[2]
        visitor_pts_html = data.find(attrs={"data-stat": "visitor_pts"}).string
        visitor_pts = None
        if visitor_pts_html is not None:
            visitor_pts = int(visitor_pts_html)
        home_team_name_href = data.find(attrs={"data-stat": "home_team_name"}).a["href"]
        home_team_name = data.find(attrs={"data-stat": "home_team_name"}).a.string
        home_team_name_acronym = home_team_name_href.split("/")[2]
        home_pts_html = data.find(attrs={"data-stat": "home_pts"}).string
        home_pts = None
        if home_pts_html is not None:
            home_pts = int(home_pts_html)

        box_score_text_href_html = data.find(attrs={"data-stat": "box_score_text"}).a
        box_score_text_href = None
        box_score_text = None
        boxscores_list = None
        if box_score_text_href_html is not None:
            box_score_text_href = box_score_text_href_html["href"]
            box_score_text = box_score_text_href_html.string
            # calculate home and visitor pts
            boxscores_list = get_boxscores_list(domain+box_score_text_href, home_team_name_acronym, visitor_team_name_acronym)


        overtimes = data.find(attrs={"data-stat": "overtimes"}).string
        attendance = data.find(attrs={"data-stat": "attendance"}).string
        game_remarks = data.find(attrs={"data-stat": "game_remarks"}).string
        x = x + 1

        if visitor_pts is not None and home_pts is not None and boxscores_list is not None:
            entity = MatchInfo(season=season, match_id=match_id, game_start_time=game_start_time,
                               date_game_href=date_game_href, visitor_team_name_acronym=visitor_team_name_acronym,
                               visitor_team_name=visitor_team_name, visitor_team_name_href=visitor_team_name_href,
                               visitor_first_pts=boxscores_list["visitor_first_pts"],
                               visitor_second_pts=boxscores_list["visitor_second_pts"],
                               visitor_third_pts=boxscores_list["visitor_third_pts"],
                               visitor_fourth_pts=boxscores_list["visitor_fourth_pts"],
                               visitor_over_time_pts=boxscores_list["visitor_over_time_pts"],
                               visitor_total_pts=boxscores_list["visitor_total_pts"],
                               home_team_name_acronym=home_team_name_acronym,
                               home_team_name=home_team_name, home_team_name_href=home_team_name_href,
                               home_first_pts=boxscores_list["home_first_pts"],
                               home_second_pts=boxscores_list["home_second_pts"],
                               home_third_pts=boxscores_list["home_third_pts"],
                               home_fourth_pts=boxscores_list["home_fourth_pts"],
                               home_over_time_pts=boxscores_list["home_over_time_pts"],
                               home_total_pts=boxscores_list["home_total_pts"],
                               box_score_text=box_score_text, box_score_text_href=box_score_text_href,
                               overtimes=overtimes, attendance=attendance, game_remarks=game_remarks)
            # print(entity)
            nba_entity_list.append(entity)

    return nba_entity_list

def craw_page_link(rep, data, page_link):
    print("parser link:", page_link)
    request_html = requests.get(page_link)
    soup = BeautifulSoup(request_html.content, "html.parser")
    nba_entity_list = get_data_list(data["season"], soup)
    rep.save_all(nba_entity_list)

def craw_and_save(season_list):
    print("parser start")
    rep = MatchInfoRepository()
    for data in season_list:
        print("parser url:", data["url"])
        main_request_html = requests.get(data["url"])
        main_soup = BeautifulSoup(main_request_html.content, "html.parser")
        page_link_list = get_page_link_list(main_soup)

        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = []
            for link in page_link_list:
                future = executor.submit(craw_page_link, rep, data, link)
                futures.append(future)
                print(type(future))
            for future in as_completed(futures):
                print(future.result())
        # for page_link in page_link_list:
            # print("parser link:", page_link)
            # request_html = requests.get(page_link)
            # soup = BeautifulSoup(request_html.content, "html.parser")
            # nba_entity_list = get_data_list(data["season"], soup)
            # rep.save_all(nba_entity_list)

start_time = time.time()
# craw_and_save(season_list)
end_time = time.time()
# get_boxscores_list()

print(f"{end_time - start_time} 秒爬取文章")