def analyze(self):
    gps_col = ["timestamp", "HDop"]
    data_gps = self.pull_data('GPS', gps_col)
    HDop = (data_gps[:, 1] >= 0.8).any()
    
    if HDop: 
        status_HDop = "error"
    else: 
        status_HDop = "ok"
        
    return f"GPS: \n\
        HDop: \t{status_HDop}"
    