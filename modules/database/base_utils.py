import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
import settings
import functions
from SqlCode import db, dbmanager

class BaseUtils:
    def __init__(self, bot):
        self.bot = bot

    async def safe_information_str(self, safe_id):
        cacheresult = dbmanager.get_safe_information(db, safe_id)
        if cacheresult.strip() == json.dumps([]):
            result = "Ошибка 1"
            return result
        safe_list = json.loads(cacheresult)

        result = f"<b>{safe_list[0]['safe_name']}</b>\n"
        result += f"Дата создания копилки: <b>{safe_list[0]['safe_created']}</b>\n"
        result += f"Длительность сбора: <b>{safe_list[0]['safe_difference']}</b>\n\n"

        balance = safe_list[0]['safe_balance']
        aimsum = safe_list[0]['safe_aimsum']
        result += f"Общая сумма сбора: <b>{functions.int_to_str(aimsum)} {safe_list[0]['safe_valute']}</b>\n"
        result += f"Собрано: <b>{functions.int_to_str(balance)} {safe_list[0]['safe_valute']}</b>\n"
        if balance >= aimsum: result += f"Поздравляем! Вы перевыполнили цель на: <b>{functions.int_to_str(balance-aimsum)} {safe_list[0]['safe_valute']}</b>\n"
        else: 
            result += f"Осталось собрать: <b>{functions.int_to_str(aimsum-balance)} {safe_list[0]['safe_valute']}</b>\n"
            result += f"{functions.predict_completion(safe_list[0]['safe_created_py'], aimsum, balance)}"

        return result

    async def add_cash_to_safe(self, safe_id, summ):
        cacheresult = dbmanager.get_safe_information(db, safe_id)
        if cacheresult.strip() == json.dumps([]):
            result = "Ошибка 2"
            return result

        safe_list = json.loads(cacheresult)

        result = f"<b>{safe_list[0]['safe_name']}</b>\n"

        balance = safe_list[0]['safe_balance'] + summ
        aimsum = safe_list[0]['safe_aimsum']

        result += f"Копилка успешно пополнена на <b>{functions.int_to_str(summ)} {safe_list[0]['safe_valute']}!</b>\n"
        result += f"Баланс до: <b>{functions.int_to_str(balance-summ)} {safe_list[0]['safe_valute']}</b>\n"
        result += f"Баланс после: <b>{functions.int_to_str(balance)} {safe_list[0]['safe_valute']}</b>\n\n"

        if balance >= aimsum: result += f"Поздравляем! Вы перевыполнили цель на: <b>{functions.int_to_str(balance-aimsum)} {safe_list[0]['safe_valute']}</b>\n"
        else: result += f"Осталось собрать: <b>{functions.int_to_str(aimsum-balance)} {safe_list[0]['safe_valute']}</b>\n"

        dbmanager.add_safe_balance(db, summ, safe_id)
        return result

    async def take_cash_from_safe(self, safe_id, summ):
        cacheresult = dbmanager.get_safe_information(db, safe_id)
        if cacheresult.strip() == json.dumps([]):
            result = "Ошибка 2"
            return result

        safe_list = json.loads(cacheresult)

        result = f"<b>{safe_list[0]['safe_name']}</b>\n"

        balance = safe_list[0]['safe_balance'] - summ
        aimsum = safe_list[0]['safe_aimsum']

        result += f"Вы успешно сняли с копилки <b>{functions.int_to_str(summ)} {safe_list[0]['safe_valute']} 😔</b>\n"
        result += f"Баланс до: <b>{functions.int_to_str(balance+summ)} {safe_list[0]['safe_valute']}</b>\n"
        result += f"Баланс после: <b>{functions.int_to_str(balance)} {safe_list[0]['safe_valute']}</b>\n\n"

        if balance >= aimsum: result += f"Поздравляем! Вы перевыполнили цель на: <b>{functions.int_to_str(balance-aimsum)} {safe_list[0]['safe_valute']}</b>\n"
        else: result += f"Осталось собрать: <b>{functions.int_to_str(aimsum-balance)} {safe_list[0]['safe_valute']}</b>\n"

        dbmanager.take_safe_balance(db, summ, safe_id)
        return result

    async def set_safe_name(self, safe_id, name):
        cacheresult = dbmanager.get_safe_information(db, safe_id)
        if cacheresult.strip() == json.dumps([]):
            result = "Ошибка 2"
            return result

        safe_list = json.loads(cacheresult)

        result = f"<b>{safe_list[0]['safe_name']} -> {name}</b>\n"

        balance = safe_list[0]['safe_balance']
        aimsum = safe_list[0]['safe_aimsum']

        result += f"Баланс копилки: <b>{functions.int_to_str(balance)} {safe_list[0]['safe_valute']}</b>\n\n"

        if balance >= aimsum: result += f"Поздравляем! Вы перевыполнили цель на: <b>{functions.int_to_str(balance-aimsum)} {safe_list[0]['safe_valute']}</b>\n"
        else: result += f"Осталось собрать: <b>{functions.int_to_str(aimsum-balance)} {safe_list[0]['safe_valute']}</b>\n"

        dbmanager.set_safe_name_db(db, name, safe_id)
        return result