import numpy as np
import importlib


class analyzer:
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
                
    def pull_data(self, msg, column_name):
        col_index = []
        columns = self.dataframe[msg]['Columns']
        for col_name in np.array(column_name, ndmin=1):
            index = np.argmax(columns == col_name)
            col_index.append(index)
        values = self.dataframe[msg]['Values'][:, col_index]
        return values
    
    def eliminate_data(self, msg, column_name=None, return_col=False):
        columns = self.dataframe[msg]['Columns']
        col_index = self.find_column_index(msg, column_name, not_in=True)   
        values = self.dataframe[msg]['Values'][:, col_index]
        if return_col:
            columns = columns[col_index]
            return values, columns
        else: 
            return values
        
    def link_value(self, msg_output, column_output, 
                   timestamp_input=None, msg_input=None, row_input=None, method="approximate"):
        if timestamp_input == None:
            timestamp_index_input = self.find_column_index(msg_input, "timestamp")
            timestamp_input = self.dataframe[msg_input]["Values"][row_input, timestamp_index_input]
        if type(msg_output) == str: 
            msg_output = [msg_output]
            
        for msg in msg_output:
            col_index = self.find_column_index(msg, column_output)
            timestamp_index_output = self.find_column_index(msg, "timestamp")
            timestamp_values_output = self.dataframe[msg]["Values"][:, timestamp_index_output]
            bool_upper = timestamp_values_output > timestamp_input
            upper = np.argmax(bool_upper)
            
            if np.sum(bool_upper) == 0:
                values = self.dataframe[msg]['Values'][-1, col_index]
            elif upper == 0 or method == "upper":
                values = self.dataframe[msg]['Values'][upper, col_index]
            elif method == "lower":
                values = self.dataframe[msg]['Values'][upper-1, col_index]
            elif method == "approximate":
                delta_t = timestamp_values_output[upper] - timestamp_values_output[upper-1]
                delta_values = self.dataframe[msg]['Values'][upper, col_index] - \
                               self.dataframe[msg]['Values'][upper-1, col_index]
                values = self.dataframe[msg]['Values'][upper, col_index] - \
                         ((timestamp_values_output[upper] - timestamp_input)/delta_t * delta_values)
            return values

    def analyze_module(self, module):
        try:
            mod = importlib.import_module("modules." + module)
            return mod.analyze(self)
        except Exception as e: 
            print(e)
            return module + ": library not exist"