import sys
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

def int_to_str(number):
    return "{:,}".format(number)

def format_date(date_str, type):
    date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

    if type == 1: result = date.strftime('%d.%m.%Y %H:%M') # 28.01.2004 12:00
    elif type == 2: result = date.strftime('%d.%m.%Y') # 28.01.2004
    return result

def days_since(date_str):
    input_date = datetime.strptime(date_str, '%d.%m.%Y')
    today = datetime.now()
    delta = today - input_date
    rd = relativedelta(today, input_date)
    
    months = rd.months
    days = rd.days
    total_days = delta.days
    
    return f"{months} месяцев {days} дней ({total_days} дня)"
    
def predict_completion(open_date_str, total_amount, collected_amount):
    # Преобразуем дату открытия в объект datetime
    open_date = datetime.strptime(open_date_str, '%Y-%m-%d %H:%M:%S')
    # Текущая дата
    current_date = datetime.now()
    # Разница в днях между текущей датой и датой открытия
    days_elapsed = (current_date - open_date).days

    # Если уже собрали всю сумму
    if collected_amount >= total_amount:
        return "Цель уже достигнута!"

    # Рассчитываем скорость сбора средств (сумма в день)
    collection_rate = collected_amount / days_elapsed if days_elapsed > 0 else 0

    # Рассчитываем оставшуюся сумму
    remaining_amount = total_amount - collected_amount

    # Предполагаемое количество дней для достижения цели
    if collection_rate > 0:
        estimated_days = remaining_amount / collection_rate
    else:
        return "Недостаточно данных для прогноза."

    # Преобразуем дни в месяцы и дни
    estimated_months = estimated_days // 30
    estimated_days = estimated_days % 30

    # Преобразуем месяцы в годы и месяцы
    estimated_years = estimated_months // 12
    remaining_months = estimated_months % 12

    # Формируем результат
    result = ""
    if estimated_years > 0:
        result += f"{int(estimated_years)} года "
    if remaining_months > 0:
        result += f"{int(remaining_months)} месяцев "
    if estimated_days > 0:
        result += f"{int(estimated_days)} дней"
    
    result = f"Примерно <b>{result}</b> потребуется для сбора оставшейся суммы."

    return result.strip()