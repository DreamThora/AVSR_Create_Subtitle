#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2023 Imperial College London (Pingchuan Ma)
# Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)

import torch
import torchaudio
import torchvision
import math
import av
from .transforms import AudioTransform, VideoTransform


class AVSRDataLoader:
    def __init__(self, modality, speed_rate=1, transform=True, detector="retinaface", convert_gray=True):
        self.modality = modality
        self.transform = transform
        if self.modality in ["audio", "audiovisual"]:
            self.audio_transform = AudioTransform()
        if self.modality in ["video", "audiovisual"]:
            if detector == "mediapipe":
                from pipelines.detectors.mediapipe.video_process import VideoProcess
                self.video_process = VideoProcess(convert_gray=convert_gray)
            if detector == "retinaface":
                from pipelines.detectors.retinaface.video_process import VideoProcess
                self.video_process = VideoProcess(convert_gray=convert_gray)
            self.video_transform = VideoTransform(speed_rate=speed_rate)


    # def load_data(self, data_filename, landmarks=None, transform=True,i=None):
    #     if self.modality == "audio":
    #         audio, sample_rate = self.load_audio(data_filename)
    #         audio = self.audio_process(audio, sample_rate)
    #         return self.audio_transform(audio) if self.transform else audio
    #     if self.modality == "video":
    #         video = self.load_video(data_filename)
    #         video = self.video_process(video, landmarks)
    #         video = torch.tensor(video)
    #         return self.video_transform(video) if self.transform else video
    #     if self.modality == "audiovisual":
    #         rate_ratio = 640
    #         audio, sample_rate = self.load_audio(data_filename)
    #         audio = self.audio_process(audio, sample_rate)
    #         video = self.load_video(data_filename)
    #         #split
    #         video = self.video_process(video, landmarks)
    #         video = torch.tensor(video)
    #         min_t = min(len(video), audio.size(1) // rate_ratio)
    #         audio = audio[:, :min_t*rate_ratio]
    #         video = video[:min_t]
    #         if self.transform:
    #             audio = self.audio_transform(audio)
    #             video = self.video_transform(video)
    #         return video, audio
    def load_data(self, data_filename, landmarks=None, transform=True, i=None):
        if self.modality == "audio":
            audio, sample_rate = self.load_audio(data_filename)
            audio = self.audio_process(audio, sample_rate)
            return self.audio_transform(audio) if self.transform else audio
        if self.modality == "video":
            video = self.load_video(data_filename)  # ส่ง i ไปที่ load_video
            video = self.video_process(video, landmarks)
            video = torch.tensor(video)
            return self.video_transform(video) if self.transform else video
        if self.modality == "audiovisual":
            rate_ratio = 640
            audio, sample_rate = self.load_audio(data_filename,i)
            audio = self.audio_process(audio, sample_rate)
            video = self.load_video(data_filename,i)  # ส่ง i ไปที่ load_video
            # split
            video = self.video_process(video, landmarks)
            video = torch.tensor(video)
            min_t = min(len(video), audio.size(1) // rate_ratio)
            audio = audio[:, :min_t * rate_ratio]
            video = video[:min_t]
            if self.transform:
                audio = self.audio_transform(audio)
                video = self.video_transform(video)
            return video, audio

    def load_audio(self, data_filename, i):
        audio_timebase = torchvision.io._video_opt.default_timebase
        audio_start = 30 * i
        audio_end = 29 + (30 * i)
        with av.open(data_filename, metadata_errors="ignore") as container:
            if container.streams.audio:
                audio_timebase = container.streams.audio[0].time_base
        end_pts = int(math.ceil(audio_end * (1 / audio_timebase)))
        start_pts = int(math.floor(audio_start * (1 / audio_timebase)))
        # waveform, sample_rate = torchaudio.load(data_filename, normalize=True,)
        waveform, sample_rate = torchaudio.load(data_filename, normalize=True,frame_offset = start_pts,num_frames = end_pts-start_pts)
        return waveform, sample_rate

    def load_video(self,data_filename,i):
        vid_start = 30 * i
        vid_end = 29 + (30 * i)
        return torchvision.io.read_video(data_filename, pts_unit='sec',start_pts=vid_start,end_pts=vid_end)[0].numpy()
    
    def audio_process(self, waveform, sample_rate, target_sample_rate=16000):
        if sample_rate != target_sample_rate:
            waveform = torchaudio.functional.resample(waveform, sample_rate, target_sample_rate)
        waveform = torch.mean(waveform, dim=0, keepdim=True)
        return waveform
