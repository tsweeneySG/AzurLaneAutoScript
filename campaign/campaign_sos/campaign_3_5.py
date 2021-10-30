from .campaign_base import CampaignBase
from module.map.map_base import CampaignMap
from module.map.map_grids import SelectedGrids, RoadGrids
from module.logger import logger

MAP = CampaignMap('SOS')
MAP.shape = 'H5'
MAP.camera_data = ['D3', 'E3']
MAP.camera_data_spawn_point = ['D3']
MAP.map_data = """
    -- -- ++ ++ -- Me -- --
    ++ Me ME ME ME MB ++ --
    -- ME SP SP __ Me ++ ME
    ME ++ ME ME ME Me ME ME
    -- ME Me ME ++ ME ME ++
"""
MAP.weight_data = """
    50 50 50 50 50 20 50 50
    50 50 30 20 10 10 50 50
    50 50 50 30 20 20 50 50
    50 50 30 30 30 30 50 50
    50 50 50 50 50 50 50 50
"""
MAP.spawn_data = [
    {'battle': 0, 'enemy': 2},
    {'battle': 1, 'enemy': 2},
    {'battle': 2, 'enemy': 2},
    {'battle': 3, 'enemy': 1, 'boss': 1},
]
A1, B1, C1, D1, E1, F1, G1, H1, \
A2, B2, C2, D2, E2, F2, G2, H2, \
A3, B3, C3, D3, E3, F3, G3, H3, \
A4, B4, C4, D4, E4, F4, G4, H4, \
A5, B5, C5, D5, E5, F5, G5, H5, \
    = MAP.flatten()


class Config:
    # ===== Start of generated config =====
    MAP_HAS_MAP_STORY = False
    MAP_HAS_FLEET_STEP = False
    MAP_HAS_AMBUSH = False
    STAR_REQUIRE_1 = 0
    STAR_REQUIRE_2 = 0
    STAR_REQUIRE_3 = 0
    # ===== End of generated config =====

    INTERNAL_LINES_HOUGHLINES_THRESHOLD = 40
    EDGE_LINES_HOUGHLINES_THRESHOLD = 40
    COINCIDENT_POINT_ENCOURAGE_DISTANCE = 1.5
    INTERNAL_LINES_FIND_PEAKS_PARAMETERS = {
        'height': (120, 255 - 40),
        'width': (1.5, 10),
        'prominence': 10,
        'distance': 35,
    }
    EDGE_LINES_FIND_PEAKS_PARAMETERS = {
        'height': (255 - 40, 255),
        'prominence': 10,
        'distance': 50,
        'wlen': 1000
    }


class Campaign(CampaignBase):
    MAP = MAP

    def battle_0(self):
        if self.clear_enemy(scale=(2, 3), genre=['light', 'carrier', 'enemy', 'main']):
            return True

        return self.battle_default()

    def battle_3(self):
        self.fleet_boss.clear_boss()
