import math

NUM_OF_VULNS = 44

propotion_table = {
    1: 2.2727,
    2: 4.5455,
    3: 6.8182,
    4: 9.0909,
    5: 11.3636,
    6: 13.6364,
    7: 15.9091,
    8: 18.1818,
    9: 20.4545,
    10: 22.7273,
    11: 25.0,
    12: 27.2727,
    13: 29.5455,
    14: 31.8182,
    15: 34.0909,
    16: 36.3636,
    17: 38.6364,
    18: 40.9091,
    19: 43.1818,
    20: 45.4545,
    21: 47.7273,
    22: 50.0,
    23: 52.2727,
    24: 54.5455,
    25: 56.8182,
    26: 59.0909,
    27: 61.3636,
    28: 63.6364,
    29: 65.9091,
    30: 68.1818,
    31: 70.4545,
    32: 72.7273,
    33: 75.0,
    34: 77.2727,
    35: 79.5455,
    36: 81.8182,
    37: 84.0909,
    38: 86.3636,
    39: 88.6364,
    40: 90.9091,
    41: 93.1818,
    42: 95.4545,
    43: 97.7273,
    44: 100.0,
}


def propotion(num: int):
    return round(num / NUM_OF_VULNS * 100, 4)


def avg(nums: list):
    return sum(nums) / len(nums)


def avg_num_and_propo(nums: list):
    return {
        "avg_num": math.floor(avg(nums)),
        "propo": {
            nums[0]: propotion_table[nums[0]],
            nums[1]: propotion_table[nums[1]],
            nums[2]: propotion_table[nums[2]],
            "avg_propo": round(avg([propotion(num) for num in nums]), 4),
        },
    }


print(avg_num_and_propo([4, 2, 5]))
