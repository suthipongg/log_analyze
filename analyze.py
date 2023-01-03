import numpy as np
import importlib


class analyzer:
    def pull_data(self, msg, column_name):
        col_index = []
        col = self.dataframe[msg]['Columns']
        for col_name in np.array(column_name, ndmin=1):
            index = np.argmax(col == col_name)
            col_index.append(index)
        values = self.dataframe[msg]['Values'][:, col_index]
        return values
    
    def eliminate_data(self, msg, column_name, return_col=False):
        col_index = []
        columns = self.dataframe[msg]['Columns']
        del_col_index = []
        for n, col_name in enumerate(columns):
            if col_name not in column_name:
                col_index.append(n)
            else: 
                del_col_index.append(n)
        values = self.dataframe[msg]['Values'][:, col_index]
        if return_col:
            columns = np.delete(columns, del_col_index)
            return values, columns
        else: 
            return values

    def analyze_module(self, module):
        try:
            mod = importlib.import_module("modules." + module)
            return mod.analyze(self)
        except: 
            return module + ": library not exist"