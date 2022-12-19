import numpy as np
from pymavlink import DFReader
from type_check import check_status
import sys

class read_binary(check_status):
    def __init__(self, path, type_check):
        check_status.__init__(self)
        
        self.path = path
        self.type_check = list(map(lambda type: type.lower(), type_check))
        self.mlog = DFReader.DFReader_binary(self.path)
        self.match_types = list(self.mlog.name_to_id.keys())
        self.match_types.sort()

        self.data = {}

    def all_msgs(self):
        use_msg = set()
        for type in self.type_check:
            if type not in list(self.ls_msg_from_type.keys()):
                print(type, "type not found")
                sys.exit()
            msg = self.ls_msg_from_type[type]
            use_msg = use_msg.union(set(msg))
        return use_msg
    
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
            if self.data.get(m_type) == None:
                self.data[m_type] = {'Columns' : np.array(list(data_timestamp.keys())), 'Values' : [list(data_timestamp.values())]}
            elif timestamp == last_timestamp:
                self.data[m_type]['Values'][-1] = list(data_timestamp.values())
            else:
                self.data[m_type]['Values'].append(list(data_timestamp.values()))

            last_timestamp = timestamp
        for msg in self.data.keys():
            self.data[msg]['Values'] = np.array(self.data[msg]['Values'])


class check_type(read_binary):
    def __init__(self, path, type_check):
        read_binary.__init__(self, path, type_check)
        self.read_bin()

    def show(self):
        ls = []
        for type in self.type_check:
            status_type = check_status.__call__(self, type)
            ls.append(status_type)
            print(status_type)


if __name__ == "__main__":
    path = r"C:\Users\Lenovo\Desktop\log_bin\Drone30LOutOfControl.bin"
    type_check = ["battery", "Gps"]
    status = check_type(path, type_check)
    status.show()