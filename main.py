from pathlib import Path
import argparse
import numpy as np
from Reader import DFReader
from analyze import analyzer
import sys, os
import importlib
import pandas as pd


class read_binary:
    def __init__(self, path):
        self.path = path
        self.mlog = DFReader.DFReader_binary(self.path)
        self.match_types = list(self.mlog.name_to_id.keys())
        self.match_types.sort()
        self.dataframe = {}
        self.msgs = []
    
    def all_msgs(self):
        all_use_msgs = set()
        for module in self.modules_check:
            try:
                msg = importlib.import_module("modules." + module)
                all_use_msgs = all_use_msgs.union(set(msg.msg))
            except Exception as e:
                print(e)
                print(module, "module not in dictionary module:messages")
        return all_use_msgs
    
    def read_bin(self):
        self.msgs = self.all_msgs()
        
        while True:
            m = self.mlog.recv_match(type=self.msgs)
            if m is None:
                del self.mlog.data_map
                self.mlog.filehandle.close()
                break
            
            timestamp = getattr(m, '_timestamp', 0.0)
            m_type = m.get_type()
            data_no_time = m.to_dict()
            del data_no_time['mavpackettype']
            data = {}
            if m_type != "FMT":
                data = {'timestamp' : timestamp}
            data.update(data_no_time)
            
            if self.dataframe.get(m_type) == None:
                self.dataframe[m_type] = {'Columns' : list(data.keys()), 
                                          'Values' : [list(data.values())]}
            elif timestamp == self.dataframe[m_type]['Values'][-1][0]  and m_type != "FMT":
                self.dataframe[m_type]['Values'][-1] = list(data.values())
            else:
                self.dataframe[m_type]['Values'].append(list(data.values()))
        
        for msg in self.dataframe.keys():
            self.dataframe[msg]['Columns'] = np.array(self.dataframe[msg]['Columns'])
            self.dataframe[msg]['Values'] = np.array(self.dataframe[msg]['Values'])


class function(analyzer, read_binary):
    def __init__(self, path, model):
        if not path:
            print("Please enter input path")
            sys.exit()

        self.path_file = Path(path)
        self.modules_check = extract_modules_from_model(model)

    def check_module(self):
        ls = {}
        for module in self.modules_check:
            status_module = self.analyze_module(module)
            ls[module] = status_module
        return ls

    def read_log(self, path):
        read_binary.__init__(self, path)
        self.read_bin()
            
    def check_file_in_dir(self):
        if os.path.isdir(self.path_file): 
            list_bin = [self.path_file / f for f in os.listdir(self.path_file) 
                        if f.split(".")[-1].lower() == "bin"]
        else:
            list_bin = [self.path_file]
        return list_bin

    def run(self):
        list_bin = self.check_file_in_dir()
        dc_log = {}
        for file in list_bin:
            self.read_log(file)
            dc_log[file.name] = self.check_module()
        return dc_log


def extract_modules_from_model(model):
    path = Path(__file__).resolve().parent / "models" / (model+".txt")
    with open(path, "r") as types:
        type = types.read().splitlines()
        return list(map(lambda type: type.lower(), type))


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', type=str, help='path log file')
    parser.add_argument('-m', '--model', type=str, default="STD" , help='model drone')
    opt = parser.parse_args()
    return opt


def main_log(path, model="STD"):
    log_analyze = function(path, model)
    result = log_analyze.run()
    file_name = result.keys()
    values = []
    first = 0
    for file in file_name:
        if not first:
            index_1_unique = result[file].keys()
            index_1 = []
            index_2 = []
        val = []
        for ind1 in index_1_unique:
            if not first:
                ind2 = list(result[file][ind1].keys())
                index_1 += [ind1]*len(ind2)
                index_2 += ind2
            val += list(result[file][ind1].values())
        first = 1
        values.append(val)
    values = np.array(values, dtype=object).T
    df = pd.DataFrame(values, index=[index_1, index_2], columns=file_name)
    return df


if __name__ == "__main__":
    opt = parse_opt()
    result = main_log(**vars(opt))
    for col in result.columns:
        print()
        print(f"________________________________{col}________________________________")
        print(result[col])