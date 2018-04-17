from driving_env import DrivingEnv
import os
import time
from pynput.keyboard import Key, Controller

class ForwardAgent(object):
    """Always going forward agent"""
    def __init__(self, action_space):
        self.action_space = action_space

    def act(self, observation, reward, done):
        return [1, 0, 0, 0]


if __name__ == '__main__':
    
    keyboard = Controller()

    env = DrivingEnv() # Create new driving env, with
    agent = ForwardAgent(env.action_space)
    reward = 0.0
    done = False
    episode_count = 500
    
    for i in range(episode_count):
        print("Episode: ", i)
        ob = env.reset()    # Start a new scenario
        count = 0
        while True:
            action = agent.act(ob, reward, done)    # Agent predict action
            ob, reward, done, _ = env.step(action)
            count = count + 1
            if done:
                done = False
                keyboard.press(Key.enter)   # Custom reset environment method 
                keyboard.release(Key.enter)
                time.sleep(2)
                break

    env.close()
