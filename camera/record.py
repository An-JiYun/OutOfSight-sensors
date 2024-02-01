import subprocess# 비디오 녹화 (30초 동안)
video_file = '/home/rpi/Videos/videoTest.mp4'
subprocess.run(['ffmpeg', '-f', 'v4l2', '-framerate', '25', '-video_size', '640x480', '-i', '/dev/video0', '-t', '30', video_file])
