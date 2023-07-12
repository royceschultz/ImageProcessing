from stages import *

toHLS = BGR2HLS()
toBGR = HLS2BGR()
cache = Cache()
source1 = ImageFileSource('samples/images/beach.jpg')
source2 = ImageFileSource('samples/images/sunset.jpg')
source1 = cache(toHLS(source1()))
source2 = cache(toHLS(source2()))
sink = Then(toBGR, ImageFileSink('output/sunset.jpg'))

vloss = ApplyToLayer(0, VSyncLoss())
bgr2hls = BGR2HLS()
hls2bgr = HLS2BGR()
shiftHue = ApplyToLayer(0, AddMod(10, 180))

s = SetLayer(1)(vloss(source1), GetLayer(1)(source2))
s = cache(s)
s = shiftHue(s)

sink(s)()
