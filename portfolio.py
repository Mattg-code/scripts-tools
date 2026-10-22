#! /usr/bin/python3
"""
Portfolio analysis tool
See if this changes

cat figures.txt | ./portfolio.py -c 18708.76

"""
# main program

import sys
import argparse
import copy

from my_utils import str2float, str2int, StockDataCols
from analysis import analysePortfolio, MAIN_TITLE_LIST, TOTALS_TRAILER_LIST
from analysis import PortfolioCols

TAB=0x9
LF=0xa
MAX_ASCII=127

class TabbedCols:
    NAME_EPIC_TAB=0
    NUM_TAB=1
    AVG_COST_TAB=2
    # book val can be computed later
    BOOK_VAL_TAB=3
    # curr cost SP is ignored
    CURR_COST_TAB=4
    MARKET_VAL_TAB=5

"""
@brief 
@param lst holdings list
@param total_bv book value
@param total_mv mrkt value
@param csv csv output
@param show_title print the heading a.k.a. title if true
@param show_median 
"""
def displayHoldingList(
        lst,
        total_bv,
        total_mv,
        csv=True,
        show_title=False,
        show_median=False):
    # assume csv output for now

    if show_title:
        heading = ''
        col_num = 0
        for col_heading in MAIN_TITLE_LIST:
            justify_by = 9 if col_num<PortfolioCols.MRKT_COL else 12
            heading = heading + col_heading.ljust(justify_by) + ','
            col_num = col_num + 1
        print(heading)

    median_mrkt_val = 0.0
    median_ix = 0
    if show_median:
        # deduce median row ix.
        
        adjusted_count = len(lst) if len(lst) % 2 else len(lst) + 1
        median_ix = int(adjusted_count/2)
        median_mrkt_val = lst[median_ix][PortfolioCols.MRKT_COL]
        if 0.0 == median_mrkt_val:
            raise ValueError("WTF? Median mrkt val should not be 0.0!!")

    row_num = 0    
    for ll in lst:
        line = ''
        for col in ll:
            line = line + str(col) + ','

        if show_median:
            median_x = ll[PortfolioCols.MRKT_COL] / median_mrkt_val
            median_x = f"{median_x:.2f}x"
            line = line + median_x.rjust(6) + ','
            if median_ix == row_num:
                line = line + " median ,"                
            row_num = row_num + 1
                
        print(line)            
            
    trailer = copy.deepcopy(TOTALS_TRAILER_LIST)
    trailer[PortfolioCols.BOOK_COL] = round(total_bv, 2)
    trailer[PortfolioCols.MRKT_COL] = round(total_mv, 2)
    line = ''
    for col in trailer:
        line = line + str(col) + ','
    print(line)

    line = ''
    for col in trailer:
        line = line + ','
    print(line)
    
"""
@brief Using the brackets split out the name and epic from the first tabbed
field
@param data first field in tabbed collections
@returns tuple (epic, name)
"""
def extractNameEpic(data):
    work = data.split('(')
    name = work[0].rstrip()
    work = work[1]
    epic = work.split(')')[0]
    return (epic, name)

"""
@brief Use the existing cost/number in stock data instance and the one just
read from the current holding line to accumulate new
@param existing_num the existing number held from the stock data instance
@param existing_cost the existing cost held from the stock data instance
@param new_num the value extracted from the currently processed line
@param new_cost the value extracted from the currently process line
@returns tuple of the latest (num, cost)
"""
def accumulateCountAndCost(existing_num, existing_cost, new_num, new_cost):
    if 0 == existing_num:
        return (new_num, new_cost)

    bk_val1 = existing_num * existing_cost
    bk_val2 = new_num * new_cost

    new_num = new_num + existing_num
    return (new_num, (bk_val1 + bk_val2)/new_num)    

"""
@brief High level file parse
@param line current line
@param epic_map the current epic_map
@returns the (new_map, book_value_for_this_row, market_value_for_this_row)

epic -> [name, number, avgcost, market]
"""
def extractTabbedData(line, epic_map):
    cur_tab_stop=0
    data=''
    cur_epic=''
    cur_num_shares=0
    cur_bv=0.0
    cur_mv=0.0
    cur_bv2=0.0
    
    for c in line:
        if ord(c) != TAB:
            data = data + c
        else:
            if TabbedCols.NAME_EPIC_TAB == cur_tab_stop:
                epic,name = extractNameEpic(data)
                cur_epic=epic
                
                if epic not in epic_map:
                    epic_map[epic] = [name, 0, 0.00, 0.00]
                    
            if TabbedCols.NUM_TAB == cur_tab_stop:
                try:
                    cur_num_shares = str2int(data)
                except:
                    cur_num_shares = str2float(data)

            if TabbedCols.AVG_COST_TAB == cur_tab_stop:
                # -1 loses the 'p' at the end
                cur_avg_cost = data[0:-1]
                cur_avg_cost = str2float(cur_avg_cost)
                existing_values = epic_map[cur_epic]
                num, cost = accumulateCountAndCost(
                    existing_values[StockDataCols.NUM_COL],
                    existing_values[StockDataCols.AVG_COST_COL],
                    cur_num_shares,
                    cur_avg_cost)
                existing_values[StockDataCols.NUM_COL] = num
                existing_values[StockDataCols.AVG_COST_COL] = cost
                cur_bv = (cur_num_shares*cur_avg_cost)/100

## test debug
##            if TabbedCols.BOOK_VAL_TAB == cur_tab_stop:
##                cur_bv2 = str2float(data)
## test debug
            
            if TabbedCols.MARKET_VAL_TAB == cur_tab_stop:
                existing_values = epic_map[cur_epic]
                cur_mv=str2float(data)
                existing_values[StockDataCols.MARKET_VAL_COL] =\
                    existing_values[StockDataCols.MARKET_VAL_COL] +\
                    cur_mv
                
            data=''            
            cur_tab_stop = cur_tab_stop + 1
            
    return (epic_map, cur_bv, cur_mv)

"""
@brief High level file parse
@param ifile input file handle
"""
def process(ifile, cash):
    data = ifile.read()

    # remove non-ascii
    data = (c for c in data if 0 < ord(c) < MAX_ASCII)
    data = ''.join(data)

    clean_data = ''
    last_c = ''
    # remove the line break after the TAB
    for c in data:
        if (LF == ord(c)) and (TAB == ord(last_c)):
            #print("condition found")
            continue

        clean_data = clean_data + c           
        last_c = c        

    line=''
    epic_map = {'CASH' : ['CASH', 1, 100*cash, cash]}
    total_bv=cash
    total_mv=cash
    
    for c in clean_data:
        if ord(c) != LF:
            line = line + c
        else:
            epic_map, bv, mv = extractTabbedData(line, epic_map)
            total_bv = total_bv + bv
            total_mv = total_mv + mv
            line = ''        
        
    analysis = analysePortfolio(epic_map, total_mv)
    alphabetical_lst = sorted(analysis, key=lambda x: x[PortfolioCols.NAME_COL])
    displayHoldingList(
        alphabetical_lst, total_bv, total_mv, csv=True, show_title=True)
    
    mrkt_val_lst = sorted(
        analysis,
        key=lambda x: x[PortfolioCols.MRKT_COL],
        reverse=True)
    displayHoldingList(
        mrkt_val_lst,
        total_bv,
        total_mv,
        csv=True,
        show_title=False,
        show_median=True)

    pl_val_lst = sorted(
        analysis,
        key=lambda x: x[PortfolioCols.P_L_COL],
        reverse=True)
    displayHoldingList(
        pl_val_lst,
        total_bv,
        total_mv,
        csv=True,
        show_title=False)

HLP="Hello"    
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--extra_help', '-h++', action='store_true',
        default=False, help=HLP)
    parser.add_argument('--cash', '-c', dest='cash', default=0.0, type=float,
                        help="Cash balance remaining")
    parser.add_argument('--file', '-f', dest='ifile', default="", type=str,
        help="CSV input file")
 
    args = parser.parse_args()

    if args.extra_help:
        print(eh)
        sys.exit(0)

    args.ifile

    curr_file = None
    try:
        curr_file = open(args.ifile)
    except:
        pass

    if not curr_file:
        curr_file = sys.stdin

    process(curr_file, args.cash)        
 
if __name__ == "__main__":
    main()
