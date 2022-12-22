import sys
from pathlib import Path
import argparse
import numpy as np
from Reader import DFReader
from analyze import analyze


class read_binary(analyze):
    def __init__(self, path, modules_check):
        analyze.__init__(self)
        
        self.path = path
        self.modules_check = modules_check
        self.mlog = DFReader.DFReader_binary(self.path)
        self.match_types = list(self.mlog.name_to_id.keys())
        self.match_types.sort()

        self.dataframe = {}


    def all_msgs(self):
        all_use_msgs = set()
        
        for module in self.modules_check:
            if module not in list(self.ls_msg_from_type.keys()):
                print(module, "module not found")
                sys.exit()
                
            msg = self.ls_msg_from_type[module]
            all_use_msgs = all_use_msgs.union(set(msg))
            
        return all_use_msgs
    
    
    def read_bin(self):
        while True:
            m = self.mlog.recv_match(type=self.all_msgs())
            
            if m is None:
                break
            
            timestamp = getattr(m, '_timestamp', 0.0)
            data_timestamp = m.to_dict()
            m_type = m.get_type()
            del data_timestamp['mavpackettype']
            data_timestamp['timestamp'] = timestamp
            
            if self.dataframe.get(m_type) == None:
                self.dataframe[m_type] = {'Columns' : np.array(list(data_timestamp.keys())), 'Values' : [list(data_timestamp.values())]}
            elif timestamp == last_timestamp:
                self.dataframe[m_type]['Values'][-1] = list(data_timestamp.values())
            else:
                self.dataframe[m_type]['Values'].append(list(data_timestamp.values()))

            last_timestamp = timestamp
            
        for msg in self.dataframe.keys():
            self.dataframe[msg]['Values'] = np.array(self.dataframe[msg]['Values'])


class check_type(read_binary):
    def __init__(self, path, model="ALL"):
        read_binary.__init__(self, path, type_model(model))
        self.read_bin()


    def show(self):
        ls = []
        for type in self.modules_check:
            status_type = self.analyze_module(type)
            ls.append(status_type)
            print(status_type)


def type_model(model):
    path = Path(__file__).resolve().parent / "models" / (model+".txt")
    with open(path, "r") as types:
        type = types.read().splitlines()
        return list(map(lambda type: type.lower(), type))


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', type=str, help='path log file')
    parser.add_argument('-m', '--model', type=str, default="ALL" , help='model drone')
    opt = parser.parse_args()
    return opt


def main(opt):
    status = check_type(**vars(opt))
    status.show()
    
    
if __name__ == "__main__":
    opt = parse_opt()
    main(opt)