import picamera
from time import sleep

camera = picamera.PiCamera()
camera.capture('image.jpg')
#camera.hflip = True
camera.vflip = True
camera.sharpness = 0
camera.contrast = 0
camera.brightness = 50
camera.saturation = 0
camera.ISO = 0
camera.video_stabilization = False
camera.exposure_compensation = 0;
camera.start_preview()
#sleep(5)
camera.capture('image2.jpg')
camera.stop_preview()

camera.start_preview()
#camera.start_recording('video.h264')
camera.start_recording('video.mjpeg')
for i in range(100):
    camera.brightness = i
    sleep(0.2)
camera.stop_recording()
camera.stop_preview()


