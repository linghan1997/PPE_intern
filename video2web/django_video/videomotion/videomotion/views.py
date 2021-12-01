from . import singlemotiondetector
import datetime
from django.http import StreamingHttpResponse
import cv2
import threading
from imutils.video import VideoStream
import imutils
import time
from django.views.decorators import gzip

# initialization
outputFrame = None
lock = threading.Lock()

vs = VideoStream(src=0).start()
time.sleep(1.0)


def detect_motion(frameCount):
    # frameCount: the minimum number of required frames to build up the background bg
    global vs, outputFrame, lock

    md = singlemotiondetector.SingleMotionDetector(accumWeight=0.1)
    total = 0

    # loop over frames from the video stream
    while True:
        # read the next frame size from the video stream and resize it
        # convert the frame to grayscale, and blur it
        frame = vs.read()
        # the smaller our input frame is, the less data there is, and thus the faster the algorithm will run
        frame = imutils.resize(frame, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # grab the current timestamp and draw it on the frame
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        # if the total number of frames has reached a sufficient number to construct a reasonable bg
        # then continue to process the frame
        if total > frameCount:
            # detect the motion in the image
            motion = md.detect(gray)

            # check to see if motion was found in the frame
            if motion is not None:
                # unpack the tuple and draw the box surrounding the "motion area" on the output frame
                (thresh, (minX, minY, maxX, maxY)) = motion
                cv2.rectangle(frame, (minX, minY), (maxX, maxY), (0, 0, 255), 2)

        # update the bg and increment the total number of frame read thus far
        md.update(gray)
        total += 1

        # acquire the lock, set the output frame, and release the lock
        with lock:
            outputFrame = frame.copy()


# generator (using yield)
def generate():
    global outputFrame, lock

    while True:
        with lock:
            if outputFrame is None:
                continue

            (flag, encodedImage) = cv2.imencode('.jpg', outputFrame)

            if not flag:
                continue

        # frame = camera.get_frame()
        yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n\r\n'


@gzip.gzip_page
def video_feed(request):
    try:
        t = threading.Thread(target=detect_motion, args=(32,))
        t.daemon = True
        t.start()

        return StreamingHttpResponse(generate(), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass
