def analyze(self):
    bat_col = ["timestamp", "Volt"]
    data_bat = self.pull_data('BAT', bat_col)
    bat_max = max(data_bat[:, 1])
    bat_min = min(data_bat[:, 1])
    return f"battery: \n\
        max: \t{bat_max:.2f} Volt \n\
        min: \t{bat_min:.2f} Volt"