def analyze(self):
    vibe_col = ["timestamp", "VibeX", "VibeY", "VibeZ", "Clip0", "Clip1", "Clip2"]
    data_vibe = self.pull_data('VIBE', vibe_col)
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
        
    return f"vibration: \n\
        X,Y,Z: \t\t{status_X_Y_Z} \n\
        clip_X,Y,Z: \t{status_clip_X_Y_Z}"