import numpy as np

# create list that contain all necessary message in "msg" variable (name variable is "msg" only)
msg = ["VIBE"]

# analyze log finction (name function is "analyze" only and have only 1 argument is "self")
def analyze(self):
    # create list that contain all necessary column for each message
    vibe_col = ["timestamp", "VibeX", "VibeY", "VibeZ", "Clip0", "Clip1", "Clip2"]
    
    # use function to pull data from log reader in dictionary type variable
    # return to numpy 2d array type sorted column by inut of column message list input
    data_vibe = self.pull_data('VIBE', vibe_col)
    
    # write condition to check error for each message
    thresh_x_y_z_val = 15
    thresh_clip_x_y_z_val = 0
    x_y_z_check = data_vibe[:, 1:4] >= thresh_x_y_z_val
    clip_x_y_z_check = data_vibe[:, 4:] > thresh_clip_x_y_z_val
    x_y_z = x_y_z_check.any()
    clip_x_y_z = clip_x_y_z_check.any()
    
    if x_y_z: 
        arg_max = np.argmax(x_y_z_check)
        row = arg_max // 3
        col = arg_max % 3
        status_X_Y_Z = "error"
        sign_x_y_z = " >= "
    else:
        arg_max = np.argmax(data_vibe[:, 1:4])
        row = arg_max // 3
        col = arg_max % 3
        status_X_Y_Z = "ok"
        sign_x_y_z = " < "
    x_y_z_val = round(data_vibe[:, 1:4][row , col], 2)
    
    if clip_x_y_z:
        arg_max = np.argmax(clip_x_y_z_check)
        row = arg_max // 3
        col = arg_max % 3
        status_clip_X_Y_Z = "error"
        sign_clip_x_y_z = " > "
    else:
        arg_max = np.argmax(data_vibe[:, 4:])
        row = arg_max // 3
        col = arg_max % 3
        status_clip_X_Y_Z = "ok"
        sign_clip_x_y_z = " <= "
    clip_x_y_z_val = round(data_vibe[:, 4:][row , col], 2)
    
    dict_data = {"x_y_z" : status_X_Y_Z + ": max x_y_z is " + str(x_y_z_val) + sign_x_y_z + str(thresh_x_y_z_val),
                 "clip_x_y_z" : status_clip_X_Y_Z + ": max clip_x_y_z is " + str(clip_x_y_z_val) + sign_clip_x_y_z + str(thresh_clip_x_y_z_val)}
        
    return dict_data