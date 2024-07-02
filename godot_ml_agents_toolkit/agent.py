class Agent:
    def __init__(self, agent_id, agent_type, team, observation_space, continuous_action_space, discrete_action_space):
        self.id = agent_id
        self.type = agent_type
        self.team = team
        self.observation_space = observation_space
        self.continuous_action_space = continuous_action_space
        self.discrete_action_space = discrete_action_space
        self.done = False
        self.current_observation = None
        self.current_reward = None
        self.last_action = None
        self.agent_func = None

    def set_observation(self, observation):
        self.current_observation = observation

    def set_reward(self, reward):
        self.current_reward = reward

    def set_done(self, done):
        self.done = done

    def set_last_action(self, last_action):
        self.last_action = last_action

    def register_agent_func(self, agent_func):
        self.agent_func = agent_func

    def run(self, env, observation, reward, done, a_id):
        self.agent_func(env, observation, reward, done, a_id)
