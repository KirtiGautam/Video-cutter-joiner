# Video Cutter and Joiner
This projects contains a python script which uses ffmpeg library to cut the portions of video given as input. You can also use this to cut out portions of the video and join the remaining pieces together.

## Installation
- Install the `ffmpeg` library from the official [site](https://www.ffmpeg.org/).
- Install python 3 from the official [site](https://www.python.org/downloads/release/python-31013/).
- From the root directory, run the following command:
```
pip install .
```

## Video Cutter
You can cut the portion of a video by mentioning the filename and timestamp you want out of that video. For example, If the filename is `my_video.mp4` and we want `00:04:05` to `00:05:10` duration out of the video then
```
cut_video --timestamp=00:04:05-00:05:10 --filename=my_video.mp4
```
Start and end timestamp are joined by `-` as mentioned in the above example


## Join multiple videos into one
You can join the multiple videos together into one by eliminatin the undesired portions out of original video, If the filename is `my_video.mp4` and we want `00:04:05` to `00:05:10` and `00:06:09` to `00:10:10` out of the original video then do
```
process_video --timestamps=00:04:05-00:05:10,00:06:09-00:10:10 --filename=my_video.mp4
```
Start and end timestamp are joined by `-` as mentioned in the above example. Multiple durations are joined by `,` which would be removed in the final video.
