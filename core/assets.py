from core.common_names import *
from core.sprite import Sprite

face_root = "./assets/face/"
eye_dict = {
    "angry":"angry_eye.png",
    "dead":"dead_eyes.png",
    "fall":"fall_move_eyes.png",
    "jump":"jump_eyes.png",
    "love":"love_eyes.png",
    "silly":"silly_eyes.png",
    "rage":"super_angry_eyes.png",
}


mouth_dict = {
    "hoo_hoo":"hoo_hoo.png",
    "talk_0":"talk_0.png",
    "talk_1":"talk_1.png",
    "talk_2":"talk_2.png",
    "talk_3":"talk_3.png",
    "smirk_0":"smirk_0.png",
    "smirk_1":"smirk_1.png",
    "smile":"smile.png",
}


right_eye_sprite_dict = {key:Sprite(face_root+path) for key,path in eye_dict.items()}
right_mouth_sprite_dict = {key:Sprite(face_root + path) for key,path in mouth_dict.items()}

left_eye_sprite_dict = {key:sprite.copy()for key,sprite in right_eye_sprite_dict.items()}
left_mouth_sprite_dict = {key:sprite.copy()for key,sprite in right_mouth_sprite_dict.items()}