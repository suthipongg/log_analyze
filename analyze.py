import numpy as np
from module import battery, gps


class analyze:
    def __init__(self):
        self.ls_msg_from_type = {"battery" : ['AGRI', 'VIBE', 'RATE'], 
                                 "gps" : ["ATT", "IMU"]}


    def pull_data(self, msg, column_name):
        col_index = []
        for col_name in np.array(column_name, ndmin=1):
            index = np.argmax(self.dataframe[msg]['Columns'] == col_name)
            col_index.append(index)
        return self.dataframe[msg]['Values'][:, col_index]


    def analyze_module(self, module):
        if module == "battery": 
            return battery.analyze(self)
        elif module == "gps": 
            return gps.analyze(self)
        else: 
            return module + " type not found"