from Reader.mavutil import mode_mapping_acm
from operator import itemgetter
from datetime import datetime
import numpy as np
# create list that contain all necessary message in "msg" variable (name variable is "msg" only)
msg = ["MODE"]

# analyze log finction (name function is "analyze" only and have only 1 argument is "self")
def analyze(self):
    # create list that contain all necessary column for each message
    mode_col = ["timestamp", "Mode"]
    
    # use function to pull data from log reader in dictionary type variable
    # return to numpy 2d array type sorted column by inut of column message list input
    data_mode = self.pull_data('MODE', mode_col)
    mode_name = itemgetter(*data_mode[:, 1])(mode_mapping_acm)
    dt_object = map(datetime.fromtimestamp, data_mode[:, 0]);
    time = list(map(lambda t : t.strftime("%H:%M:%S"), dt_object));
    result = np.array([np.array(time), np.array(mode_name)]).T

    # write condition to check error for each message
    return result