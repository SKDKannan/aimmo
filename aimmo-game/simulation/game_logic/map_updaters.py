from abc import ABCMeta, abstractmethod
from collections import namedtuple
import random
import math
from logging import getLogger
from simulation.pickups import ALL_PICKUPS

LOGGER = getLogger(__name__)

MapContext = namedtuple('MapContext', 'num_avatars')


class _MapUpdater:
    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self, world_map, context):
        raise NotImplementedError


class ScoreLocationUpdater(_MapUpdater):
    def update(self, world_map, context):
        for cell in world_map.score_cells():
            if random.random() < world_map.settings['SCORE_DESPAWN_CHANCE']:
                cell.generates_score = False

        new_num_score_locations = len(list(world_map.score_cells()))
        target_num_score_locations = int(math.ceil(
            context.num_avatars * world_map.settings['TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR']
        ))
        num_score_locations_to_add = target_num_score_locations - new_num_score_locations
        locations = world_map._spawn_location_finder.get_random_spawn_locations(num_score_locations_to_add)
        for cell in locations:
            cell.generates_score = True


class PickupUpdater(_MapUpdater):
    def update(self, world_map, context):
        target_num_pickups = int(math.ceil(
            context.num_avatars * world_map.settings['TARGET_NUM_PICKUPS_PER_AVATAR']
        ))
        LOGGER.debug('Aiming for %s new pickups', target_num_pickups)
        max_num_pickups_to_add = target_num_pickups - len(list(world_map.pickup_cells()))
        locations = world_map._spawn_location_finder.get_random_spawn_locations(max_num_pickups_to_add)
        for cell in locations:
            if random.random() < world_map.settings['PICKUP_SPAWN_CHANCE']:
                LOGGER.info('Adding new pickup at %s', cell)
                cell.pickup = random.choice(ALL_PICKUPS)(cell)
