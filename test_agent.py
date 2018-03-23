from driving_env import DrivingEnv


class ForwardAgent(object):
    """Always going forward agent"""
    def __init__(self, action_space):
        self.action_space = action_space

    def act(self, observation, reward, done):
        print(reward)
        return [1, 0, 0, 0]


if __name__ == '__main__':

    env = DrivingEnv()
    agent = ForwardAgent(env.action_space)
    episode_count = 1
    reward = 0.0
    done = False

    for i in range(episode_count):
        ob = env.reset()    # Start a new scenario
        while True:
            action = agent.act(ob, reward, done)    # Agent predict action
            ob, reward, done, _ = env.step(action)
            if done:    # One episode finishes
                break

    env.close()
