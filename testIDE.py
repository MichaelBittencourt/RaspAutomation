import picamera
camera = picamera.PiCamera()
camera.capture('michael.jpg')
camera.close()
camera.contrast(100)
camera.capture('michael2.jpg') 