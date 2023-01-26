"""
# create list that contain all necessary message in "msg" variable (name variable is "msg" only)
msg = ["msg1", "msg2", ...]

# analyze log finction (name function is "analyze" only and have only 1 argument is "self")
def analyze(self):
    # create list that contain all necessary column for each message
    msg1_col = ["timestamp", "data", ...]
    msg2_col = ["col1", "col2", ...]
    .
    .
    .
    
    # use function to pull data from log reader in dictionary type variable
    # return to numpy 2d array type sorted column by inut of column message list input
    data_msg1 = self.pull_data('msg1', msg1_col)
    data_msg2 = self.pull_data('msg2', msg2_col)
    .
    .
    .
    
    # write condition to check error for each message
    col = (data_msg[:, 1] >= 0.8).any() # example
    
    # if require the value at the desired time from another message 
    # use "link_value" function from analyze.py
    msg1_desired = self.link_value("msg1_desired", ["col1_msg1_desired", "col2_msg1_desired"], 
                    timestamp_input=timestamp1 at the desired time)
    msg2_desired = self.link_value("msg2_desired", ["col1_msg2_desired", "col2_msg2_desired"], 
                    timestamp_input=timestamp2 at the desired time)
    .
    .
    .
    
"""