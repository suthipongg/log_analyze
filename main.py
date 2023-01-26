from pathlib import Path
import argparse
import numpy as np
from Reader import DFReader
from analyze import analyzer
import sys, os
import importlib


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
    def __init__(self, path, model="STD"):
        if not path:
            print("Please enter input path")
            sys.exit()

        self.path_file = Path(path)
        self.modules_check = extract_modules_from_model(model)

    def check_module(self):
        ls = []
        for module in self.modules_check:
            status_module = self.analyze_module(module)
            ls.append(status_module)
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
            if len(list_bin) == 1:
                dc_log = self.check_module()
            else:
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


def main(opt):
    log_analyze = function(**vars(opt))
    result = log_analyze.run()
    for i in result:
        if type(i) == str:
            i = [i]
        for j in i:
            print(j)
    
    
if __name__ == "__main__":
    opt = parse_opt()
    main(opt)