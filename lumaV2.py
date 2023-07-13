from stages import *

toHLS = BGR2HLS()
toBGR = HLS2BGR()
source1 = ImageFileSource('samples/images/beach.jpg')
source2 = ImageFileSource('samples/images/sunset.jpg')
cache, clear = Cache()
source1 = cache(toHLS(source1()))
cache, clear = Cache()
source2 = cache(toHLS(source2()))
sink = Then(toBGR, ImageFileSink('output/sunset.jpg'))

vloss = ApplyToLayer(0, VSyncLoss())
bgr2hls = BGR2HLS()
hls2bgr = HLS2BGR()
shiftHue = ApplyToLayer(0, AddMod(10, 180))

s = SetLayer(1)(vloss(source1), GetLayer(1)(source2))
cache, clear = Cache()
s = cache(s)
s = shiftHue(s)

sink(s)()
