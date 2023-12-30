from setuptools import setup, find_packages

setup(
    name="Video processor",
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'click==8.1.7',
        'ffmpeg-python==0.2.0',
        'future==0.18.3'
    ],
    entry_points=
    '''
        [console_scripts]
        cut_video=video.processor:cut
        process_video=video.processor:cut_and_join    
    ''',
)