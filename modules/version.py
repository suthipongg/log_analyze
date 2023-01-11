def analyze(self):
    ver_col = ["TimeUS", "timestamp"]
    data_msg, column_msg = self.eliminate_data('PROF', ver_col, return_col=True)
    data_msg = data_msg[0]
    result = "version: "
    for n, col in enumerate(column_msg):
        result += "\n\t" + col + ": " + str(data_msg[n])
    return result