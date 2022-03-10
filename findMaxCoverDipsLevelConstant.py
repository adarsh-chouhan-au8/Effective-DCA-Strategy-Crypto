import fn
from datetime import date
from datetime import datetime
debug=False
compounding=False
take_basic_income=False
percentage_cover=60
# percentage_levels=25
trading_fee_percent=.2
monthly_expenses=0
pair_file="BINANCE_LINKUSDT, 30 1 year"
base_account=12987

#testing parameters for
percentage_levels = 7
max_limit_percentage_cover = 45




roughFile=open("rough.txt",'a')
roughFile.write("\n")   
roughFile.write("\n")   
roughFile.write("################################################################# printing stars...")   
roughFile.write("trading pair: "+pair_file+"\n")
roughFile.write("percentage cover: "+str(percentage_cover)+"\n")
roughFile.write("compounding: "+str(compounding)+"\n")
roughFile.write("take basic income: "+str(take_basic_income)+"\n")
roughFile.write("\n")



percentage_levels_arr=[]
Total_account_balance_arr=[]

while True:
    print(percentage_levels)
    if percentage_levels>43:
        break
    percentage_cover=24    
    for i in range(1000000):
        if percentage_cover>74:
            break
        file1=open(pair_file+".csv",'r')
        data=file1.readline().split(",")
        data=file1.readline().split(",")
        # time_stamp=int(data[0])
        # print(datetime.fromtimestamp(time_stamp))
        # exit()
        low = float(data[3])
        if debug:
            print(low)
        # if debug:
        #     low=1.932
        # if percentage_levels>max_limit_percentage_cover:
        #     break
        roughFile.write("percentage levels: "+str(percentage_levels)+" ")
        roughFile.write("percentage cover: "+str(percentage_cover)+"\n")

        levels = fn.get_dynamic_levels(percentage_cover, percentage_levels, low)
        print(levels)

        #levels=[[1.9383795052002744, 'filled'], [1.7865248895855064, 'filled'], [1.6465667185119874, 'filled'], [1.5175730124534446, 'filled'], [1.3986848041045572, 'filled'], [1.2891104185295459, 'filled'], [1.1881202014097196, 'filled'], [1.0950416602854558, 'filled'], [1.009254986438208, 'filled'], [0.9301889275928186, 'empty']]
        highest_level = levels[0][0]

        Total_account_balance=base_account
        cash_in_hand=0
        trading_unit=Total_account_balance/(len(levels))
        profit = 0
        count=0
        loop_count=1
        day=4

        month=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
        profit_arr=[0,0,0,0,0,0,0,0,0,0,0,0]

        while True: 
            data=file1.readline().split(",")
            print(data)
            if not data[0]:
                break
            low = float(data[3])
            high = float(data[2])
            opening_price=float(data[1])
            closing_price=float(data[4])
            time_stamp=int(data[0])
            current_month= date.fromtimestamp(time_stamp).month

            current_day=date.fromtimestamp(time_stamp).day
            #remove 92000 per month from base accounts 
            if take_basic_income:
                if current_month>1:
                    Total_account_balance-=0.80625

        #check if new levels need to be added and lower levels need to be removed
            
            if debug:
                print(highest_level)
                print(high)
            
            for i in range(10):
                highest_level = levels[0][0]
                if high>=(highest_level+(highest_level*percentage_levels*.01)):
                    new_level=(highest_level+(highest_level*percentage_levels*.01))
                    levels.insert(0,[new_level,"empty"])
                    levels.pop()
                else:
                    break    

            

        # check for buying events if possible buy at those levels
            for key,value in enumerate(levels):
                if value[0] < low and value[0] < high:
                    break
                if value[0] >= low and value[0] <= high and levels[key][1] == 'empty' :
                    levels[key][1] = 'filled'
                    print ("buy order executed at " +str(value[0]) +" ar "+str(datetime.fromtimestamp(time_stamp)))
                    print("current profit"+str(profit*76))
                    print("Trading unit"+str(Total_account_balance/(len(levels))))

                    if debug:
                        input("press Enter")
            print(levels)
            
                
        # check for selling events if possible sell at those
            for key,value in enumerate(levels):
                if key == len(levels)-1:
                    continue
                
                #considering the case of red candles
                if opening_price>closing_price:
                    high=closing_price
                
                
                
                    if value[0] >= low and value[0] <= high and levels[key+1][1] == 'filled':
                            levels[key+1][1] = 'empty'
                            print ("sell order executed at " +str(value[0]) +" ar "+str(datetime.fromtimestamp(time_stamp)))
                            count+=1
                        
                        
                            # if int(current_day)==1 and compounding:
                            #     monthly_expenses=0

                            # if (int(current_month)==31 or int(current_month)==30 )and compounding:
                            #     monthly_expenses-=1200    

                            

                            trading_unit=Total_account_balance/(len(levels))
                            profit += ((percentage_levels-trading_fee_percent)*trading_unit)/100
                            if compounding:
                                monthly_expenses+=((percentage_levels-trading_fee_percent)*trading_unit)/100

                            
                            profit_arr[current_month-1]+=((percentage_levels-trading_fee_percent)*trading_unit)/100  

                            if  compounding:
                                Total_account_balance+=((percentage_levels-trading_fee_percent)*trading_unit)/100
                            print("current profit"+str(profit*76))
                            print("Trading unit"+str(Total_account_balance/(len(levels))))    
                            
                            if debug: 
                                input("press Enter")
                            
                    
                

            day+=1
            loop_count+=1  
            
            

        for i in range(len(profit_arr)):
            print("Net profit for "+str(month[i])+" is: "+ str(profit_arr[i]*76)+" INR")
            roughFile.write("Net profit for "+str(month[i])+" is: "+ str(profit_arr[i]*76)+" INR"+"\n")
        cash_in_hand=0
        for lev in levels:
            if lev[1]=='empty':
                cash_in_hand+=Total_account_balance/(len(levels))

        print("Net profit "+ str(profit)+" USDT")
        print("Net profit "+ str(profit*76)+" INR")
        roughFile.write("total profit : "+str((Total_account_balance-base_account)*76)+"\n")   
        roughFile.write("Levels : "+str(len(levels))+"\n")   
        roughFile.write("CASH IN HAND : "+str(cash_in_hand*76)+"\n")   
        roughFile.write("TOTAL ACCOUNT BALANCE : "+str(Total_account_balance*76)+"\n")   
        roughFile.write(','.join([str(i[0]) for i in levels])+"\n")   
        

        roughFile.write("\n")   
        roughFile.write("\n")   
        print("TYotaal account balance "+ str(Total_account_balance*76)+" INR")
        print(count)
        print("no of levels : "+str(len(levels))) 
        print(((percentage_levels-trading_fee_percent)*trading_unit)/100)
        print(trading_unit)
        Total_account_balance_arr.append(profit*76)
        percentage_levels_arr.append(percentage_levels)
        file1.close()
        percentage_cover+=1
        # exit()
    percentage_levels+=.4    

for i in range(len(Total_account_balance_arr)):
    print(Total_account_balance_arr[i],percentage_levels_arr[i])
print(max(Total_account_balance_arr))
i=Total_account_balance_arr.index(max(Total_account_balance_arr))
print(percentage_levels_arr[i])
roughFile.write("the maximum ROI was : "+str(max(Total_account_balance_arr))+" at "+str(percentage_levels_arr[i])+"\n")   
roughFile.write("\n")   


