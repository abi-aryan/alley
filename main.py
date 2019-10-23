import os
import time
import numpy as np

from envs_layer import ArenaEnvs
from agents_layer import ArenaAgent


def main():
    num_envs = 3
    ma_envs = ArenaEnvs(
        env_name='Arena-Test-Discrete',
        num_envs=num_envs,
        train_mode=False,
    )

    # single-agent-like sync step
    agents = [
        ArenaAgent(
            action_space=ma_envs.sa_envs[agent_i].action_space,
            observation_space=ma_envs.sa_envs[agent_i].observation_space,
            num_envs=num_envs,
            id=agent_i,
        ) for agent_i in range(ma_envs.number_agents)
    ]

    for agent_i in range(ma_envs.number_agents):
        ma_envs.sa_envs[agent_i].reset()

    for agent_i in range(ma_envs.number_agents):
        obs = ma_envs.sa_envs[agent_i].get_observe_after_reset()
        agents[agent_i].observe_after_reset(obs)

    k = 0
    while True:
        for agent_i in range(ma_envs.number_agents):
            actions = agents[agent_i].act()
            ma_envs.sa_envs[agent_i].step(actions)
        ma_envs.step_sync()
        for agent_i in range(ma_envs.number_agents):
            obs, reward, done, info = ma_envs.sa_envs[agent_i].get_observe_after_step(
            )
            agents[agent_i].observe_after_step(obs, reward, done, info)
        k += 1
        print('========{}========='.format(k))

    # # multi-agent step
    # obs = ma_envs.reset()
    # k = 0
    # while True:
    #     actions = np.random.randint(ma_envs.action_space.n, size=(
    #         ma_envs.num_envs, ma_envs.number_agents))
    #     print('act {}'.format(actions))
    #     obs, reward, done, info = ma_envs.step(actions)
    #     print('step {} {} {} {} {} {}'.format(
    #         type(obs), np.shape(obs),
    #         type(reward), np.shape(reward),
    #         type(done), np.shape(done),
    #     ))
    #     k += 1
    #     print('step at {}'.format(k))


if __name__ == '__main__':
    main()
