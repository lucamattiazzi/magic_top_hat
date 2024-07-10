# import os
from datetime import datetime

from dotenv import load_dotenv
from magic_top_hat import (
    get_day_out_of_datetime,
    random_dice_roll,
    random_value_between,
    sum_integers,
)

load_dotenv()
# os.environ["I_DONT_TRUST_ROBOTS"] = "True"


def get_corrected_dice_roll():
    bonus = random_value_between(1, 10)
    print(f"Bonus: {bonus}")
    dice_roll = random_dice_roll()
    print(f"Rolled dice: {dice_roll}")
    total = sum_integers(dice_roll, bonus)
    print(f"Total of dice roll + bonus is {total}")


def get_today_day():
    today = datetime.now()
    day = get_day_out_of_datetime(today)
    print(f"Today is {day}")


if __name__ == "__main__":
    get_corrected_dice_roll()
    get_today_day()
