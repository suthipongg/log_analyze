def analyze(self):
    msg_col = ["timestamp", "data"]
    data_msg = self.pull_data('msg', msg_col)
    col = (data_msg[:, 1] >= 0.8).any()
    
    if col: 
        status_data = "error"
    else: 
        status_data = "ok"
        
    return f"msg: \n\
        data: \t{status_data}"
    