#! /usr/bin/python3
"""
my_utils.py
"""

def str2int(s):
    try:
        return int(s)
    except:
        return int(s.replace("'", '').replace(',', ''))

def str2float(s):
    try:
        return float(s)
    except:
        return float(s.replace("'", '').replace(',', ''))

class StockDataCols:
    NAME_COL=0
    NUM_COL=1
    AVG_COST_COL=2
    MARKET_VAL_COL=3


