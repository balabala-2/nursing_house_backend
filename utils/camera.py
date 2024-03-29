# base_camera.py
import os
import threading
import time

import cv2

try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident


class CameraEvent(object):
    """An Event-like class that signals all active clients when a new frame is
    available.
    """

    def __init__(self):
        self.events = {}

    def wait(self):
        """Invoked from each client's thread to wait for the next frame."""
        ident = get_ident()
        if ident not in self.events:
            # this is a new client
            # add an entry for it in the self.events dict
            # each entry has two elements, a threading.Event() and a timestamp
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        """Invoked by the camera thread when a new frame is available."""
        now = time.time()
        remove = []
        for ident, event in self.events.items():
            if not event[0].isSet():
                # if this client's event is not set, then set it
                # also update the last set timestamp to now
                event[0].set()
                event[1] = now
            else:
                # if the client's event is already set, it means the client
                # did not process a previous frame
                # if the event stays set for more than 5 seconds, then assume
                # the client is gone and remove it
                if now - event[1] > 5:
                    remove.append(ident)

        for ident in remove:
            del self.events[ident]

    def clear(self):
        """Invoked from each client's thread after a frame was processed."""
        self.events[get_ident()][0].clear()


class BaseCamera(object):
    # thread = None  # background thread that reads frames from camera
    # frame = None  # current frame is stored here by background thread
    # last_access = 0  # time of last client access to the camera
    # event = CameraEvent()

    def __init__(self, video_url=0, stream=cv2.VideoCapture(0)):
        """Start the background camera thread if it isn't running yet."""
        self.video_url = video_url
        self.thread = None  # background thread that reads frames from camera
        self.frame = None  # current frame is stored here by background thread
        self.last_access = 0  # time of last client access to the camera
        self.event = CameraEvent()
        self.stream = stream
        self.isFile = False
        self.isCamera = False
        self.isUrl = False

        if os.path.isfile(video_url):
            self.isFile = True
        elif type(video_url) == int:
            self.isCamera = True
        else:
            self.isUrl = True

        if self.thread is None:
            self.last_access = time.time()

            # start background frame thread
            self.thread = threading.Thread(target=self._thread)
            self.thread.start()

            # wait until frames are available
            while self.get_frame() is None:
                time.sleep(0)

    def get_frame(self):
        """Return the current camera frame."""
        self.last_access = time.time()

        # wait for a signal from the camera thread
        self.event.wait()
        self.event.clear()

        return self.frame

    def frames(self):
        """"Generator that returns frames from the camera."""
        raise RuntimeError('Must be implemented by subclasses.')

    def _thread(self):
        """Camera background thread."""
        print('Starting camera thread.')
        frames_iterator = self.frames()  # call for frames method (Staticmethod)
        for frame in frames_iterator:
            self.frame = frame
            self.event.set()  # send signal to clients
            time.sleep(0)

            # if there hasn't been any clients asking for frames in
            # the last 10 seconds then stop the thread
            if time.time() - self.last_access > 10:
                frames_iterator.close()
                print('Stopping camera thread due to inactivity.')
                break
        self.thread = None


class Camera(BaseCamera):
    # video_url = 'rtmp://81.69.47.203:1935/hls/live'
    def __init__(self, video_url=0, stream=cv2.VideoCapture(0)):
        super().__init__(video_url, stream)

    # over-wride of BaseCamera class frames method
    def frames(self):
        while self.stream.isOpened():
            ret, img = self.stream.read()
            if ret:
                img = cv2.flip(img, 1)
                img = cv2.resize(img, (640, 360))
                if self.isFile:
                    cv2.waitKey(1)
                yield cv2.imencode('.jpg', img)[1].tobytes()
