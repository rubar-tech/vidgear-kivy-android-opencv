# import required libraries
from vidgear.gears import VideoGear
from vidgear.gears import NetGear
import cv2

# open pi video stream with defined parameters
stream = VideoGear(source=0, resolution=(640, 480), framerate=30).start()

# activate Bidirectional mode
options = {"bidirectional_mode": True}

# Define NetGear server at given IP address and define parameters
# !!! change following IP address '192.168.x.xxx' with client's IP address !!!
server = NetGear(
    address="192.168.8.104",
    port="5454",
    protocol="tcp",
    pattern=1,
    logging=True,
    **options
)  #

# loop over until KeyBoard Interrupted
while True:

    try:
        # read frames from stream
        frame = stream.read()

        # check for frame if Nonetype
        if frame is None:
            break

        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # {do something with the frame here}

        # prepare data to be sent(a simple text in our case)
        target_data = "Hello, I am a Server."

        # send frame & data and also receive data from Client
        recv_data = server.send(frame, message=target_data)

        # print data just received from Client
        if not (recv_data is None):
            print(recv_data)

    except KeyboardInterrupt:
        break

# safely close video stream
stream.stop()

# safely close server
server.close()
