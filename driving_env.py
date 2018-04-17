import argparse
import base64
from datetime import datetime
import os
import shutil
import time
import threading

import gym
import numpy as np
import socketio
import eventlet
import eventlet.wsgi

from PIL import Image
from flask import Flask
from io import BytesIO


class DrivingClient(threading.Thread):
    def __init__(self, record_path=""):
        threading.Thread.__init__(self)
        self.daemon = True

        self.throttle = 0
        self.steering_angle = 0
        self.observed_speed = 0
        self.observed_frame = np.zeros((160, 320, 3))
        self.observed_throttle = 0
        self.observed_steering_angle = 0

        # Connect to Udacity Simulator
        self.sio = socketio.Server()
        self.app = Flask(__name__)

        @self.sio.on("connect")
        def connect(sid, environ):
            print("connect ", sid)
            self.send_control()
            
        @self.sio.on("telemetry")
        def telemetry(sid, data):
            if data:
                # The current steering angle of the car
                self.observed_steering_angle = float(data["steering_angle"])
                # The current throttle of the car
                self.observed_throttle = float(data["throttle"])
                # The current speed of the car
                self.observed_speed = float(data["speed"])
                # The current image from the center camera of the car
                imgString = data["image"]
                image = Image.open(BytesIO(base64.b64decode(imgString)))
                self.observed_frame = np.asarray(image)

                self.send_control()

                # save frame
                if record_path != "":
                    timestamp = datetime.utcnow().strftime("%Y_%m_%d_%H_%M_%S_%f")[:-3]
                    image_filename = os.path.join(args.image_folder, timestamp)
                    image.save("{}.jpg".format(image_filename))
            else:
                # NOTE: DON'T EDIT THIS.
                self.sio.emit("manual", data={}, skip_sid=True)


        self.app = socketio.Middleware(self.sio, self.app)

    def run(self):
        eventlet.wsgi.server(eventlet.listen(("", 4567)), self.app)

    def send_control(self):
        # print(self.throttle, self.steering_angle)
        self.sio.emit(
            "steer",
            data={
                "steering_angle": self.steering_angle.__str__(),
                "throttle": self.throttle.__str__()
            },
            skip_sid=True)
    
    # Attempted env reset using socketio
    # socketio inconsistent in resetting environment
    
    # def reset(self):
    #     # print(self.throttle, self.steering_angle)
    #     print("Resetting environment")
    #     self.sio.emit(
    #         "reset",
    #         data={},
    #         skip_sid=True
    #         )

 
class DrivingEnv(gym.Env):
    def __init__(self, desired_speed=9, Kp=0.1, Ki=0.002):
        self.error = 0
        self.desired_speed = 0
        
        # Define action and observations
        # throttle, brake, steer left, steer right
        self.action_space = gym.spaces.MultiBinary(4)
        self.allowed_options = list(range(4))
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(160, 320, 3))

        # Launch client
        self.client = DrivingClient()
        self.client.start()

    def reset(self):
        # self.client.reset()
        self.error = 0

    def step(self, action):
        self.client.steering_angle = action[3] - action[2]
        self.client.throttle = action[0] - action[1]

        time.sleep(0.1)
        self.error += (self.client.observed_speed - self.desired_speed)**2
        # self.error += 1

        print(self.error)
        if self.error >=25000:
            print("Error >= 25000")
            return self.client.observed_frame, -self.error, True, dict()
        # observation, reward, done, ?
        return self.client.observed_frame, -self.error, False, dict()

    def seed(self):
        pass
