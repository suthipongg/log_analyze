import difflib

# create list that contain all necessary message in "msg" variable (name variable is "msg" only)
msg = ["MSG"]

key_message = ["Low Battery", 
               "Critical Battery"
               ]

# analyze log finction (name function is "analyze" only and have only 1 argument is "self")
def analyze(self):
    # create list that contain all necessary column for each message
    msg_col = ["timestamp", "Message"]
    
    # use function to pull data from log reader in dictionary type variable
    # return to numpy 2d array type sorted column by inut of column message list input
    data_msg = self.pull_data('MSG', msg_col)
    
    # write condition to check error for each message
    msg = data_msg[:, 1].flatten()
    ls_error = []
    for key in key_message:
        error_msg = difflib.get_close_matches(key, msg, n=1, cutoff=0.6)
        if error_msg == []:
            continue
        ls_error.append(error_msg[0])
        
    return ["_________________messagge_________________", f"data: {ls_error}"]