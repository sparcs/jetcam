from .camera import Camera
import atexit
import cv2
from traitlets import Integer, observe


class USBCamera(Camera):

    capture_api_pref = Integer(default_value=cv2.CAP_ANY)
    capture_fps = Integer(default_value=30)
    capture_width = Integer(default_value=640)
    capture_height = Integer(default_value=480)
    capture_device = Integer(default_value=0)

    def __init__(self, *args, **kwargs):
        super(USBCamera, self).__init__(*args, **kwargs)
        self.cap = None
        self._init_video_capture(self.capture_api_pref)
        atexit.register(self.release_camera)

    def _init_video_capture(self, api_pref):
        try:
            self.release_camera()
            self.cap = self._video_capture(api_pref)
            re, image = self.cap.read()
            if not re:
                raise RuntimeError('Could not read image from camera.')
        except RuntimeError:
            raise RuntimeError('Could not initialize camera.')

    def release_camera(self):
        if self.cap is not None:
            try:
                self.cap.release()
            except Exception as ex:
                print('Could not clear previous camera setup.')
                print(getattr(ex, 'message', repr(ex)))

    def _video_capture(self, api_pref):
        if api_pref == cv2.CAP_GSTREAMER:
            return cv2.VideoCapture(self._gst_str(), api_pref)
        cap = cv2.VideoCapture(self.capture_device, api_pref)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.capture_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.capture_height)
        cap.set(cv2.CAP_PROP_FPS, self.capture_fps)
        return cap

    def _gst_str(self):
        return 'v4l2src device=/dev/video{} ! video/x-raw, width=(int){}, \
                height=(int){}, framerate=(fraction){}/1 ! videoconvert ! \
                video/x-raw, format=(string)BGR ! appsink'.format(
                    self.capture_device,
                    self.capture_width,
                    self.capture_height,
                    self.capture_fps)

    @observe('api_pref')
    def _api_pref_changed(self, change):
        if change['old'] != change['new']:
            self._init_video_capture(change['new'])

    def _read(self):
        re, image = self.cap.read()
        if re:
            image_resized = cv2.resize(image,
                                       (int(self.width), int(self.height)))
            return image_resized
        else:
            raise RuntimeError('Could not read image from camera')
