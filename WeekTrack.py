import sys
import os
from datetime import date
import logging
import argparse
import collections
import csv

def calculate_weekly_trend(dataList):
    positive = []  # week start going up and ending positive
    negtive = []   # week start negative and ending negative
    reversed = []  # trend reversed during the week
    begin = 0.00
    begining = 0.00
    ending = 0.00
    previous_ending = 0.00

    for i in range(len(dataList)):
        try:
            ds, c,o, h, l = dataList[i].split(",") # date_string, close, open, high, low
            m,d,y = ds.split('/')
            dt = date(int(y), int(m),int(d))
            # Monday is 0 and Sunday is 6
            wd = dt.weekday()
            match wd:
                case 0:
                    begin = float(c)
                    if(begining == 0.00):
                        begining = float(c)
                case 4:
                    ending = float(c)
                    if previous_ending != 0.00:
                        if begin > previous_ending and ending > begin:
                            positive.append(ending - begin)
                        elif begin > previous_ending and ending < begin:
                            reversed.append(ending - begin)
                        elif begin < previous_ending and ending < begin:
                            negtive.append(ending - begin)
                        elif begin < previous_ending and ending > begin:
                            reversed.append(ending - begin)
                    previous_ending = ending
        except:
            print("Bad data at position {} : {}".format(i, dataList[i]))
    return (positive, negtive, reversed, begining, ending)

def parsingArgs():
    parser = argparse.ArgumentParser(description='Process some S&P 500 data.')
    parser.add_argument('-m','--month', dest='month', type=str, nargs="+",
                        help='Calculated the gains for the month, passing as 1-9,12  or 3-5,8-6 ')
    parser.add_argument('filename', default="SPX500.csv",  nargs='?')

    logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s %(message)s ')

    args = parser.parse_args()
    logging.info(args.month)

    Range = collections.namedtuple("Range","x y")
    Ranges = []

    if args.month == None:
        Ranges.append(Range(1,12))
    else:
        """ def cleanMonth(p):
            if ',' in p:
            p = p.split(',')[0]
            logging.debug(f"month is: {p}")
            return p 
        m = list(map(cleanMonth, args.month)) """
        if not isinstance(args.month, str):
            m = ''.join(args.month).split(',')
        else:
            m = args.month.split(','
                                )
        logging.debug(f"month are: {m}")
        mos = []
        for mm in m:
            try:
                if mm.isnumeric() and int(mm) < 13 and int(mm) > 0:
                    mos.append(int(mm))
                elif '-' in mm :
                    ms = mm.split('-')
                    for i in range( int(ms[0]), int(ms[1])+1 ):
                        mos.append(i)

            except ValueError:
                print(mm, " is not a valid number")

        if len(mos):
            mos = list(set(mos))
            mos.sort()
            logging.debug(f"mos is: {mos}")
            if(len(mos) == 1):
                Ranges.append(Range(mos[0], mos[0]))
            else:
                begin = 0
                i = 1
                for i in range(1, len(mos)):
                    if mos[i] != mos[i-1] + 1 :
                        Ranges.append(Range(mos[begin], mos[i-1]))
                        begin = i
                    
                if len(Ranges) == 0 or Ranges[len(Ranges)-1].x != mos[begin]:
                    Ranges.append(Range(mos[begin], mos[len(mos)-1]))

            logging.debug(f"Month looking at: {Ranges}")
            return { "Month": Ranges, "Filename": args.filename }

def gettingDataCSV(data_file ):
    logging.debug("Reading data from ", data_file)

    if(not os.path.isfile(data_file)):
        logging.error("Can not locate file ", data_file)
        exit(1)

    with open(data_file, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        sniffer = csv.Sniffer()
        sample = csv_file.read(1024)
        csv_file.seek(0)
        if(sniffer.has_header(sample)):
            next(csv_reader)
        dataList = list(csv_reader)
        dataList.reverse()
        logging.debug("data is ", dataList)
    
        return dataList

def gettingWeeklyTrend(dataList):
    p, n, r, b, e = calculate_weekly_trend(dataList)

    total = len(dataList)/5
    print( "Percent of following Moday trend: {:.{}f}%".format( (len(p)+len(n))*100/total, 2))
    print( "Percent of reversing Moday trend: {:.{}f}%".format( len(r)*100/total, 2))

    p_points = np.sum(p);
    for i in range(len(r)):
        if r[i] < 0.00:
            p_points += r[i]

    print( "Total points gained following positive Moday: {0} vs Market {1}".format(b, e - b))


if __name__ == "__main__":
    args = parsingArgs()
    print(args)
    data = gettingDataCSV(args["Filename"])
