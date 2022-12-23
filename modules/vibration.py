def analyze(self):
    vibe_col = ["timestamp", "VibeX", "VibeY", "VibeZ", "Clip0", "Clip1", "Clip2"]
    data_vibe = self.pull_data('VIBE', vibe_col)
    x_y_z = sum(data_vibe[:, 1:4].flatten() >= 15)
    clip_x_y_z = sum(data_vibe[:, 4:].flatten() > 0)
    
    if x_y_z > 0 & clip_x_y_z > 0: 
        return "vibration: \n\
        X,Y,Z \t\terror \n\
        clip_X,Y,Z \terror"
    elif x_y_z > 0: 
        return "vibration: \n\
        X,Y,Z: \t\terror \n\
        clip_X,Y,Z: \tok"
    elif clip_x_y_z > 0: 
        return "vibration: \n\
        X,Y,Z: \t\tok \n\
        clip_X,Y,Z: \terror"
    else: 
        return "vibration: \n\
        X,Y,Z: \t\tok \n\
        clip_X,Y,Z: \tok"