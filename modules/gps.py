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
    HDop = (data_gps[:, 1] >= 0.8).any()
    
    if HDop: 
        status_HDop = "error"
    else: 
        status_HDop = "ok"
        
    return ["_________________GPS_________________", f"HDop: {status_HDop}"]
    