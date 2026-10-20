#! /usr/bin/python3
"""
Portfolio analysis tool
See if this changes
"""
# main program

import sys
import argparse

TAB=0x9
LF=0xa
MAX_ASCII=127

class TabbedCols:
    NAME_EPIC_TAB=0
    NUM_TAB=1
    AVG_COST_TAB=2
    BOOK_VAL_TAB=3
    CURR_COST_TAB=4
    MARKET_VAL_TAB=5

def extractNameEpic(data):
    work = data.split('(')
    name = work[0]
    work = work[1]
    epic = work.split(')')[0]
    print("name={0} epic={1}".format(name, epic))

"""
@brief High level file parse
@param line current line
@param epic_map the current epic_map
@returns the new_map

epic -> [name, number, avgcost, book, market]

"""
def extractTabbedData(line, epic_map):
    cur_tab_stop=0
    data=''
    for c in line:
        if ord(c) != TAB:
            data = data + c
        else:
            if TabbedCols.NAME_EPIC_TAB == cur_tab_stop:
                extractNameEpic(data)
            data=''
            cur_tab_stop = cur_tab_stop + 1
    

"""
@brief High level file parse
@param ifile input file handle
"""
def process(ifile):
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

    #print(clean_data)
    line=''
    epic_map = {}
    for c in clean_data:
        if ord(c) != LF:
            line = line + c
        else:
            extractTabbedData(line, epic_map)
            line = ''        
        

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

    process(curr_file)        
 
if __name__ == "__main__":
    main()
