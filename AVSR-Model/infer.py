# Copyright 2023 Imperial College London (Pingchuan Ma)
# Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)

import torch
import hydra
from pipelines.pipeline import InferencePipeline
from pipelines.model import AVSR
import math
from srt import *
import cv2

import sys
@hydra.main(version_base=None, config_path="hydra_configs", config_name="default")
def main(filename):
    cfg = {
    "gpu_idx": 0,  # Add this line
    # ... other configurations
    }
    #setup
    config_filename = "./LRS3_AV_WER0.9.ini"
    device = torch.device("cuda:0" if torch.cuda.is_available() and cfg.get("gpu_idx", 0) >= 0 else "cpu")
    detector = "mediapipe"
    inference_pipeline = InferencePipeline(config_filename, device=device, detector=detector, face_track=True)

    #all path
    data_filename = f"./files/origin_video/{filename}"
    vid_name = data_filename.split('/')[-1].split('.')[0]
    subtitle_path= f'./files/subtitle/{vid_name}.srt'
    merged_path = f'./files/merge_video/{filename}'
    thumbnail_path = f'./files/thumbnail/{vid_name}.png'

    print(f"Processing : {filename}")
    cap = cv2.VideoCapture(data_filename)
    dur = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / cap.get(cv2.CAP_PROP_FPS)
    n_loop = math.ceil(dur/30)
    sentence = []

    #get vid and sound
    for i in range(n_loop):
        data = inference_pipeline(data_filename, i=i)
        fps = data[0].size(dim=1)
        if fps > 75:
            n_loop = math.ceil(fps/75)
            for i in range(n_loop):
                if i+1 == n_loop:
                    vid = data[0][:, 75*i : -1, :, :]
                    sound = data[1][48000 * i : -1, :]
                    tup = (vid, sound)
                    hyp = inference_pipeline.model.infer(tup)
                    sentence.append(hyp)
                else:
                    vid = data[0][:, 75*i : (75*i) + 74, :, :]
                    sound = data[1][48000 * i : (48000*i) + 47999, :]
                    tup = (vid, sound)
                    hyp = inference_pipeline.model.infer(tup)
                    sentence.append(hyp)
        else:
            hyp = inference_pipeline.model.infer(data)
            sentence.append(hyp)
    print("*" *40)        
    print(sentence)
    print("*" *40)

    #post predicted
    create_srt_file(sentence, output_path= subtitle_path)
    merge_video_with_subtitle_ffmpeg(video_path = data_filename, subtitle_path=subtitle_path, output_path=merged_path)
    create_thumbnail(video_path=data_filename,thumbnail_path=thumbnail_path)


filename = sys.argv[1]
main(filename)
