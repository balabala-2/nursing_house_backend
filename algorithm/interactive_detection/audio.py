# import os
# while True:
#     os.system('ffmpeg -re -i 1.mp4 -vcodec copy -acodec copy -f flv rtmp://81.69.47.203:1935/hls/live')


# import os
# os.system(
#     'ffmpeg '
#     '-i rtmp://81.69.47.203:1935/hls/lyh '
#     '-map 0:a '
#     '-f segment '
#     '-segment_time 10 '
#     'output_%01d.wav') # 拉流

# import ffmpeg
# ffmpeg.input('output_1.wav').output('demo.wav', ar=16000, ac=1).run()

import os
import ffmpeg
import time
from aip import AipSpeech
from algorithm.utils.global_variable import interactive_detection_url
import subprocess

class Audio_detection:
    
    APP_ID = '26674325'
    API_KEY = 'vzCfHyZSu41DWR6wVRtwGHr9'
    SECRET_KEY = 'BT0NpRduGodP7vT1ShWodhhRjb9aVKB4'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    file_root_path = 'resources/audio_rtmp/'
    cur_file_idx = 0
    text = ''

    @classmethod
    def init(cls):
        Audio_detection.cur_file_idx = 0
        Audio_detection.text = ''
        
    # 拉流
    @classmethod
    def pull_flow(cls):
        os.system('ffmpeg '
                  '-rw_timeout 5000000 '
                  '-fflags +igndts '
                  f'-i {interactive_detection_url} '
                  '-ac 1 '
                  '-ar 16000 '
                  '-f segment '
                  '-segment_time 10 '
                  'resources/audio_rtmp/output_%01d.wav')
        # subprocess.run(
        #     [
        #         'ffmpeg',
        #         '-rw_timeout', '5000000',
        #         '-fflags', '+igndts',
        #         '-i', f'{interactive_detection_url}',
        #         '-ac', '1',
        #         '-ar', '16000',
        #         '-f', 'segment',
        #         '-segment_time', '10',
        #         'resources/audio_rtmp/output_%01d.wav'
        #     ]
        # )

    @classmethod
    def handle_wav(cls):
        files = os.listdir(Audio_detection.file_root_path)
        while len(files) > 0:
            file_path = Audio_detection.file_root_path + f'/output_{Audio_detection.cur_file_idx}.wav'
            audio_file = open(file_path,'rb').read()
            text = Audio_detection.get_text(audio_file)
            os.system(f'rm {file_path}')
            Audio_detection.text += text
            Audio_detection.cur_file_idx += 1
            files = os.listdir(Audio_detection.file_root_path)

    @classmethod
    def run(cls):
        os.system('rm -rf resources/audio_rtmp/*')
        Audio_detection.pull_flow()
        Audio_detection.handle_wav()

    @classmethod
    def get_text(cls, wav_bytes):
        result = Audio_detection.client.asr(wav_bytes, 'wav', 16000, {'dev_pid': 1536,})
        try:
            text = ','.join(result['result'])
        except Exception as e:
            print(e)
            text = ""
        return text

