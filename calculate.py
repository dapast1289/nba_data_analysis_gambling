#!/user/bin/env python3
# -*- coding: utf-8 -*-
import math
import os
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import Manager
from random import randint

import repository.analysis_record_repository
from repository.analysis_record_repository import AnalysisRecord
from repository.dao import MatchInfoRepository, AnalysisRecordRepository, NbaDao
from repository.per_record_repository import PerRecord
from repository.process_record_repository import ProcessRecord


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
def randon_result_analysis(game_result_list, lose_key, continue_lose_num, randon_sample_count, thread_id,
						   sub_thread_id):
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
	record.thread_id = thread_id
	record.sub_thread_id = sub_thread_id
	record.lose_keyword = lose_key
	record.continue_lose_num = continue_lose_num
	record.sample_count = randon_sample_count
	record.sample_start_date = game_result_list[0][0].game_start_time.date()
	record.sample_end_date = game_result_list[len(game_result_list) - 1][0].game_start_time.date()
	record.win_count = win_count
	record.lose_count = lose_count
	record.win_percent = win_count / (win_count + lose_count) * 100
	record.lose_percent = lose_count / (win_count + lose_count) * 100
	record.cost_of_seconds = end_time - start_time
	return record


# TODO
def randon_result_analysis_by_process(game_result_list, lose_key, continue_lose_num, random_sample_count, process_id):
	def is_add_or_odd(game_result):
		total_pts = game_result.visitor_total_pts + game_result.home_total_pts
		if total_pts % 2 == 0:
			return "雙"
		else:
			return "單"

	odds = 0.97
	win_count = 0
	lose_count = 0
	per_record_list = []
	for i in random_sample_count:
		init_money = 35000
		money = init_money
		gambling_money = 100
		double_money_if_lose = 2.1
		start_time = time.time()
		is_loss = False
		numb = continue_lose_num
		day = 1
		for idx, per_game_result in enumerate(game_result_list):
			choose_idx = randint(0, len(per_game_result) - 1)
			game_result = per_game_result[choose_idx]
			if is_add_or_odd(game_result) == lose_key:
				numb -= 1
				# 輸了扣錢
				money -= gambling_money
				# 計算下一把賭金
				gambling_money = math.ceil(gambling_money * double_money_if_lose)
			else:
				# 計算贏多少錢
				win_money = math.ceil(gambling_money * odds)
				# 加回現金
				money += win_money
				numb = continue_lose_num
			if numb == 0:
				# 出局
				is_loss = True
				day += idx
				break
			elif numb == continue_lose_num and idx + numb > len(game_result_list):
				# 如果目前沒輸任何一場且剩餘場數不滿連輸場次，則退出比賽
				day += idx
				break
		if is_loss:
			lose_count += 1
		else:
			win_count += 1
		end_time = time.time()
		per_record = PerRecord()
		per_record.process_id = process_id
		per_record.season = game_result_list[0][0].season
		per_record.period_days = day
		per_record.lose_keyword = lose_key
		per_record.continue_lose_num = continue_lose_num
		per_record.sample_start_date = game_result_list[0][0].game_start_time.date()
		per_record.sample_end_date = game_result_list[0][day - 1].game_start_time.date()
		per_record.gambling_result = is_loss
		per_record.init_money = init_money
		per_record.balance_money = money - init_money
		per_record.finally_money = money
		per_record.cost_of_seconds = end_time - start_time
		per_record_list.append(per_record)
	return per_record_list


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


def assign_samples_to_each_work(sample_count, max_works):
	sample_per_work = []
	divide_sample = sample_count // max_works
	remain_sample = sample_count % max_works
	for idx_work in range(max_works):
		if idx_work == max_works - 1:
			sample_per_work.append(divide_sample + remain_sample)
		else:
			sample_per_work.append(divide_sample)
	return sample_per_work


def test_randon_case_by_multi_thread(thread_id, game_result_list, lose_keyword, continue_lose_num, sample_count):
	print("test_randon_case_by_multi_thread(", thread_id, game_result_list, lose_keyword, continue_lose_num,
		  sample_count, ")")
	max_threads = 100
	sample_per_work = assign_samples_to_each_work(sample_count, max_threads)
	# analysis_record_repository = AnalysisRecordRepository()
	analysis_record_repository = NbaDao()
	with ThreadPoolExecutor(max_workers=max_threads) as executor:
		futures = []
		thread_start_time = time.time()
		total_time = 0
		total_sample = 0
		result_list = []
		for index, sample in enumerate(sample_per_work):
			sub_thread_id = str(thread_id) + "-" + str(index)
			future = executor.submit(randon_result_analysis, game_result_list, lose_keyword, continue_lose_num, sample,
									 thread_id, sub_thread_id)
			futures.append(future)
		for future in as_completed(futures):
			total_time += future.result().cost_of_seconds
			total_sample += future.result().sample_count
			result_list.append(future.result())
		thread_end_time = time.time()
		for result in result_list:
			result.sample_count_of_thread = total_sample
			result.cost_of_seconds_of_thread = thread_end_time - thread_start_time
		analysis_record_repository.save_all(result_list)


# TODO
def write(q, game_result_list, lose_keyword, continue_lose_num, sample, process_id, sub_process_id, lock):
	per_record_list = randon_result_analysis_by_process(game_result_list, lose_keyword, continue_lose_num, sample,
														process_id + str(os.getpid()), sub_process_id)
	lock.acquire()  # 加上鎖
	win_count = 0
	lose_count = 0
	for record in per_record_list:
		if record.gambling_result:
			win_count += 1
		else:
			lose_count += 1
	process = ProcessRecord()
	process.process_id
	process.season
	process.period_days
	process.lose_keyword
	process.continue_lose_num
	process.sample_count_of_thread
	process.sample_start_date
	process.sample_end_date
	process.win_count = win_count
	process.lose_count = lose_count
	process.win_percent = win_count / (win_count + lose_count)
	process.lose_percent = lose_count / (win_count + lose_count)
	process.cost_of_seconds
	q.put(process)
	lock.release()  # 釋放鎖


def test_randon_case_by_multi_process(process_id, game_result_list, lose_keyword, continue_lose_num, sample_count):
	print("test_randon_case_by_multi_process(", process_id, game_result_list, lose_keyword, continue_lose_num,
		  sample_count, ")")
	sample_per_work = assign_samples_to_each_work(sample_count, max_works=8)
	analysis_record_repository = NbaDao()
	with Manager() as manager:
		dict = manager.dict()
		q = manager.Queue()
		lock = manager.Lock()  # 初始化一把鎖
		p = Pool()
		pw = p.apply_async(write, args=(q, lock))
		pr = p.apply_async(read, args=(q,))

		l = manager.list(range(10))

	with ThreadPoolExecutor(max_workers=len(sample_per_work)) as executor:
		futures = []
		thread_start_time = time.time()
		total_time = 0
		total_sample = 0
		result_list = []
		for index, sample in enumerate(sample_per_work):
			sub_thread_id = str(process_id) + "-" + str(index)
			future = executor.submit(randon_result_analysis, game_result_list, lose_keyword, continue_lose_num, sample,
									 process_id, sub_thread_id)
			futures.append(future)
		for future in as_completed(futures):
			total_time += future.result().cost_of_seconds
			total_sample += future.result().sample_count
			result_list.append(future.result())
		thread_end_time = time.time()
		for result in result_list:
			result.sample_count_of_thread = total_sample
			result.cost_of_seconds_of_thread = thread_end_time - thread_start_time
		analysis_record_repository.save_all(result_list)


if __name__ == '__main__':
	repository.dao.drop_db()
	repository.dao.init_db()
	# test_actually(game_result_list[0:9])

	match_info_repository = MatchInfoRepository()
	game_result_list_2018 = match_info_repository.query_from_statement("2018")
	game_result_list_2019 = match_info_repository.query_from_statement("2019")
	game_result_list_2020 = match_info_repository.query_from_statement("2020")
	game_result_list_2021 = match_info_repository.query_from_statement("2021")

	sample_num = 10000
	for x in range(1):
		test_randon_case_by_multi_thread(uuid.uuid4(), game_result_list_2018, "雙", 8, sample_num)
		test_randon_case_by_multi_thread(uuid.uuid4(), game_result_list_2019, "雙", 8, sample_num)
		test_randon_case_by_multi_thread(uuid.uuid4(), game_result_list_2020, "雙", 8, sample_num)
		test_randon_case_by_multi_thread(uuid.uuid4(), game_result_list_2021, "雙", 8, sample_num)
		test_randon_case_by_multi_thread(uuid.uuid4(), game_result_list_2018, "單", 8, sample_num)
		test_randon_case_by_multi_thread(uuid.uuid4(), game_result_list_2019, "單", 8, sample_num)
		test_randon_case_by_multi_thread(uuid.uuid4(), game_result_list_2020, "單", 8, sample_num)
		test_randon_case_by_multi_thread(uuid.uuid4(), game_result_list_2021, "單", 8, sample_num)
