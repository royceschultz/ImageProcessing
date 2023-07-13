import cv2 as cv
from stages import *
import time

# cap = cv.VideoCapture('samples/videos/video.mp4')
cap = cv.VideoCapture('samples/videos/sunset.mp4')
# Get cap properties
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv.CAP_PROP_FPS))
# Total frames
total_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))

print(f'width: {width}, height: {height}, fps: {fps}')

writer = cv.VideoWriter('output/phase.mp4', cv.VideoWriter_fourcc(
    *'mp4v'), fps, (width, height))

source, setSource = VariableSource()
source = source()
source = BGR2HLS()(source)
s = ApplyToLayer(0, SlowPhase(10))(source)
# s = ApplyToLayer(1, VSyncLoss())(s)
s = VSyncLoss()(s)
s = HLS2BGR()(s)

count = 0
t_start = time.time()
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    count += 1
    dt = time.time() - t_start
    render_fps = count / dt
    print(f'{(count / total_frames):.3f} {render_fps:.1f}  ({count}) total: {total_frames}  ', end='\r')
    if count > 200:
        break

    setSource(frame)
    frame = s()
    writer.write(frame)

print()
cap.release()
writer.release()
