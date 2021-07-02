#!/user/bin/env python3
# -*- coding: utf-8 -*-
import copy
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from decimal import Decimal
from random import randint
from unicodedata import decimal

import repository.analysis_record_repository
from repository.analysis_record_repository import AnalysisRecord, AnalysisRecordRepository
from repository.nba_repository import MatchInfoRepository


def get_combination(data_list, index=0, result=[]):
	if index == 0:
		for value in data_list[index]:
			temp = [value]
			result.append(temp)

	temp_result = []
	for i in result:
		for j in data_list[index + 1]:
			temp = i.copy()
			temp.append(j)
			temp_result.append(temp)

	result = temp_result
	if index < len(data_list) - 2:
		# call def arrange
		result = get_combination(data_list, index + 1, result)
	return result

# 實際數據測試法
def actually_analysis(combination_list, lose_key, continue_lose_num):

	def is_add_or_odd(game_result):
		total_pts = game_result.visitor_total_pts + game_result.home_total_pts
		if total_pts % 2 == 0:
			return "雙"
		else:
			return "單"

	win_count = 0
	loss_count = 0
	loss_combination = []
	add_count = 0
	odd_count = 0
	for per_combination in combination_list:
		is_loss = False
		numb = continue_lose_num
		for game_result in per_combination:
			if is_add_or_odd(game_result) == lose_key:
				numb -= 1
				add_count += 1
			else:
				odd_count += 1
				numb = continue_lose_num
			if numb == 0:
				is_loss = True
				# loss_combination.append(per_combination)
				break
		if is_loss:
			loss_count += 1
		else:
			win_count += 1
	return {"輸的機率": loss_count / len(combination_list) * 100,
			"贏的機率": win_count / len(combination_list) * 100,
			"單雙總數": add_count + odd_count, "單總數": add_count, "雙總數": odd_count,
			"單機率": add_count / (add_count + odd_count) * 100,
			"雙機率": odd_count / (add_count + odd_count) * 100,
			"輸的條件": "連續出現 " + str(continue_lose_num) + " 次" + lose_key,
			"組合數": len(combination_list)}


# 隨機取樣法
def randon_result_analysis(game_result_list, lose_key, continue_lose_num, randon_sample_count, uuid, consider_ignore_game=False):
	# print(uuid, randon_sample_count)
	def is_add_or_odd(game_result):
		total_pts = game_result.visitor_total_pts + game_result.home_total_pts
		if total_pts % 2 == 0:
			return "雙"
		else:
			return "單"

	win_count = 0
	lose_count = 0
	start_time = time.time()
	for idx in range(randon_sample_count):
		is_loss = False
		numb = continue_lose_num
		for per_game_result in game_result_list:
			choose_idx = randint(0, len(per_game_result) - 1)
			game_result = per_game_result[choose_idx]
			if is_add_or_odd(game_result) == lose_key:
				numb -= 1
			else:
				numb = continue_lose_num
			if numb == 0:
				is_loss = True
				break
		if is_loss:
			lose_count += 1
		else:
			win_count += 1
	end_time = time.time()
	record = AnalysisRecord()
	record.season = game_result_list[0][0].season
	record.period_days = len(game_result_list)
	record.uuid = uuid
	record.lose_keyword = lose_key
	record.continue_lose_num = continue_lose_num
	record.sample_count = randon_sample_count
	record.sample_start_date = game_result_list[0][0].game_start_time.date()
	record.sample_end_date = game_result_list[len(game_result_list)-1][0].game_start_time.date()
	record.win_count = win_count
	record.lose_count = lose_count
	# record.win_percent = str(win_count / (win_count + lose_count) * 100)
	record.win_percent = win_count / (win_count + lose_count) * 100
	# record.lose_percent = str(lose_count / (win_count + lose_count) * 100)
	record.lose_percent = lose_count / (win_count + lose_count) * 100
	record.cost_of_seconds = end_time - start_time
	return record


def test_actually(game_result_list):
	# 計算排列組合
	start_time = time.time()
	game_combination = get_combination(game_result_list)
	end_time = time.time()
	print("比賽天數:", len(game_result_list), "比賽組合數:", len(game_combination), f"{end_time - start_time} 秒計算排列組合")

	# 實際排列組合運算
	actually_combination_test_start = time.time()
	print("實際組合勝負計算", actually_analysis(game_combination, "雙", 4))
	actually_combination_test_end = time.time()
	print(f"{actually_combination_test_end - actually_combination_test_start} 秒計算排列組合")

	# 取樣排列組合運算
	actually_randon_combination_test_start = time.time()
	test_1 = randon_result_analysis(game_result_list, "雙", 4, 1000, uuid.uuid4())
	print("隨機挑選組合勝負計算", str(test_1))
	actually_randon_combination_test_end = time.time()
	print("隨機挑選組合勝負計算", str(randon_result_analysis(game_result_list, "雙", 4, 1000, uuid.uuid4())))
	print("隨機挑選組合勝負計算", str(randon_result_analysis(game_result_list, "雙", 4, 1000, uuid.uuid4())))
	print("隨機挑選組合勝負計算", str(randon_result_analysis(game_result_list, "雙", 4, 500000, uuid.uuid4())))
	print(f"{actually_randon_combination_test_end - actually_randon_combination_test_start} 秒計算排列組合")


def test_randon_case_by_multi_thread(game_result_list, lose_keyword, continue_lose_num, sample_count):
	repository = AnalysisRecordRepository()
	max_threads = 1000
	sample_per_work = []
	divide_sample = sample_count // max_threads
	remain_sample = sample_count % max_threads
	for x in range(max_threads):
		if x == max_threads-1:
			sample_per_work.append(divide_sample+remain_sample)
		else:
			sample_per_work.append(divide_sample)

	with ThreadPoolExecutor(max_workers=max_threads) as executor:
		futures = []
		thread_start_time = time.time()
		total_time = 0
		total_sample = 0
		result_list = []
		for sample in sample_per_work:
			future = executor.submit(randon_result_analysis, game_result_list, lose_keyword,
									 continue_lose_num, sample, uuid.uuid4())
			futures.append(future)
		for future in as_completed(futures):
			total_time += future.result().cost_of_seconds
			total_sample += future.result().sample_count
			result_list.append(copy.copy(future.result()))
			repository.save(future.result())
		thread_end_time = time.time()
		print("thread_time", thread_end_time - thread_start_time)
		print("total_time", total_time)
		print("total_time", total_sample)
		for result in result_list:
			print(type(result.lose_percent))
			print(str(result))

repository.analysis_record_repository.drop_db()
repository.analysis_record_repository.init_db()
# test_actually(game_result_list[0:9])

repository = MatchInfoRepository()
game_result_list_2018 = repository.query_from_statement("2018")
game_result_list_2019 = repository.query_from_statement("2019")
game_result_list_2020 = repository.query_from_statement("2020")
game_result_list_2021 = repository.query_from_statement("2021")

for x in range(1000):
	test_randon_case_by_multi_thread(game_result_list_2018, "雙", 8, 10000000)
	test_randon_case_by_multi_thread(game_result_list_2019, "雙", 8, 10000000)
	test_randon_case_by_multi_thread(game_result_list_2020, "雙", 8, 10000000)
	test_randon_case_by_multi_thread(game_result_list_2021, "雙", 8, 10000000)
	test_randon_case_by_multi_thread(game_result_list_2018, "單", 8, 10000000)
	test_randon_case_by_multi_thread(game_result_list_2019, "單", 8, 10000000)
	test_randon_case_by_multi_thread(game_result_list_2020, "單", 8, 10000000)
	test_randon_case_by_multi_thread(game_result_list_2021, "單", 8, 10000000)
