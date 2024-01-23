from pytube import YouTube, query
from pydub import AudioSegment
from typing import Tuple
import tkinter as tk
import pandas as pd
import requests
import re
import os

class VideoStream(YouTube):
    def __init__(self, url, *args, **kwargs):
        super().__init__(url, *args, **kwargs)
        self.check_availability()
        self.url = url
        self.video_path = './video/'
        self.audio_path = './audio/'
        self.videos_frame = None
        self.audios_frame = None
        self.thumbnail = None
        self.__stream_data()
        self.download_thumbnail()

    def __stream_data(self):
        
        video_re = re.compile(r'type="video"')
        audio_re = re.compile(r'type="audio"')

        audios = [str(stream) for stream in list(self.streams) if audio_re.search(str(stream))]
        videos = [str(stream) for stream in list(self.streams) if video_re.search(str(stream))]

        # audio    
        itag_list=[]
        mime_type_list=[]
        abr_list=[]
        acodec_list=[]
        progressive_list=[]
        type_list=[]

        for audio in audios:
            itag_list.append(audio.split('itag="')[1].split('"')[0])
            mime_type_list.append(audio.split('mime_type="')[1].split('"')[0])
            abr_list.append(audio.split('abr="')[1].split('"')[0])
            acodec_list.append(audio.split('acodec="')[1].split('"')[0])
            progressive_list.append(audio.split('progressive="')[1].split('"')[0])
            type_list.append(audio.split('type="')[1].split('"')[0])

        audio_data = {
        'itag' : itag_list,
        'mime_type' : mime_type_list,
        'abr (kbps)' : abr_list,
        'acodec' : acodec_list,
        'progressive' : progressive_list,
        'type' : type_list
        }

        audio_frame = pd.DataFrame(audio_data)
        audio_frame['itag'] = audio_frame['itag'].astype(int)
        audio_frame['abr (kbps)'] = audio_frame['abr (kbps)'].str.extract('(\d+)').astype(int)


        # video
        itag_list=[]
        mime_type_list=[]
        res_list=[]
        fps_list=[]
        vcodec_list=[]
        acodec_list=[]
        progressive_list=[]
        type_list=[]
        
        for video in videos:
            itag_list.append(video.split('itag="')[1].split('"')[0])
            mime_type_list.append(video.split('mime_type="')[1].split('"')[0])
            res_list.append(video.split('res="')[1].split('"')[0])
            fps_list.append(video.split('fps="')[1].split('"')[0])
            vcodec_list.append(video.split('vcodec="')[1].split('"')[0])
            progressive_list.append(video.split('progressive="')[1].split('"')[0])

            try:
                acodec_list.append(video.split('acodec="')[1].split('"')[0])
            except IndexError:
                acodec_list.append('N/A')

            type_list.append(video.split('type="')[1].split('"')[0])

        video_data = {
        'itag' : itag_list,
        'mime_type' : mime_type_list,
        'res' : res_list,
        'fps' : fps_list,
        'vcodec' : vcodec_list,
        'acodec' : acodec_list,
        'progressive' : progressive_list,
        'type' : type_list
        }

        video_frame = pd.DataFrame(video_data)    
        video_frame['itag'] = video_frame['itag'].astype(int)
        video_frame['res'] = video_frame['res'].str.extract('(\d+)').astype(int)
        video_frame['fps'] = video_frame['fps'].str.extract('(\d+)').astype(int)

        self.videos_frame = video_frame
        self.audios_frame = audio_frame
    
    def download_video(self, itag: int = -1):
    # global streams, video_path

        if itag != -1:
            self.streams.get_by_itag(itag).download(self.video_path)
            return

        max_res_videos = self.videos_frame[self.videos_frame['res'] == self.videos_frame['res'].max()]
        max_res_videos = max_res_videos.reset_index()

        # print(max_res_videos)
        # print('')

        mp4_videos = max_res_videos.loc[max_res_videos['mime_type'] == 'video/mp4']
        if mp4_videos.empty:
            itag = list(max_res_videos['itag'])[0]
        else:
            itag = list(mp4_videos['itag'])[0]

        self.streams.get_by_itag(itag).download(self.video_path)

    def download_audio(self, itag: int = -1):

        if itag != -1:
            streams.get_by_itag(itag).download(self.audio_path)
            return

        max_res_audios = self.audios_frame[self.audios_frame['abr (kbps)'] == self.audios_frame['abr (kbps)'].max()]
        max_res_audios = max_res_audios.reset_index()

        mp4_videos = max_res_audios.loc[max_res_audios['type'] == 'audio/mp4']

        if mp4_videos.empty:
            itag = list(max_res_audios['itag'])[0]
            convert = True
        else:
            itag = list(mp4_videos['itag'])[0]
            convert = False

        audio_filename = self.streams.get_by_itag(itag).download(self.audio_path)
        remove_filename = self.audio_path + audio_filename.split(self.audio_path)[1]

        if convert:
            audio_filename = self.audio_path + audio_filename.split(self.audio_path)[1]
            opus_audio = AudioSegment.from_file(audio_filename)
            audio_filename = audio_filename.split('.')
            audio_filename = '.' + audio_filename[-2] + '.wav'
            opus_audio.export(audio_filename,format='wav')

        os.remove(remove_filename)

    def download_thumbnail(self, full_res = False):
        thumbnail = requests.get(self.thumbnail_url)
        if thumbnail.status_code == 200:
            with open('thumbnail.jpg', 'wb') as file:
                file.write(thumbnail.content)
            self.thumbnail = thumbnail

def run():
    # url = input("url: ")
    url = "https://www.youtube.com/watch?v=JpSOSihBW9g"
    video = VideoStream(url)


if __name__ == "__main__":
    run()