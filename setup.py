from setuptools import setup, find_packages

setup(
    name="Video processor",
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'click==8.1.7',
        'ffmpeg-python==0.2.0',
        'future==0.18.3',
        'google-api-python-client==1.7.2',
        'google-auth==1.8.0',
        'oauth2client',
        'google-auth-httplib2==0.0.3',
        'google-auth-oauthlib==0.4.1'
    ],
    entry_points=
    '''
        [console_scripts]
        cut_video=video.processor:cut
        process_video=video.processor:cut_and_join
        process_and_upload_video=video.processor:cut_and_join_and_upload_to_youtube
    ''',
)