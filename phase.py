from stages import *

toHLS = BGR2HLS()
toBGR = HLS2BGR()
source = ImageFileSource('samples/images/sunset.jpg')
cache, clear = Cache()
source = cache(toHLS(source()))
sink = Then(toBGR, ImageFileSink('output/phase.jpg'))

phase = ApplyToLayer(0, SlowPhase(20))
p2 = ApplyToLayer(2, SlowPhase(10, 256))

s = phase(source)
s = p2(s)
sink(s)()
