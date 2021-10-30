from module.campaign.campaign_base import CampaignBase
from module.map.map_base import CampaignMap
from module.map.map_grids import SelectedGrids, RoadGrids
from module.logger import logger

MAP = CampaignMap('13-1')
MAP.shape = 'H6'
MAP.camera_data = ['D2', 'D4', 'E2', 'E4']
MAP.camera_data_spawn_point = ['D4']
MAP.map_data = """
    ME -- ME Me ++ ++ ME MB
    ++ ME -- ME -- ++ ME --
    ++ __ Me ME -- -- Me --
    ME ME ++ ME ME -- __ --
    ME -- SP SP -- -- ++ --
    ME -- Me ME Me Me ++ MB
"""
MAP.weight_data = """
    50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50
"""
MAP.spawn_data = [
    {'battle': 0, 'enemy': 2},
    {'battle': 1, 'enemy': 2},
    {'battle': 2, 'enemy': 2},
    {'battle': 3, 'enemy': 1},
    {'battle': 4, 'enemy': 1},
    {'battle': 5},
    {'battle': 6, 'boss': 1},
]
A1, B1, C1, D1, E1, F1, G1, H1, \
A2, B2, C2, D2, E2, F2, G2, H2, \
A3, B3, C3, D3, E3, F3, G3, H3, \
A4, B4, C4, D4, E4, F4, G4, H4, \
A5, B5, C5, D5, E5, F5, G5, H5, \
A6, B6, C6, D6, E6, F6, G6, H6, \
    = MAP.flatten()


class Config:
    MAP_SWIPE_MULTIPLY = 1.519
    MAP_SWIPE_MULTIPLY_MINITOUCH = 1.469


class Campaign(CampaignBase):
    MAP = MAP

    def battle_0(self):
        if self.clear_filter_enemy('2L > 2M > 3L > 2E > 3E > 2C > 3C > 3M', preserve=1):
            return True

        return self.battle_default()

    def battle_5(self):
        if self.clear_filter_enemy('2L > 2M > 3L > 2E > 3E > 2C > 3C > 3M', preserve=0):
            return True

        return self.battle_default()

    def battle_6(self):
        return self.fleet_boss.clear_boss()
