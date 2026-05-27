"""
Script originally from Koteukin (https://github.com/Koteukin69/minescript/blob/main/rotation.py). I use the modified version of MrPrope (https://discord.com/channels/930220988472389713/1418561537945370664/1418963953324658710).
All credits belongs to them, I didn't contributed anything to this script, just using it.

Note: I adjusted the rotation speed, using other values may break the script.
"""
from minescript import player_orientation, player_set_orientation, player_position
from time import perf_counter
from math import sqrt, degrees, atan2, pi, sin, pow
import sys


MIN_ROTATION_SPEED = 0.8
MAX_ROTATION_SPEED = 1.4


MIN_ANGLE_THRESHOLD = 10.0
MAX_ANGLE_THRESHOLD = 150.0

MAX_CURVE_INTENSITY = 1.5


def easeOutCubic(t: float):
    return 1 - pow(1 - t, 3)


def humanized_rotate_releative(x: float, y: float, speed: float, curve_intensity: float, func=easeOutCubic):
    o = player_orientation()
    start_time = perf_counter()

    angular_distance = sqrt(x**2 + y**2)
    time_needed = 0 if speed == 0 else angular_distance / (speed * 180)
    t = 0

    while t < 1:
        t = (perf_counter() - start_time) / time_needed if time_needed > 0 else 1
        if t > 1:
            t = 1

        eased_t = func(t)
        current_yaw = o[0] + x * eased_t
        base_pitch = o[1] + y * eased_t

        pitch_offset = curve_intensity * sin(pi * t)
        player_set_orientation(current_yaw, base_pitch - pitch_offset)

    player_set_orientation(o[0] + x, o[1] + y)


def humanized_look_at_block(x: int, y: int, z: int):
    p = player_position()

    target_pos = (x + 0.5, y + 0.5, z + 0.5)
    dx, dy, dz = target_pos[0] - p[0], target_pos[1] - p[1], target_pos[2] - p[2]

    target_yaw = -degrees(atan2(dx, dz))
    target_pitch = -degrees(atan2((dy - 1.6), sqrt(dx**2 + dz**2)))

    o = player_orientation()
    delta_yaw = (target_yaw - o[0] + 180) % 360 - 180
    delta_pitch = target_pitch - o[1]

    angular_distance = sqrt(delta_yaw**2 + delta_pitch**2)

    dynamic_speed = MIN_ROTATION_SPEED
    dynamic_curve = 0.0

    if angular_distance > MIN_ANGLE_THRESHOLD:
        if angular_distance >= MAX_ANGLE_THRESHOLD:
            dynamic_speed = MAX_ROTATION_SPEED
            dynamic_curve = MAX_CURVE_INTENSITY
        else:
            ratio = (angular_distance - MIN_ANGLE_THRESHOLD) / (MAX_ANGLE_THRESHOLD - MIN_ANGLE_THRESHOLD)
            dynamic_speed = MIN_ROTATION_SPEED + (MAX_ROTATION_SPEED - MIN_ROTATION_SPEED) * ratio
            dynamic_curve = MAX_CURVE_INTENSITY * ratio

    humanized_rotate_releative(delta_yaw, delta_pitch, dynamic_speed, dynamic_curve, func=easeOutCubic)


if __name__ == "__main__":
    humanized_look_at_block(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
