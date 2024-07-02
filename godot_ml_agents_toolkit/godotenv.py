import socket
from gymnasium import spaces

from .gdtype import binaryapiv4 as binaryapi
from .agent import Agent


class GodotEnv:
    def __init__(
            self,
            game_path: str = None, tcp_port: int = 5000,
            udp_port: int = 5005,
            speed_up: int = None
    ):
        print("Initializing GodotEnv")
        self.game_path = game_path
        self.tcp_port = tcp_port
        self.udp_port = udp_port
        self.num_agents = None
        self.speed_up = speed_up

        self.agents = []
        self.agents_to_train = []
        self.actions_to_send = []

        self.tcp_connection, self.udp_connection = self._start_server()
        self._establish_client_connection()
        self._init_environment_info()

    def _establish_client_connection(self):
        data = self.tcp_connection.recv(1024)
        if data == b"handshake":
            message = "handshake"
            self._send_tcp_message(message)
            print("Connection established")

    def _start_server(self):
        sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        server_address_tcp = ('localhost', self.tcp_port)
        server_address_udp = ('localhost', self.udp_port)

        sock_tcp.bind(server_address_tcp)
        sock_udp.bind(server_address_udp)

        sock_tcp.listen(1)
        tcp_connection, client_address = sock_tcp.accept()

        print('Connection from', client_address)
        return tcp_connection, sock_udp

    def _init_environment_info(self):
        message = self.process_data()
        self.num_agents = message[0]

        message = message[1:len(message)]
        for agent_data in message:
            a_id = agent_data[0]
            a_type = agent_data[1]
            a_team = agent_data[2]
            a_observation_space = agent_data[3]
            a_cont_action_space = agent_data[4]
            a_disc_action_space = agent_data[5]

            cont_space = None
            disc_space = None
            if a_cont_action_space > 0:  # Continuous actions present
                cont_space = spaces.Box(low=-1.0, high=1.0, shape=(a_cont_action_space,))
            if a_disc_action_space > 0:  # Discrete actions present
                disc_space = spaces.Discrete(a_disc_action_space)
            agent = Agent(a_id, a_type, a_team, a_observation_space, cont_space, disc_space)
            print(
                f"Agent {a_id}, type: {a_type}, team: {a_team}, obs space: {a_observation_space}, actions (Cont,Disc): "
                f"{a_cont_action_space, a_disc_action_space}")

            self.agents.append(agent)

    # change "learn" to "run"
    def run(self):
        for agent in self.agents_to_train:
            agent.run(self, agent.current_observation, agent.current_reward, agent.done, agent.id)
        self.agents_to_train = []

        data = self.step(self.actions_to_send)
        self.actions_to_send = []
        return data

    def set_action_to_send(self, agent_id, action):
        self.actions_to_send.append([agent_id, action])

    def _get_data(self):
        try:
            data = self.udp_connection.recv(1024)
            if len(data) != 0:
                data_decoded = binaryapi.deserialize(data)
                return data_decoded

        except socket.timeout as e:
            print("Connection timed out: ", e)
        return None

    def _get_tcp_message(self):
        try:
            data = self.tcp_connection.recv(1024)
            print("Received data:", data)
            if len(data) != 0:
                data_decoded = binaryapi.deserialize(data)
                return data_decoded

        except socket.timeout as e:
            print("Connection timed out: ", e)
        return None

    def send_action(self, action):
        data = binaryapi.serialize(action)
        self.udp_connection.sendto(data, ('127.0.0.1', 7071))

    def process_data(self):
        message = self._get_data()
        if message is not None:
            return message

    def step(self, action):
        self.send_action(action)
        data = self.process_data()
        self.save_data_to_agents(data)
        return data

    def reset(self):
        self.begin_episode()
        data = self.process_data()
        self.save_data_to_agents(data)
        return data

    def freeze_game(self):
        self._send_tcp_message("freeze")

    def unfreeze_game(self):
        self._send_tcp_message("unfreeze")

    def begin_episode(self):
        self._send_tcp_message("reset")

    def _send_tcp_message(self, message):
        message_encoded = binaryapi.serialize(message)
        self.tcp_connection.send(message_encoded)

    def get_agent_by_id(self, agent_id):
        for agent in self.agents:
            if agent.id == agent_id:
                return agent
        return None

    def get_agents_by_type(self, agent_type):
        agents = []
        for agent in self.agents:
            if agent.agent_type == agent_type:
                agents.append(agent)
        return agents

    def save_data_to_agents(self, data):
        for agent_data in data:
            a_id = agent_data[0]
            a_type = agent_data[1]
            a_team = agent_data[2]
            a_observation_vector = agent_data[3]
            a_reward = agent_data[4]
            a_done = agent_data[5]

            agent = self.get_agent_by_id(a_id)
            agent.set_observation(a_observation_vector)
            agent.set_reward(a_reward)
            agent.set_done(a_done)

            self.agents_to_train.append(agent)

    def register_agent_func_by_type(self, agent_type, agent_func):
        for agent in self.agents:
            if agent.agent_type == agent_type:
                agent.register_agent_func(agent_func)

    def register_agent_func_by_id(self, agent_id, agent_func):
        agent = self.get_agent_by_id(agent_id)
        agent.register_agent_func(agent_func)

    def register_agent_func_for_all(self, agent_func):
        for agent in self.agents:
            agent.register_agent_func(agent_func)

    def close(self):
        pass
