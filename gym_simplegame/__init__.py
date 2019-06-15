import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='simplegame-v0',
    entry_point='gym_simplegame.envs:SimplegameEnv'
)
