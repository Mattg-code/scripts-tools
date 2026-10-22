#! /usr/bin/python3
"""
my_utils.py

NAME	EPIC	NUMBER	AVG COST	BOOK	MRKT	% MRKT	P/L

"""
import math
from my_utils import StockDataCols

MAIN_TITLE_LIST=["NAME","EPIC","NUMBER","AVG COST","BOOK","MRKT","% MRKT","P/L"]
TOTALS_TRAILER_LIST=["","","","","BOOK","MRKT","",""]

class PortfolioCols:
    NAME_COL=0
    EPIC_COL=1
    NUM_COL=2
    AVG_COST_COL=3
    BOOK_COL=4
    MRKT_COL=5
    PERC_MRKT_COL=6
    P_L_COL=7

class PortfolioSort:
    ALPHA=0,
    WEIGHT=1,
    P_L=2

"""
@brief build the analysed list
@param epic_map the processed stock datas
@param market_val the total market val
"""
def analysePortfolio(epic_map, market_val):
    analysed = []
    for k, v in epic_map.items():
        num = v[StockDataCols.NUM_COL]
        avg_cost = v[StockDataCols.AVG_COST_COL]        
        bv = (num*avg_cost)/100
        mv = v[StockDataCols.MARKET_VAL_COL]        
        mrk_perc = mv/market_val
        p_l = (mv - bv)/bv

        analysed.append(
            [v[StockDataCols.NAME_COL],
             k,
             round(num,2),
             round(avg_cost,2),
             round(bv,2),
             round(mv,2),
             round(mrk_perc,4),
             round(p_l,4)])
    return analysed

