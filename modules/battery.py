def analyze(self):
    ls_col = ["timestamp", "VibeX", "VibeY","VibeZ"]
    data_batt = self.pull_data('VIBE', ls_col)
    return f"battery ok \n{data_batt[:10]}"