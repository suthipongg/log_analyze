import numpy as np
import importlib


class analyzer:
    # find column index that required
    def find_column_index(self, msg, column_name=None, not_in=False):
        columns = self.dataframe[msg]['Columns']
        if column_name == None or len(column_name) == 0:
            if not_in:
                return list(range(len(columns)))
            else:
                return []
        else:
            col_index = []
            if type(column_name) == str: 
                column_name = [column_name]
            for n, col_name in enumerate(columns):
                if col_name not in column_name:
                    if not_in:
                        col_index.append(n)
                else:
                    if not not_in:
                        col_index.append(n)
            return col_index
    # pull the required columns and message from dataframe       
    def pull_data(self, msg, column_name):
        col_index = []
        columns = self.dataframe[msg]['Columns']
        for col_name in np.array(column_name, ndmin=1):
            index = np.argmax(columns == col_name)
            col_index.append(index)
        values = self.dataframe[msg]['Values'][:, col_index]
        return values
    # pull the required message and eliminate unwanted columns from dataframe 
    def eliminate_data(self, msg, column_name=None, return_col=False):
        columns = self.dataframe[msg]['Columns']
        col_index = self.find_column_index(msg, column_name, not_in=True)   
        values = self.dataframe[msg]['Values'][:, col_index]
        if return_col:
            columns = columns[col_index]
            return values, columns
        else: 
            return values
    # get value from another message that match with required timestamp
    # approximate method is approximate link data to required timestamp
    # upper method is select upper bound of link data at that timestamp
    # lower method is select lower bound of link data at that timestamp
    def link_value(self, msg_output, column_output, timestamp_input, method="approximate"):
        col_index = self.find_column_index(msg_output, column_output)
        timestamp_index_output = self.find_column_index(msg_output, "timestamp")
        timestamp_values_output = self.dataframe[msg_output]["Values"][:, timestamp_index_output]
        bool_upper = timestamp_values_output > timestamp_input
        upper = np.argmax(bool_upper)
        
        if np.sum(bool_upper) == 0:
            values = self.dataframe[msg_output]['Values'][-1, col_index]
        elif upper == 0 or method == "upper":
            values = self.dataframe[msg_output]['Values'][upper, col_index]
        elif method == "lower":
            values = self.dataframe[msg_output]['Values'][upper-1, col_index]
        elif method == "approximate":
            delta_t = timestamp_values_output[upper] - timestamp_values_output[upper-1]
            delta_values = self.dataframe[msg_output]['Values'][upper, col_index] - \
                            self.dataframe[msg_output]['Values'][upper-1, col_index]
            values = self.dataframe[msg_output]['Values'][upper, col_index] - \
                        ((timestamp_values_output[upper] - timestamp_input)/delta_t * delta_values)
        return values
    # analyze module
    def analyze_module(self, module):
        try:
            mod = importlib.import_module("modules." + module)
            return mod.analyze(self)
        except Exception as e: 
            print(e)
            return module + ": library not exist"