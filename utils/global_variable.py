import torch
video_width = 640
video_height = 360

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
