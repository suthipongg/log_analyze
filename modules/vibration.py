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
    x_y_z = (data_vibe[:, 1:4] >= 15).any()
    clip_x_y_z = (data_vibe[:, 4:] > 0).any()
    
    if x_y_z: 
        status_X_Y_Z = "error"
    else:
        status_X_Y_Z = "ok"
        
    if clip_x_y_z:
        status_clip_X_Y_Z = "error"
    else:
        status_clip_X_Y_Z = "ok"
        
    return ["_________________vibration_________________", f"X,Y,Z: {status_X_Y_Z}", 
            f"clip_X,Y,Z: {status_clip_X_Y_Z}"]