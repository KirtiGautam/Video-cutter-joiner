from typing import List

from moviepy.editor import VideoFileClip, concatenate_videoclips


class Cutter:
    __clip: VideoFileClip
    __path: str

    def __init__(self, *, path: str) -> None:
        self.__path = path
        self.__clip = VideoFileClip(self.__path)
    
    def __cut_portions(self, *, timestamps: List[str]) -> List[VideoFileClip]:
        clips: List[VideoFileClip] = []
        for timestamp in timestamps:
            start, end = timestamp.split('-')
            clips.append(self.__clip.subclip(start, end))
        return clips

    def __join_portions(self, *, portions: List[VideoFileClip]) -> VideoFileClip:
        final_clip = concatenate_videoclips(portions)
        return final_clip

    def cut_and_join(self) -> str:
        path, extension = self.__path.split('.')
        portions: List[VideoFileClip] = self.__cut_portions(timestamps=['00:00:00-00:00:10', '00:00:20-00:00:30'])
        final_clip: VideoFileClip =  self.__join_portions(portions=portions)
        final_clip.write_videofile(f'{path}_final.{extension}', audio_bitrate='50k', codec='libvpx-vp9',
                     threads='12', bitrate='8000k')
    

if __name__ == '__main__':
    cutter = Cutter(path='')
    cutter.cut_and_join()
