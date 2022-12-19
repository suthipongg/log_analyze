import numpy as np

class check_status(object):
    def __init__(self):
        self.ls_msg_from_type = {"battery" : ['AGRI', 'VIBE', 'RATE'], 
                                    "gps" : ["ATT", "IMU"]}

    def pull_data(self, msg, column_name):
        col_index = np.where(self.data[msg]['Columns'] == column_name)
        return self.data[msg]['Values'][:, col_index].flatten()

    def battery(self):
        timestamp = self.pull_data('AGRI', 'timestamp')
        return f"battery ok {timestamp[:10]}"

    def gps(self):

        return f"gps ok {type(self.data['ATT']['Columns'])}"

    def __call__(self, type):
        if type == "battery": 
            return self.battery()
        elif type == "gps": 
            return self.gps()
        else: 
            return type + " type not found"