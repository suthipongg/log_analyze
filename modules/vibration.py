def analyze(self):
    vibe_col = ["timestamp", "VibeX", "VibeY", "VibeZ", "Clip0", "Clip1", "Clip2"]
    data_vibe = self.pull_data('VIBE', vibe_col)
    x_y_z = sum(data_vibe[:, 1:4].flatten() >= 15)
    clip_x_y_z = sum(data_vibe[:, 4:].flatten() > 0)
    if x_y_z > 0 & clip_x_y_z > 0: return "vibration: \n\tX,Y,Z \t\terror \n\tclip_X,Y,Z error"
    elif x_y_z > 0: return "vibration: \n\tX,Y,Z: \t\terror \n\tclip_X,Y,Z: ok"
    elif clip_x_y_z > 0: return "vibration: \n\tX,Y,Z: \t\tok \n\tclip_X,Y,Z: error"
    else: return "vibration: \n\tX,Y,Z: \t\tok \n\tclip_X,Y,Z: \tok"