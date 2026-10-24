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

class Criteria:
    TYPES = 0
    REGIONS = 1
    BUSINESS = 2
    
"""
@brief We are parsing this:
TYPES,REGIONS,BUSINESS,
0.UK Share,0.UK,0.Insurance,
1.US Share,1.Global,1.Semiconductors,
2.IT,2.China,2.Software+Analysis,
3.OEIC,3.Japan,3.Retail+Consumer+Books+Fags,
4.European Share,4.India,4.Mining,
5.Cash,5.Vietnam,5.Energy,
.. .. ..
.. .. ..
<blank line is the end>
@param info_lut_f ptr to the CSV file lines
@return tuple(curr_line, tuple(map{int -> string}, , ))

"""    
def parseCategoriesLUTs(info_lut_lines):    
    criteria_names = info_lut_lines[0].split(',')[0:3]
    #print(criteria_names)
    line_no = 1

    type_lut = {}
    region_lut = {}
    business_lut = {}
    
    for line in info_lut_lines:
        blank = True
        criteria_entries = info_lut_lines[line_no].split(',')[0:3]
        entry = criteria_entries[Criteria.TYPES]
        if entry:
            type_entry = entry.split('.')[0:2]
            type_lut[int(type_entry[0])] = type_entry[1]
            blank = False
            
        entry = criteria_entries[Criteria.REGIONS]
        if entry:
            region_entry = entry.split('.')[0:2]
            region_lut[int(region_entry[0])] = region_entry[1]
            blank = False
            
        entry = criteria_entries[Criteria.BUSINESS]
        if entry:
            business_entry = entry.split('.')[0:2]
            business_lut[int(business_entry[0])] = business_entry[1]
            blank = False

        line_no = line_no + 1
        if blank:
            break
            
    return (line_no, (type_lut, region_lut, business_lut))
    
"""
@brief parse

EPIC     	TYPE	REGION	BUSINESS
FOUR	0.UK Share	9.USA	12.Diverse
ADM	0.UK Share	0.UK	0.Insurance
AJB	0.UK Share	0.UK	7.AssetManagement
GOOG	1.US Share	1.Global	9.Tech
AAL	0.UK Share	1.Global	4.Mining
ANTO	0.UK Share	1.Global	4.Mining
ASML	4.European Share	1.Global	1.Semiconductors
AZN	0.UK Share	1.Global	8.Pharmaceutial+HealthCare
BA.	0.UK Share	1.Global	10.Defense
BERI	2.IT	1.Global	5.Energy
BRWM	2.IT	1.Global	4.Mining

@return map: "epic" - > (type, region, business)
"""
def parseEPICcategories(info_lut_lines):
    epic_descriptions = {}
    for description in info_lut_lines:
        cols = description.split(',', 3)
        epic = cols[0]
        type_col = cols[Criteria.TYPES+1].split('.')[0]
        region_col = cols[Criteria.REGIONS+1].split('.')[0]
        business_col = cols[Criteria.BUSINESS+1].split('.')[0]
        try:
            epic_descriptions[epic] = (int(type_col), int(region_col), int(business_col))
        except:
            if epic != "CASH":
                raise
            epic_descriptions[epic] = (int(type_col), -1, -1)

    return epic_descriptions

def categoriseHoldings(info_lut_f, epic_map, total_mv, cash):
    lines = info_lut_f.readlines()
    curr_line_no, category_info_luts = parseCategoriesLUTs(lines)
    
    # advance past the heading
    epic_descriptions = parseEPICcategories(lines[curr_line_no + 1:])
    #for k,v in epic_descriptions.items():
    #    print(f'key={k} val={v}')
    #
    #print(epic_map)        

    mv_less_cash = total_mv - cash

    type_output_bucket = {} # type ix -> accumulating market value
    region_output_bucket = {} # region ix -> accumulating market value
    business_output_bucket = {} # business ix -> accumulating market value

    # enumerate each holding

    

    
    
