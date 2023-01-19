from pathlib import Path
import argparse
import numpy as np
from Reader import DFReader
from analyze import analyzer
import modules._msgs_module as _msgs_module
import sys, os
from datetime import datetime


class read_binary:
    def __init__(self, path):
        self.path = path
        self.mlog = DFReader.DFReader_binary(self.path)
        self.match_types = list(self.mlog.name_to_id.keys())
        self.match_types.sort()
        self.dataframe = {}
        self.msgs = []
        self.data_one_file = []
    
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
        if self.all_msg:
            self.msgs = list(self.mlog.name_to_id.keys())
        else:
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
            
            if self.save_one_file:
                date_time = datetime.fromtimestamp(timestamp)
                self.data_one_file.append(str(date_time)+": "+m_type+" "+str(data_no_time))
            
            if self.analyzation or self.save_file_type:
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
        
        if self.analyzation:
            for msg in self.dataframe.keys():
                self.dataframe[msg]['Columns'] = np.array(self.dataframe[msg]['Columns'])
                self.dataframe[msg]['Values'] = np.array(self.dataframe[msg]['Values'])


class function(analyzer, read_binary):
    def __init__(self, path, model="STD", analyzation=False,
                 save_file_type=None, all_msg=False, path_out_file=None, save_one_file=False):
        if not path:
            print("Please enter input path")
            sys.exit()
        
        self.path_file = Path(path)
        self.modules_check = extract_modules_from_model(model)
        self.analyzation = analyzation
        self.save_file_type = save_file_type
        self.all_msg = all_msg
        if not path_out_file:
            path_out_file = self.path_file.parent
        self.path_out_file = Path(path_out_file)
        self.path_out_file_type = Path(path_out_file)
        self.path_out_one_file = Path(path_out_file)
        if os.path.isdir(self.path_file): 
            if save_file_type:
                create_dir_out = str(self.path_file.name) + "_" +  save_file_type
                self.path_out_file_type = self.check_file_name(self.path_out_file, create_dir_out, mkdir=True)
            if save_one_file:
                create_dir_out = str(self.path_file.name) + "_one"
                self.path_out_one_file = self.check_file_name(self.path_out_file, create_dir_out, mkdir=True)
        self.save_one_file = save_one_file
        self.log_file_name = ""
        
        self.run()

    def check_file_name(self, path_out, name, ext="", mkdir=False):
        extention = ""+ext
        n = 0
        ls_dir = os.listdir(path_out)
        while 1:
            if name+extention in ls_dir:
                n += 1
                extention = "_(" + str(n) + ")" + ext
            else:
                name_ext = name+extention
                path = path_out / name_ext
                if mkdir:
                    os.mkdir(path)
                return path

    def save_in_one_file(self):
        path = self.check_file_name(self.path_out_one_file, self.log_file_name, ext=".txt")
        with open(path, 'w') as outfile:
            outfile.write('\n'.join(self.data_one_file))
    
    def save_json(self):
        import json
        path = self.check_file_name(self.path_out_file_type, self.log_file_name, mkdir=True)
        for msg in self.dataframe.keys():
            data_msg = self.dataframe[msg]
            if self.analyzation:
                data_msg['Columns'] = data_msg['Columns'].tolist()
                data_msg['Values'] = data_msg['Values'].tolist()
                
            with open(path / str(msg+".json"), 'w') as outfile:
                json.dump(data_msg, outfile)
            
    def save_csv(self):
        import csv
        path = self.check_file_name(self.path_out_file_type, self.log_file_name, mkdir=True)
        for msg in self.msgs:
            if self.dataframe.get(msg) == None: 
                continue
            column = self.dataframe[msg]['Columns']
            value = self.dataframe[msg]['Values']
            with open(path / str(msg+".csv"), 'w', newline='') as f:
                write = csv.writer(f)
                write.writerow(column)
                write.writerows(value)

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
            if self.analyzation:
                if len(list_bin) == 1:
                    dc_log = self.check_module()
                dc_log[file.name] = self.check_module()
                
            self.log_file_name = file.stem
            if self.save_one_file: 
                self.save_in_one_file()
                
            if self.save_file_type:
                if self.save_file_type == "csv":
                    self.save_csv()
                elif self.save_file_type == "json":
                    self.save_json()
                else:
                    print(self.save_file_type, "file type not found")    
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
    parser.add_argument('-z', '--analyzation', default=False , action='store_true', help='analyze action')
    parser.add_argument('-sf', '--save_file_type', type=str, default=None , help='file type save')
    parser.add_argument('-a', '--all_msg', default=False , action='store_true', help='save all msg')
    parser.add_argument('-po', '--path_out_file', type=str, default=None , help='path file output')
    parser.add_argument('-sn', '--save_one_file', default=False , action='store_true', help='save in one file')
    opt = parser.parse_args()
    return opt


def main(opt):
    log_analyze = function(**vars(opt))
    result = log_analyze.run()
    print(result)
    
    
if __name__ == "__main__":
    opt = parse_opt()
    main(opt)