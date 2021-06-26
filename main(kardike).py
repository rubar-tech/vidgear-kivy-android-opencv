from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
from vidgear.gears import NetGear

# activate Bidirectional mode
options = {"bidirectional_mode": True}

# Define NetGear Client at given IP address and define parameters
# !!! change following IP address '192.168.x.xxx' with yours !!!
client = NetGear(
    address="192.168.8.101",
    port="5454",
    protocol="tcp",
    pattern=1,
    receive_mode=True,
    logging=True,
    **options
)

target_data = "Hi, I am a Client here."


class Kivygear(Image):
    def __init__(self, capture, fps, **kwargs):
        super(Kivygear, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        server_data, frame = client.recv(return_data=target_data)
        print(frame.shape)
        if not (server_data is None):
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            image_texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture


class vidgearApp(App):
    def build(self):
        self.capture = client.recv(return_data=target_data)
        self.my_camera = Kivygear(capture=self.capture, fps=60)
        return self.my_camera

    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()
        client.close()


if __name__ == '__main__':
    vidgearApp().run()