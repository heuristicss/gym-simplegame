import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='simplegame-v0',
    entry_point='gym_simplegame.envs:SimpleGame',
    kwargs={'grid' : 2},
)

register(
    id='simplegame4-v0',
    entry_point='gym_simplegame.envs:SimpleGame',
    kwargs={'grid' : 4},
)

register(
    id='simplegame8-v0',
    entry_point='gym_simplegame.envs:SimpleGame',
    kwargs={'grid' : 8},
)
