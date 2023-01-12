import difflib


key_message = ["Low Battery", 
               "Critical Battery"
               ]

def analyze(self):
    msg_col = ["timestamp", "Message"]
    data_msg = self.pull_data('MSG', msg_col)
    msg = data_msg[:, 1].flatten()
    ls_error = []
    for key in key_message:
        error_msg = difflib.get_close_matches(key, msg, n=1, cutoff=0.6)
        if error_msg == []:
            continue
        ls_error.append(error_msg[0])
        
    return f"messagge: \n\
        data: \t{ls_error}"
    