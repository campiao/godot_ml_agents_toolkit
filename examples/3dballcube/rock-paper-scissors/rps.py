from godot_ml_agents_toolkit.godotenv import GodotEnv
import random


def random_choice(env: GodotEnv, observation, reward, done, a_id):
    action = random.choice([0, 1, 2])
    print(f"Observation: {observation}, Action: {action}")
    env.set_action_to_send(a_id, action)


env = GodotEnv()
env.reset()
env.register_agent_func_for_all(random_choice)

for i in range(5):
    env.run()
