import cv2

class Settings:
    def __init__(self, n_trackbar):
        def nothing(x):
            pass

        # Create a window
        cv2.namedWindow('settings')

        self.trackbar_names = []

        for i in range(n_trackbar):
            self.trackbar_names.append(str(i))
            cv2.createTrackbar(str(i), 'settings', 0, 255, nothing)

    def update_settings_window(self, frame):
        """ Returns the key pressed """
        cv2.imshow('settings', frame)
        return cv2.waitKey(1)

    def settings_window_closed(self):
        return cv2.getWindowProperty('settings', 0) < 0

    def get_settings_window_values(self):
        try:
            return [cv2.getTrackbarPos(trackbar_name, 'settings') for trackbar_name in self.trackbar_names]
        except AttributeError:
            raise (Exception("Settings Window not initialised correctly"))