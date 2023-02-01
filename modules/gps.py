import numpy as np

# create list that contain all necessary message in "msg" variable (name variable is "msg" only)
msg = ["GPS"]

# analyze log finction (name function is "analyze" only and have only 1 argument is "self")
def analyze(self):
    # create list that contain all necessary column for each message
    gps_col = ["timestamp", "HDop"]
    
    # use function to pull data from log reader in dictionary type variable
    # return to numpy 2d array type sorted column by inut of column message list input
    data_gps = self.pull_data('GPS', gps_col)
    
    # write condition to check error for each message
    thresh_val = 0.8
    HDop_check = data_gps[:, 1] >= thresh_val
    HDop = HDop_check.any()
    
    if HDop: 
        row = np.argmax(HDop_check)
        status_HDop = "error "
        sign = " >= "
    else: 
        row = np.argmax(data_gps[:, 1])
        status_HDop = "ok "
        sign = " < "
        
    Hdop_val = data_gps[row, 1]
        
    dict_data = {"HDop" : status_HDop + ": max HDop value is " + str(Hdop_val) + sign + str(thresh_val)}
    
    return dict_data
    