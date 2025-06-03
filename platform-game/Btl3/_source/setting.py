from enum import Enum

class SFXType:
    @staticmethod
    def COIN_COLLECT() : return 'coin collect'
    @staticmethod
    def ITEM_COLLECT() : return 'item collect'
    @staticmethod
    def ENEMY_DIE() : return 'enemy die'
    @staticmethod
    def RUN() : return 'run'
    @staticmethod
    def JUMP() : return 'jump'
    @staticmethod
    def SWORD() : return 'sword'
    @staticmethod
    def HIT() : return 'hit'
    @staticmethod
    def OVERWORLD_THEME() : return 'ot'
    @staticmethod
    def LEVEL_THEME() : return 'lt'
    @staticmethod
    def RAIN() : return 'rain'
    @staticmethod
    def TRANSFORMATION() : return 'tf'
    @staticmethod
    def BOSS_ATTACK01() : return 'ba1'
    @staticmethod
    def BOSS_ATTACK02() : return 'ba2'
    @staticmethod
    def BOSS_ATTACK03() : return 'ba3'
    @staticmethod
    def BOSS_PRE_ATTACK03() : return 'bpa3'
    @staticmethod
    def BOSS_AWAKE() : return 'ba'
    @staticmethod
    def BOSS_DIE() : return 'bd'
    @staticmethod
    def BOSS_THEME() : return 'bt'
    @staticmethod
    def ULTIMATE01() : return 'ulti1'
    @staticmethod
    def ULTIMATE02() : return 'ulti2'


class GameState:
    @staticmethod 
    def OVERWORLD() : return 'overworld'
    @staticmethod
    def LEVEL() : return 'level'

class PlayerType:
    @staticmethod
    def LIGHT(): return 0 
    @staticmethod
    def DARK() : return 1

class VFX_State:
    @staticmethod
    def LIGHT2DARK() : return 'FX_lighttodark'
    @staticmethod
    def DARK2LIGHT() : return 'FX_darktolight'

class State:
    @staticmethod
    def IDLE(): return 'idle'
    @staticmethod
    def RUN(): return 'run'
    @staticmethod
    def JUMP(): return 'jump'
    @staticmethod
    def FALL(): return 'fall'
    @staticmethod
    def ATTACK01(): return 'attack1'
    @staticmethod
    def ATTACK02(): return 'attack2'
    @staticmethod
    def ATTACK03(): return 'attack3'
    @staticmethod
    def TRANSFORM(): return 'transform'
    @staticmethod
    def AWAKE() : return 'awake'
    @staticmethod
    def LIE_STATIC() : return 'lying'
    @staticmethod
    def NOT_ATTACK() : return 'not_attack'
    @staticmethod
    def DIE() : return 'die'
vertical_tile_number = 11
tile_size = 64
tile_real_size = 16
background_png_size = (6400, 704)

screen_height = vertical_tile_number * tile_size
screen_width = 1280

thunderstorm_color = (255, 255, 255, 255)

GLOBAL_VOLUME = 1

TERRAIN_TILESET_PATH = '../_levels/png/BWForest/Tileset.png'
TREE_AND_STUFF_PATH = '../_levels/png/BWForest/Trees_and_etc.png'
BACK_PATH = '../_levels/level_data/back_tree.png'
FRONT_PATH = '../_levels/level_data/front_tree.png'
BACKGROUND_PATH = '../_levels/level_data/background_gold.png'
BACKGROUND_BOSS_PATH = '../_levels/level_data/bg_hanger_dude.png'
COIN_PATH = '../_levels/png/coin01.png'
ICON_PATH = '../_assets/icon.png'

HOME_SCREEN_PATH = '../_assets/Home/Homescene.png'
UNMUTE_PATH = '../_assets/UI/unmute.png'
MUTE_PATH =  '../_assets/UI/mute.png'


particle_scale = 2.5

particle_sizes_light2dark = (59, 88)
particle_sizes_dark2light = (71, 94)

particle_anim_speed_light2dark = 0.25
particle_anim_speed_dark2light = 0.25

particle_transform_sizes = {
    PlayerType.LIGHT() : particle_sizes_light2dark,
    PlayerType.DARK() : particle_sizes_dark2light
}
particle_anim_transform_speed = {
    PlayerType.LIGHT() : particle_anim_speed_light2dark,
    PlayerType.DARK() : particle_anim_speed_dark2light
}

boss_init_position = (-50, 160)

# facing = -1 : left, 1 : right
boss_attack_state = {
    'attack 1' : 
    [
        {
            'position' : (350, 400),
            'facing' : 1,
            'attack' : True,
            'time' : 3000
        },
        {
            'position' : (900, 400),
            'facing' : -1,
            'attack' : True,
            'time' : 3000
        },
        {
            'position' : (350, 400),
            'facing' : 1,
            'attack' : True,
            'time' : 3000
        }
    ],
    'attack 2' : 
    [
        {
            'position' : (900, 400),
            'facing' : -1,
            'attack' : True,
            'time' : 5000
        },
        {
            'position' : (350, 400),
            'facing' : 1,
            'attack' : True,
            'time' : 5000
        },
        {
            'position' : (900, 400),
            'facing' : -1,
            'attack' : True,
            'time' : 5000
        }
    ],
    'attack 3' : 
    [
        {
            'position' : (900, 400),
            'facing' : -1,
            'attack' : True,
            'time' : 10000
        },
        {
            'position' : (350, 400),
            'facing' : 1,
            'attack' : True,
            'time' : 10000
        },
        {
            'position' : (350, 400),
            'facing' : 1,
            'attack' : True,
            'time' : 10000
        }
    ],
    'attack 4' : 
    [
        {
            'position' : (625, 400),
            'facing' : -1,
            'attack' : True,
            'time' : 5000
        },
        {
            'position' : (625, 400),
            'facing' : 1,
            'attack' : True,
            'time' : 5000
        },
        {
            'position' : (625, 400),
            'facing' : 1,
            'attack' : True,
            'time' : 5000
        }
    ]
}

boss_pivot_top = (screen_width / 2, screen_height / 3)
boss_scale = 5
boss_anim_loop = {
    State.IDLE() : True,
    State.AWAKE() : False,
    State.RUN() : True,
    State.LIE_STATIC() : True,
    State.ATTACK01() : False,
    State.ATTACK02() : False,
    State.ATTACK03() : False,
    State.NOT_ATTACK() : False,
    State.DIE() : False
}
boss_sizes = {
    State.IDLE() : (201, 94),
    State.AWAKE() : (201, 94),
    State.RUN() : (201, 94),
    State.LIE_STATIC() : (201, 94),
    State.ATTACK01() : (201, 94),
    State.ATTACK02() : (201, 94),
    State.ATTACK03() : (201, 94),
    State.NOT_ATTACK() : (201, 94),
    State.DIE() : (201, 94)
}
boss_anim_speed = {
    State.IDLE() : 0.25,
    State.AWAKE() : 0.2,
    State.RUN() : 0.25,
    State.LIE_STATIC() : 0.25,
    State.ATTACK01() : 0.25,
    State.ATTACK02() : 0.25,
    State.ATTACK03() : 0.25,
    State.NOT_ATTACK() : 0.25,
    State.DIE() : 0.5
}

player_scale = 2.5
player_sizes_light = {
    State.IDLE() : (24, 24),
    State.RUN() : (24, 24),
    State.JUMP() : (24, 24),
    State.FALL() : (24, 24),
    State.ATTACK01() : (38, 22),
    State.ATTACK02() : (52, 24),
    State.ATTACK03() : (52, 24),
    State.TRANSFORM() : (23, 60)
}
player_anim_speed_light = {
    State.IDLE() : 0.15,
    State.RUN(): 0.3,
    State.JUMP() : 0.15,
    State.FALL() : 0.15,
    State.ATTACK01() : 0.3,
    State.ATTACK02() : 0.25,
    State.ATTACK03() : 0.25,
    State.TRANSFORM() : 0.25
}
player_sizes_dark = {
    State.IDLE() : (22, 18),
    State.RUN() : (26, 22),
    State.JUMP() : (21, 27),
    State.FALL() : (18, 37),
    State.ATTACK01() : (65, 27),
    State.ATTACK02() : (65, 27),
    State.ATTACK03() : (65, 27),
    State.TRANSFORM() : (26, 65)
}
player_anim_speed_dark = {
    State.IDLE() : 0.15,
    State.RUN(): 0.3,
    State.JUMP() : 0.15,
    State.FALL() : 0.15,
    State.ATTACK01() : 0.3,
    State.ATTACK02() : 0.25,
    State.ATTACK03() : 0.25,
    State.TRANSFORM() : 0.25
}
player_sizes = {
    PlayerType.LIGHT() : player_sizes_light,
    PlayerType.DARK() : player_sizes_dark
}
player_anim_speed = {
    PlayerType.LIGHT() : player_anim_speed_light,
    PlayerType.DARK() : player_anim_speed_dark
}

level_theme_light = {
    'tile' : 'grey',
    'background' : 'black'
}
level_theme_dark = {
    'tile' : 'black',
    'background' : 'grey'
}
level_theme = {
    PlayerType.LIGHT() : level_theme_light,
    PlayerType.DARK() : level_theme_dark
}