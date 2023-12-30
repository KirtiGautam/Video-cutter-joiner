from typing import List

import click
import ffmpeg
import os
import shutil

class Cutter:
    __path: str
    __extension: str
    __timestamps: List[str]

    def __init__(self, *, path: str, timestamps: List[str]) -> None:
        self.__path, self.__extension = path.split('.')
        self.__timestamps = timestamps
        if not os.path.exists(f'./{self.__path}'):
            os.mkdir(f'./{self.__path}')
        shutil.move(f'./{self.__path}.{self.__extension}', f'./{self.__path}/{self.__path}.{self.__extension}')
        os.chdir(f'./{self.__path}')

    def __cut(self, *, start: str, end: str, suffix: str) -> str:
        ffmpeg.input(f'./{self.__path}.{self.__extension}', ss=start, to=end).output(f'./{self.__path}_{suffix}.{self.__extension}').run()
        
    def __cut_portions(self):
        for number, timestamp in enumerate(self.__timestamps):
            start, end = timestamp.split('-')
            self.__cut(
                start=start,
                end=end,
                suffix=number
            )

    def __join_portions(self):
        open(f'./concat.txt', 'w').writelines([(f'file {self.__path}_{number}.{self.__extension}\n') for number in range(0, len(self.__timestamps))])
        ffmpeg.input(f'./concat.txt', format='concat', safe=0).output(f'./{self.__path}_final.{self.__extension}', c='copy').run()
        os.remove(f'./concat.txt')

    def cut_and_join(self) -> str:
        self.__cut_portions()
        self.__join_portions()
        for number in range(0, len(self.__timestamps)):
            os.remove(f'./{self.__path}_{number}.{self.__extension}')
        os.chdir('..')
        return f'{self.__path}/{self.__path}_final.{self.__extension}'
    
    def cut(self) -> str:
        start, end = self.__timestamps[0].split('-')
        self.__cut(
            start=start,
            end=end,
            suffix='final'
        )
        os.chdir('..')
        return f'{self.__path}/{self.__path}_final.{self.__extension}'


@click.command()
@click.option('--timestamps', default='', required=True,
              help='Comma separated duration timestamps, eg. 00:00:00-00:01:30,00:19:40-00:20:00')
@click.option('--filename', required=True,
              help='Filename which needs to be cut and joined based on the duration timestamp')
def cut_and_join(*, filename: str, timestamps: str):
    timestamps = timestamps.split(',')
    if len(timestamps) > 0:
        cutter = Cutter(
            path=filename,
            timestamps=timestamps
        )
        filepath: str = cutter.cut_and_join()
        print(f'Video saved to {filepath}')


@click.command()
@click.option('--timestamp', default='', required=True,
              help='Duration timestamp, eg. 00:00:00-00:01:30')
@click.option('--filename', required=True,
              help='Filename which needs to be cut and joined based on the duration timestamp')
def cut(*, filename: str, timestamp: str):
    cutter = Cutter(
        path=filename,
        timestamps=[timestamp]
    )
    filepath: str = cutter.cut()
    print(f'Video saved to {filepath}')
