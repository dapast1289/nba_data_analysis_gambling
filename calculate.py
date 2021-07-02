#!/user/bin/env python3
# -*- coding: utf-8 -*-
import time
from random import randint

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


def actually_analysis(combination_list, lose_key, continue_lose_num):

	def lose_argument(game_result):
		total_pts = game_result.visitor_total_pts + game_result.home_total_pts
		is_odd = False
		if total_pts % 2 == 0:
			is_odd = True
		if lose_key == "單":
			return is_odd == False
		elif lose_key == "雙":
			return is_odd == True

	win_count = 0
	loss_count = 0
	loss_combination = []
	add_count = 0
	odd_count = 0
	for per_combination in combination_list:
		is_loss = False
		numb = continue_lose_num
		for game_result in per_combination:
			if lose_argument(game_result):
				numb = numb - 1
				add_count += 1
			else:
				odd_count += 1
				numb = continue_lose_num
			if numb == 0:
				is_loss = True
				loss_combination.append(per_combination)
		if is_loss:
			loss_count += 1
		else:
			win_count += 1
	return {"單雙數": add_count + odd_count, "單數": add_count, "雙數": odd_count,
			"單機率": add_count / (add_count + odd_count) * 100,
			"雙機率": odd_count / (add_count + odd_count) * 100,
			"輸的條件": "連續出現 " + str(continue_lose_num) + " 次" + lose_key,
			"輸的機率": loss_count / len(combination_list) * 100,
			"贏的機率": win_count / len(combination_list) * 100,
			"組合數": len(combination_list)}


def randon_result_analysis(game_result_list, lose_key, continue_lose_num, run_numb, consider_ignore_game=False):
	def lose_argument(game_result):
		total_pts = game_result["visitor_total_pts"] + game_result["home_total_pts"]
		is_odd = False
		if total_pts % 2 == 0:
			is_odd = True
		if lose_key == "單":
			return is_odd == False
		elif lose_key == "雙":
			return is_odd == True

	win_count = 0
	loss_count = 0
	for idx in range(run_numb):
		is_loss = False
		numb = continue_lose_num
		for per_game_result in game_result_list:
			choose_idx = randint(0, len(per_game_result) - 1)
			game_result = per_game_result[choose_idx]
			if lose_argument(game_result):
				numb -= 1
			else:
				numb = continue_lose_num
		if is_loss:
			loss_count += 1
		else:
			win_count += 1
	return {"必輸機率": loss_count / (win_count + loss_count) * 100,
			"必贏機率": win_count / (win_count + loss_count) * 100,
			"輸的條件": "連續出現 " + str(continue_lose_num) + " 次" + lose_key,
			"測試次數": run_numb}


repository = MatchInfoRepository()
game_result_list = repository.query_from_statement("2018")
print("比賽天數:", len(game_result_list[0:3]))
start_time = time.time()
game_combination = get_combination(game_result_list[0:3])
end_time = time.time()
print("比賽組合數:", len(game_combination))
print(f"{end_time - start_time} 秒計算排列組合")
for d in game_combination:
	temp = []
	for a in d:
		re = (a.visitor_total_pts + a.home_total_pts) % 2
		if re == 0:
			temp.append("雙")
		else:
			temp.append("單")
	print(temp)

print(actually_analysis(game_combination, "雙", 2))

