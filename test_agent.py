from driving_env import DrivingEnv
import os

class ForwardAgent(object):
    """Always going forward agent"""
    def __init__(self, action_space):
        self.action_space = action_space

    def act(self, observation, reward, done):
        # print(reward)
        return [1, 0, 0, 0]


if __name__ == '__main__':

    # env = DrivingEnv()
    # agent = ForwardAgent(env.action_space)
    # reward = 0.0
    # done = False
    episode_count = 500
    
    for i in range(episode_count):
        print("Episode: ", i)
        env = DrivingEnv()
        agent = ForwardAgent(env.action_space)
        reward = 0.0
        done = False
        ob = env.reset()    # Start a new scenario
        count = 0
        while True:
            # print(count)
            action = agent.act(ob, reward, done)    # Agent predict action
            ob, reward, done, _ = env.step(action)
            count = count + 1
            if done:
                # os.execv('test_agent.py', [])  
                break

    env.close()
