# -*- coding: utf-8 -*-
import pygame

# play audio
def play_audio(audio_name):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(audio_name)
        pygame.mixer.music.play(1)
        while pygame.mixer.music.get_busy():  # 在音频播放为完成之前不退出程序
            pass
    except Exception as e:
        print(e)
    