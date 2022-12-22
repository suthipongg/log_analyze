def analyze(self):
    gps_col = ["timestamp", "HDop"]
    data_gps = self.pull_data('GPS', gps_col)
    HDop = sum(data_gps[:, 1].flatten() >= 0.8)
    if HDop > 0: return "GPS: \n\tHDop: error"
    else: return "GPS: \n\tHDop: \tok"