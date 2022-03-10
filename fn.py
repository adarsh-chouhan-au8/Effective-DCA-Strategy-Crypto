
def get_levels(low,high,level_percentage):
    levels = []
    new_level=0
    levels.append([low,"empty"])
    for i in range(50):
       
        new_level = (low*level_percentage)/100+low
        
        if new_level>high:
            break
        levels.append([new_level,"empty"])
        low=new_level
    levels.reverse()        
    return levels


def get_dynamic_levels(percentage_cover,levels_percentage,price):
    levels=[]
    base=price*(1-percentage_cover*.01)
    #print(base)
    levels.append([base,"empty"])

    while True:


        
        base=((base*levels_percentage)/100)+base
        if base>price:
            break
        levels.append([base,"empty"])
    levels.reverse() 
    return levels    

        



def buy_possible(low,high,levels):
    for key in levels:
        if key<low and key<high:
            break
        if key>=low and key<=high and levels[key]=='empty':
            levels[key]='filled'
    return False

def plot_levels(levels):
    for level in levels:
        print("plot("+str(level[0])+")")

def roi(base_account, profit):
    percentage_roi=(profit*100)/base_account
    return percentage_roi


