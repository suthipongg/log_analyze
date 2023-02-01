import numpy as np

# create list that contain all necessary message in "msg" variable (name variable is "msg" only)
msg = ["BAT", "CTUN"]

# analyze log finction (name function is "analyze" only and have only 1 argument is "self")
def analyze(self):
    # create list that contain all necessary column for each message
    bat_col = ["timestamp", "Volt"]
    
    # use function to pull data from log reader in dictionary type variable
    # return to numpy 2d array type sorted column by inut of column message list input
    data_bat = self.pull_data('BAT', bat_col)
    
    # write condition to check error for each message
    index_bat_max = np.argmax(data_bat[:, 1])
    bat_max = data_bat[index_bat_max, 1]
    index_bat_min = np.argmin(data_bat[:, 1])
    bat_min = data_bat[index_bat_min, 1]
    
    # if require the value at the desired time from another message 
    # use "link_value" function from analyze.py
    ctun_col = ["ThI", "Alt"]
    data_link_ctun = self.link_value("CTUN", ctun_col, data_bat[index_bat_max, 0])
    
    dict_data = {"bat_max" : "maximum batterry : " + str(bat_max) + " Volt", 
                 "bat_min" : "minimum batterry : " + str(bat_min) + " Volt", 
                 'ctun_at_bat_max' : "ctun at maximum battery" + str(data_link_ctun)}
        
    return dict_data