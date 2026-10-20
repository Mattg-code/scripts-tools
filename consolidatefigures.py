#! /usr/bin/python3
"""
The converts the CSV file made by iwebsummary2csv.sh into 3 sorted portfolio
presentations. Cash balance can be handled one of 2 ways:

1. the balance from either ISA can either be summarised and passed as -c <cash>
2. or it can be used to produce a fake line(s) in the figures.txt e.g.

CASH  (CASH) 	
52 	2,864.0577p 	1,480.31 	*2,795.00p 	1,480.31 	-35.91 	-2.41%

and maybe

CASH  (CASH) 	
52 	2,864.0577p 	15.80     	*2,795.00p 	15.80     	-35.91 	-2.41%
"""
 
import sys
import argparse

type_buckets = {
    "Cash" : 0.00,
    "IT" : 0.00,
    "OEIC" : 0.00,
    "Swiss" : 0.00,
    "Tech" : 0.00,
    "UK" : 0.00,
    "Uranium" : 0.00,
    "US" : 0.00
}

type_lut = {
    "ADM" : "UK",
    "AJB" : "UK",
    "AAL" : "UK",
    "ANTO" : "UK",
    "ASML" : "Tech",
    "ATR" : "IT",
    "AZN" : "UK",
    "BA." : "UK",
    "BERI" : "IT",
    "BRWM" : "IT",
    "BMY" : "UK",
    "BOY" : "UK",
    "CCJ" : "Uranium",
    "CASH" : "Cash",
    "CCJI" : "IT",
    "CSCO" : "Tech",
    "CTY" : "IT",
    "CKN" : "UK",
    "KO" : "US",
    "CCC" : "UK",
    "CRH" : "US",
    "FCSS" : "IT",
    "FIAAGM" : "OEIC",
    "FOUR" : "UK",
    "GFRD" : "UK",
    "GAW" : "UK",
    "GEN" : "UK",
    "GOOG" : "Tech",
    "GSK" : "UK",
    "HLMA" : "UK",
    "HFEL" : "IT",
    "HILS" : "UK",
    "IBT" : "IT",
    "IGET" : "IT",
    "IMB" : "UK",
    "ITRK" : "UK",
    "JNJ" : "US",
    "JCGI" : "IT",
    "JEGI" : "IT",
    "JIGI" : "IT",
    "KLR" : "UK",
    "LGEN" : "UK",
    "ROBG" : "Tech",
    "MRCH" : "IT",
    "MGNS" : "UK",
    "MYI" : "IT",
    "NAIT" : "IT",
    "NG." : "UK",
    "NXT" : "UK",
    "NVDA" : "Tech",
    "PSN" : "UK",
    "PLUS" : "UK",
    "PCT" : "Tech",
    "QQ." : "UK",
    "REL" : "UK",
    "RSW" : "UK",
    "ROR" : "UK",
    "SHEL" : "UK",
    "SCT" : "UK",
    "SPX" : "UK",
    "ESCT" : "IT",
    "SGE" : "UK",
    "UC94" : "Swiss",
    "ULVR" : "UK",
    "UEM" : "IT",
    "VOF" : "IT",
    "YCA" : "Uranium"
}    

HLP = "Consolidate the figures from iWeb valuation statements, either pipe "
HLP = HLP + "figures.csv on stdin, or on command line"

# inputs
NUM_COLS=6
DESC=0
EPIC=1
NUM=2
AVG=3
BOOK=4
MRKT=5

# outputs
O_DESC=0
O_EPIC=1
O_BOOK=2
O_MRKT=3
O_PERC=4
O_PL=5
O_NUM=6
O_AVG=7
 
def output_holdings(listy, total_book, total_mrkt, holding_weight_disp=False):
    if holding_weight_disp:
        num_holdings = len(listy)
        even_num = (0 == (num_holdings % 2))
    
        median_stock_ix = int(num_holdings / 2)
    
        median_value = listy[median_stock_ix][O_MRKT]
        if even_num:
            median_value = median_value + listy[median_stock_ix-1][O_MRKT]
            median_value = median_value/2

    ix = 0
    for li in listy:
        if holding_weight_disp:
            output_median = "median" if median_stock_ix == ix else ""
            proportion_median = "{0:.2f}x".format(li[O_MRKT] / median_value)
        else:
            output_median = ""
            proportion_median = ""
            
        print("%s,%s,%d,%.2f,%.2f,%.2f,%.3f,%.3f,%s,%s" % (
            li[O_DESC], li[O_EPIC], li[O_NUM], li[O_AVG], li[O_BOOK],
            li[O_MRKT], li[O_PERC], li[O_PL], proportion_median, output_median))
        ix = ix + 1
        
    print("TOTAL,,,,%.2f,%.2f,," % (total_book, total_mrkt))

NUM_COLS=6
DESC=0
EPIC=1
NUM=2
AVG=3
BOOK=4
MRKT=5

def consolidate(cash, ifile):
    f = None
    try:
        f = open(ifile)
    except:
        pass
    
    if not f:
        f = sys.stdin

    global type_buckets
    global type_lut

    dict_holdings = {"CASH": ["CASH", cash, cash, 1, cash]}
    total_mrkt = cash
    total_book = cash

    # indexes for "dict_holdings", epic is the key.
    DICT_LIST_DESC = 0
    DICT_LIST_BOOK = 1
    DICT_LIST_MRKT = 2
    DICT_LIST_NUM = 3
    DICT_LIST_AVG = 4
    
    for line in f:
        line = line.strip('\n')
        columns = line.split(',')
        if NUM_COLS != len(columns):
            print("Invalid line", line)
            continue

        desc = columns[DESC] 
        epic = columns[EPIC]
        book = float(columns[BOOK])
        mrkt = float(columns[MRKT])

        # Oeics etc. may be fractional
        oeic = columns[NUM].split('.')[0]
        num_shares = int(oeic)
        
        remove_p = columns[AVG].split('p')[0]
        avg_cost =  float(remove_p)
        
        total_mrkt += mrkt
        total_book += book
        if epic in dict_holdings:
            datas = dict_holdings[epic]
            dict_holdings[epic][DICT_LIST_BOOK] += book
            dict_holdings[epic][DICT_LIST_MRKT] += mrkt
            bv = (dict_holdings[epic][DICT_LIST_AVG]*dict_holdings[epic][DICT_LIST_NUM]
                + avg_cost*num_shares)
            dict_holdings[epic][DICT_LIST_AVG] = bv/(num_shares+dict_holdings[epic][DICT_LIST_NUM])
            dict_holdings[epic][DICT_LIST_NUM] += num_shares
        else:
            dict_holdings[epic] = [desc, book, mrkt, num_shares, avg_cost]

    sorted_holdings = []

    SORT_DESC=0
    SORT_EPIC=1
    SORT_BOOK=2
    SORT_MRKT=3
    SORT_PERC=4
    SORT_PL=5
    
    for epic,v in dict_holdings.items():
        book = v[DICT_LIST_BOOK]
        mrkt = v[DICT_LIST_MRKT]
        perc_mrkt = mrkt/total_mrkt if total_mrkt else 0.0
        pl = (mrkt - book)/book if book else 0.00
        sorted_holdings.append([v[DICT_LIST_DESC],epic,v[DICT_LIST_BOOK],v[DICT_LIST_MRKT],perc_mrkt,pl, v[DICT_LIST_NUM], v[DICT_LIST_AVG]])

        try:
            # find epic in type_lut,
            investment_type = type_lut[epic]
        except:
            print("No entry for {0] in type lut :(".format(epic))
            raise

        type_buckets[investment_type] = type_buckets[investment_type] + mrkt
        
    name_sort = sorted(sorted_holdings, key=lambda x: x[SORT_DESC])
    pl_sort =  sorted(sorted_holdings, key=lambda x: x[SORT_PL], reverse=True)
    contrib_sort =  sorted(sorted_holdings, key=lambda x: x[SORT_PERC], reverse=True)


    print("NAME,EPIC,NUMBER,AVG COST,BOOK,MRKT,%s MRKT,P/L" % "%")        
    output_holdings(name_sort, total_book, total_mrkt)
    print(",,,,,")
    output_holdings(contrib_sort, total_book, total_mrkt,True)
    print(",,,,,")
    output_holdings(pl_sort, total_book, total_mrkt)
    print(",,,,,")

    sorted_types = sorted(type_buckets.items(), key=lambda x: x[1], reverse=True)

    for investment_type,mrkt_value in sorted_types:
        print("{0},{1:.4f},,,,".format(investment_type, mrkt_value/total_mrkt))
        
       
# main program
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

    consolidate(args.cash, args.ifile)        
 
if __name__ == "__main__":
    main()
