# create list that contain all necessary message in "msg" variable (name variable is "msg" only)
msg = ["PROF"]

# analyze log finction (name function is "analyze" only and have only 1 argument is "self")
def analyze(self):
    # create list that contain all necessary column for each message
    ver_col = ["TimeUS", "timestamp"]
    
    # use function to pull data from log reader in dictionary type variable
    # return to numpy 2d array type sorted column by inut of column message list input
    data_msg, column_msg = self.eliminate_data('PROF', ver_col, return_col=True)
    
    # write condition to check error for each message
    data_msg = data_msg[0]
    result = ["_________________version_________________"]
    for n, col in enumerate(column_msg):
        result += [col + ": " + str(data_msg[n])]
    return result