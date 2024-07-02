import gymnasium as gym
import numpy as np
from gymnasium import spaces
from godot_ml_agents_toolkit.godotenv import GodotEnv


def convert_to_list(arr):
    if isinstance(arr, np.ndarray):
        return arr.tolist()  # Convert NumPy array to Python list
    else:
        return arr  # Return as-is if it's not a NumPy array


possible_actions = [
    [-0.1, -0.1],
    [-0.1, 0.1],
    [0.1, -0.1],
    [0.1, 0.1],
    [-0.1, 0],
    [0, -0.1],
    [0, 0.1],
    [0.1, 0],
    [0, 0]
]


class GodotEnvWrapper(gym.Env):
    def __init__(self, game_path=None, tcp_port=5000, udp_port=5005, speed_up=None):
        super(GodotEnvWrapper, self).__init__()
        self.env = GodotEnv(game_path, tcp_port, udp_port, speed_up)

        # Define action and observation space
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(8,), dtype=np.float32)
        self.action_space = spaces.Discrete(9)

    def reset(self, seed=0, options=None):
        # Reset the environment and return the initial observation
        data = self.env.reset()
        data = data[0]
        state = data[3]
        info = {}
        return np.array(state, dtype=np.float32), info

    def step(self, action):
        continuous_action = np.array(possible_actions[action])
        action = convert_to_list(continuous_action)
        # Take a step in the environment with the given action
        self.env.set_action_to_send(0, action)  # Assuming single agent; modify if needed
        data = self.env.step(self.env.actions_to_send)
        data = data[0]
        self.env.actions_to_send = []

        obs = np.array(data[3], dtype=np.float32)
        reward = data[4]
        done = data[5]
        info = {}

        return obs, reward, done, False, info

    def render(self, mode='human'):
        # Render the environment (if needed)
        pass

    def close(self):
        # Close the environment
        self.env.close()
