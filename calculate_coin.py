#!/user/bin/env python3
# -*- coding: utf-8 -*-
import time
from random import randint

from calculate import get_combination


def actually_analysis_for_coin(combination_list, lose_key, continue_lose_num):
	win_count = 0
	loss_count = 0
	loss_combination = []
	front_count = 0
	back_count = 0
	for per_combination in combination_list:
		is_loss = False
		numb = continue_lose_num
		for coin in per_combination:
			if coin == lose_key:
				numb = numb - 1
				front_count += 1
			else:
				back_count += 1
				numb = continue_lose_num
			if numb == 0:
				is_loss = True
				loss_combination.append(per_combination)
		if is_loss:
			loss_count += 1
		else:
			win_count += 1
	return {"正反面數": front_count + back_count, "正面數": front_count, "反面數": back_count,
			"正面機率": front_count / (front_count + back_count) * 100,
			"反面機率": back_count / (front_count + back_count) * 100,
			"輸的條件": "連續出現 " + str(continue_lose_num) + " 次" + lose_key,
			"輸的機率": loss_count / len(combination_list) * 100,
			"贏的機率": win_count / len(combination_list) * 100,
			"組合數": len(combination_list)}


def randon_result_analysis_for_coin(result_list, lose_key, continue_lose_num, run_numb):
	win_count = 0
	loss_count = 0
	for idx in range(run_numb):
		is_loss = False
		numb = continue_lose_num
		for per_result in result_list:
			a = per_result[randint(0, len(per_result) - 1)]
			if a == lose_key:
				numb -= 1
			else:
				numb = continue_lose_num
			if numb == 0:
				is_loss = True
		if is_loss:
			loss_count += 1
		else:
			win_count += 1
	return {"必輸機率": loss_count / (win_count + loss_count) * 100,
			"必贏機率": win_count / (win_count + loss_count) * 100,
			"輸的條件": "連續出現 " + str(continue_lose_num) + " 次" + lose_key,
			"測試次數": run_numb}


coin = [["正", "反"], ["正", "反", "反", "反"], ["正", "反", "反"], ["正", "反"]]
coin_combination = get_combination(coin)
print("組合列表:", coin_combination)
print("組合數:", len(coin_combination))
print("實際組合測試:", actually_analysis_for_coin(coin_combination, "正", 2))
start_time = time.time()
print("隨機抽取組合測試:", randon_result_analysis_for_coin(coin, "正", 2, 5000000))
end_time = time.time()
print(f"{end_time - start_time} 秒計算排列組合")