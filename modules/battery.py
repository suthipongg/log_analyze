import numpy as np

def analyze(self):
    bat_col = ["timestamp", "Volt"]
    data_bat = self.pull_data('BAT', bat_col)
    bat_max = max(data_bat[:, 1])
    bat_min = min(data_bat[:, 1])
    # argmax_bat = np.argmax(data_bat[:, 1])
    # test = self.link_value("CTUN", ["ThI", "Alt"], msg_input="BAT", row_input=argmax_bat)
    # print(test)
    return f"battery: \n\
        max: \t{bat_max:.2f} Volt \n\
        min: \t{bat_min:.2f} Volt"