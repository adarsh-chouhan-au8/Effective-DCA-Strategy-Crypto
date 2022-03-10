import fn
from datetime import date
from datetime import datetime


test_month = 1  
test_year = 2021


testing = False
debug = False
compounding = False
take_basic_income = False
run_for_single_percentage_cover = True


percentage_cover = 60
trading_fee_percent = .2
monthly_expenses = 0
base_account = 12000
percentage_levels = 15
max_limit_percentage_cover = 99


# pair_file="data/BINANCE_ETHUSDT, 30 test data for may 12 to end"
# pair_file="data/BINANCE_ETHUSDT, 30 from april 2021 to feb 2022"
# pair_file="data/BINANCE_ETHUSDT, 30 1 jan 2021 to april 2021"
pair_file = "data/BINANCE_ETHUSDT, 60 jan 2019 to feb 2022"
# pair_file="data/BINANCE_LINKUSDT, 60 from 2019 to 2022"
# pair_file="data/BINANCE_XRPUSDT, 60 from 2019 to 2022"
# pair_file="data/BINANCE_ADAUSDT, 60 from 2019 to 2022"

open("rough.txt", "w").close()
roughFile = open("rough.txt", 'a')
roughFile.write("\n")
roughFile.write("\n")
roughFile.write(
    "################################################################# printing stars...")
roughFile.write("trading pair: "+pair_file+"\n")
roughFile.write("percentage cover: "+str(percentage_cover)+"\n")
roughFile.write("compounding: "+str(compounding)+"\n")
roughFile.write("take basic income: "+str(take_basic_income)+"\n")
roughFile.write("\n")


percentage_levels_arr = []
Total_account_balance_arr = []

for i in range(1000000):
    file1 = open(pair_file+".csv", 'r')
    data = file1.readline().split(",")
    data = file1.readline().split(",")

    low = float(data[3])
    if debug:
        print(low)

    if percentage_levels > max_limit_percentage_cover:
        break
    roughFile.write("percentage levels: "+str(percentage_levels)+" ")
    roughFile.write("percentage cover: "+str(percentage_cover)+"\n")

    levels = fn.get_dynamic_levels(percentage_cover, percentage_levels, low)
    # print(levels)

    highest_level = levels[0][0]

    Total_account_balance = base_account
    cash_in_hand = 0
    trading_unit = Total_account_balance/(len(levels))
    profit = 0
    count = 0
    loop_count = 1

    month = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
             'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    profit_arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    while True:
        data = file1.readline().split(",")

        if not data[0]:
            break

        low = float(data[3])
        high = float(data[2])
        opening_price = float(data[1])
        closing_price = float(data[4])

        time_stamp = int(data[0])
        current_month = date.fromtimestamp(time_stamp).month
        current_day = date.fromtimestamp(time_stamp).day
        current_year = date.fromtimestamp(time_stamp).year

        if current_year != test_year:
            continue

    # remove basic income from base account every month
        if take_basic_income:
            if current_month > 1:
                Total_account_balance -= 0.80625

    # check if new levels need to be added and lower levels need to be removed

        if debug:
            print(highest_level)
            print(high)

        for i in range(10):
            highest_level = levels[0][0]
            if high >= (highest_level+(highest_level*percentage_levels*.01)):
                new_level = (
                    highest_level+(highest_level*percentage_levels*.01))
                levels.insert(0, [new_level, "empty"])
                levels.pop()
            else:
                break

    # check for possible buying events and execution
        for key, value in enumerate(levels):
            if value[0] < low and value[0] < high:
                break
            if value[0] >= low and value[0] <= high and levels[key][1] == 'empty':
                levels[key][1] = 'filled'
                # print(levels)
                # print("buy order executed at " +
                #       str(value[0]) + " ar "+str(datetime.fromtimestamp(time_stamp)))
                # print("current profit"+str(profit*76))
                # print("Trading unit"+str(Total_account_balance/(len(levels))))

                if debug:
                    input("press enter to continue")

    # check for possible selling events and execution
        for key, value in enumerate(levels):
            if key == len(levels)-1:
                continue

            # considering the case of red candles
            if opening_price > closing_price:
                high = closing_price

            if value[0] >= low and value[0] <= high and levels[key+1][1] == 'filled':
                levels[key+1][1] = 'empty'
                # print(levels)
                # print("sell order executed at " +
                #       str(value[0]) + " ar "+str(datetime.fromtimestamp(time_stamp)))
                count += 1

                trading_unit = Total_account_balance/(len(levels))
                profit += ((percentage_levels-trading_fee_percent)
                           * trading_unit)/100
                if compounding:
                    monthly_expenses += ((percentage_levels -
                                          trading_fee_percent)*trading_unit)/100

                profit_arr[current_month -
                           1] += ((percentage_levels-trading_fee_percent)*trading_unit)/100

                if compounding:
                    Total_account_balance += ((percentage_levels -
                                               trading_fee_percent)*trading_unit)/100

                if debug:
                    input("press enter to continue")

        loop_count += 1

    for i in range(len(profit_arr)):
        print("Net profit for " +
              str(month[i])+" "+str(test_year)+" is: " + str(profit_arr[i]*76)+" INR")
        roughFile.write(
            "Net profit for "+str(month[i])+" is: " + str(profit_arr[i]*76)+" INR"+"\n")
    cash_in_hand = 0
    for lev in levels:
        if lev[1] == 'empty':
            cash_in_hand += Total_account_balance/(len(levels))


    print("\n")
    print("ROI: " +
          str(fn.roi(base_account, profit))+" %")

    print("Net profit: " + str(profit*76)+" INR")


    roughFile.write("total profit : " +
                    str((Total_account_balance-base_account)*76)+"\n")
    roughFile.write("Levels : "+str(len(levels))+"\n")
    roughFile.write("CASH IN HAND : "+str(cash_in_hand*76)+"\n")
    roughFile.write("\n")
    roughFile.write("\n")



    Total_account_balance_arr.append(profit*76)
    percentage_levels_arr.append(percentage_levels)
    file1.close()

    percentage_levels += .45

    if run_for_single_percentage_cover:
        exit()


for i in range(len(Total_account_balance_arr)):
    print(Total_account_balance_arr[i], percentage_levels_arr[i])
print(max(Total_account_balance_arr))
i = Total_account_balance_arr.index(max(Total_account_balance_arr))
print(percentage_levels_arr[i])
roughFile.write("the maximum ROI was : "+str(max(Total_account_balance_arr)
                                             )+" at "+str(percentage_levels_arr[i])+"\n")
roughFile.write("\n")
