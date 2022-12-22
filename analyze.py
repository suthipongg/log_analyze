import numpy as np
import importlib


ls_msg_from_type = {"battery" : ['AGRI', 'VIBE', 'RATE'], 
                                 "gps" : ["ATT", "IMU"]}


class analyzer:
    def pull_data(self, msg, column_name):
        col_index = []
        for col_name in np.array(column_name, ndmin=1):
            index = np.argmax(self.dataframe[msg]['Columns'] == col_name)
            col_index.append(index)
        return self.dataframe[msg]['Values'][:, col_index]

    def analyze_module(self, module):
        try:
            mod = importlib.import_module("modules." + module)
            return mod.analyze(self)
        except: 
            return module + " library not exist"