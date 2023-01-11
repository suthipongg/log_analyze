from pathlib import Path
import argparse
import numpy as np
from Reader import DFReader
from analyze import analyzer
import modules._msgs_module as _msgs_module
import sys, os

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))

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
                msg = _msgs_module.ls_msg_from_modules[module]
                all_use_msgs = all_use_msgs.union(set(msg))
            except Exception as e:
                print(e)
                print(module, "module not in dictionary module:messages")
        return all_use_msgs
    
    def read_bin(self):
        self.msgs = self.all_msgs()
        while True:
            m = self.mlog.recv_match(type=self.msgs)
            if m is None:
                break
            
            timestamp = getattr(m, '_timestamp', 0.0)
            m_type = m.get_type()
            data = {}
            if m_type != "FMT":
                data = {'timestamp' : timestamp}
            data.update(m.to_dict())
            del data['mavpackettype']
            
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


class check_module(analyzer, read_binary):
    def __init__(self, path, model="STD"):
        if not path:
            print("Please enter input path")
            sys.exit()
        
        path = Path(path)
        self.modules_check = extract_modules_from_model(model)
        read_binary.__init__(self, path)
        self.read_bin()

    def show(self):
        ls = []
        for module in self.modules_check:
            status_module = self.analyze_module(module)
            ls.append(status_module)
            print(status_module)


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
    status = check_module(**vars(opt))
    status.show()
    
    
if __name__ == "__main__":
    opt = parse_opt()
    main(opt)