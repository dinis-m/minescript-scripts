"""
Modified version of No's script (https://github.com/n-aoH/minescript-projects/blob/main/astar_pathing.py) for pathfinding in minecraft using minescript.

Current state:
- Fixed bugs like for jumping and diagonal movement
- Some small performance improvements (using precalculated offset directions + itertools)
- Added some typehinting to make life easier
- Walking works with smooth rotation + nearly always walking and sprinting. However its not the best implementation and can be improved (see my comment in the discord post (https://discord.com/channels/930220988472389713/1420155321434898562/1422565926368186398))
"""

import sys
import math
from heapq import heappop, heappush
import time
from typing import Optional, TypeAlias, TypeVar, Generic, List, Union
from itertools import product

import minescript
from minescript import echo
from rotation import humanized_look_at_block

minescript.set_default_executor(minescript.script_loop)

T = TypeVar("T")
BlockPos: TypeAlias = tuple[int, int, int]
WorldData: TypeAlias = dict[BlockPos, str]


IMPASSABLE_BLOCKS = {"minecraft:water", "minecraft:lava", "minecraft:cactus", "minecraft:fire", "minecraft:wither_rose"}
PASSABLE_BLOCKS = {
    "minecraft:air",
    "minecraft:torch",
    "minecraft:sugar_cane",
    "minecraft:rail",
    "minecraft:detector_rail",
    "minecraft:activator_rail",
    "minecraft:powered_rail",
    "minecraft:short_dry_grass",
    "minecraft:tall_dry_grass",
    "minecraft:tall_grass",
    "minecraft:short_grass",
    "minecraft:snow",
    "minecraft:soul_torch",
    "minecraft:redstone_wire",
    "minecraft:redstone_torch",
    "minecraft:redstone_wall_torch",
    "minecraft:repeater",
    "minecraft:comparator",
    "minecraft:flower_pot",
    "minecraft:rose_bush",
    "minecraft:poppy",
    "minecraft:allium",
    "minecraft:azalea_bush",
    "minecraft:azure_bluet",
    "minecraft:blue_orchid",
    "minecraft:brown_mushroom",
    "minecraft:closed_eyeblossom",
    "minecraft:cornflower",
    "minecraft:crimson_fungus",
    "minecraft:crimson_roots",
    "minecraft:dandelion",
    "minecraft:fern",
    "minecraft:dead_bush",
    "minecraft:lily_of_the_valley",
    "minecraft:open_eyeblossom",
    "minecraft:orange_tulip",
    "minecraft:oxeye_daisy",
    "minecraft:pink_tulip",
    "minecraft:red_mushroom",
    "minecraft:red_tulip",
    "minecraft:torchflower",
    "minecraft:warped_fungus",
    "minecraft:warped_roots",
    "minecraft:white_tulip",
    "minecraft:acacia_pressure_plate",
    "minecraft:bamboo_pressure_plate",
    "minecraft:birch_pressure_plate",
    "minecraft:cherry_pressire_plate",
    "minecraft:crimson_pressure_plate",
    "minecraft:dark_oak_pressure_plate",
    "minecraft:heavy_weighted_pressure_plate",
    "minecraft:jungle_pressure_plate",
    "minecraft:light_weighted_pressure_plate",
    "minecraft:mangrove_pressure_plate",
    "minecraft:oak_pressure_plate",
    "minecraft:pale_oak_pressure_plate",
    "minecraft:polished_blackstone_pressure_plate",
    "minecraft:spruce_pressure_plate",
    "minecraft:stone_pressure_plate",
    "minecraft:stone_pressure_plate",
    "minecraft:warped_pressure_plate",
}

NEIGHBOR_OFFSETS = tuple(p for p in product((-1, 0, 1), repeat=3) if any(p))

TICK_DURATION = 0.05  # seconds

LOOKAHEAD_TRESHOLD = 0.9

debug = False


def decho(msg: str):
    """Echo only if debug is enabled."""
    if debug:
        echo(msg)


def _distance(a: BlockPos, b: BlockPos) -> float:
    # euclidean distance for 3D space
    return math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2])


class Node(Generic[T]):
    def __init__(
        self,
        position: BlockPos,
        parent: Optional["Node"] = None,
        heuristic_cost: float = 0,
    ):
        self.parent = parent
        self.position = position
        self.cost = 0  # cost from start to current node (g-cost)
        self.heuristic_cost = heuristic_cost  # estimated cost from current node to end node (h-cost)
        self.total_cost = 0  # total cost (f-cost): f = g + h

    def __eq__(self, other: "Node"):
        return self.position == other.position

    def __lt__(self, other: "Node"):
        return self.total_cost < other.total_cost

    def __hash__(self):
        return hash(self.position)


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self.heapq: List[Node[T]] = []

    def push(self, node: Node[T]) -> None:
        heappush(self.heapq, node)

    def pop(self) -> Node[T]:
        return heappop(self.heapq)

    def __bool__(self) -> bool:
        return bool(self.heapq)


def _is_walkable(origin: BlockPos, to: BlockPos, world_data: WorldData, offset: BlockPos) -> bool:
    """
    Checks if a position is "walkable" for a 2-block-high entity.
    """
    jump = offset[1] > 0
    diagonal = all((offset[0], offset[2]))

    to_head_position = (to[0], to[1] + 1, to[2])
    to_feet_position = to
    to_ground_position = (to[0], to[1] - 1, to[2])

    to_safe_standing = (
        "air" in world_data.get(to_head_position, "air")
        and "air" in world_data.get(to_feet_position, "air")
        and "air" not in world_data.get(to_ground_position, "air")
        and not any(imp in world_data.get(to_ground_position, "air") for imp in IMPASSABLE_BLOCKS)
    )

    if not to_safe_standing:
        return False

    if jump:
        # check if blocked by a block when jumping
        origin_above = (origin[0], origin[1] + 2, origin[2])
        if "air" not in world_data.get(origin_above, "air"):
            return False

    # check if diagonal movement is blocked by corner blocks
    if diagonal and jump:
        # when jumping diagonally, check both corner blocks at head and one level above
        corner1 = (origin[0] + offset[0], origin[1] + 1, origin[2])
        corner2 = (origin[0], origin[1] + 1, origin[2] + offset[2])
        corner3 = (origin[0] + offset[0], origin[1] + 2, origin[2])
        corner4 = (origin[0], origin[1] + 2, origin[2] + offset[2])
        return all("air" in world_data.get(corner, "air") for corner in (corner1, corner2, corner3, corner4))
    elif diagonal and not jump:
        # when moving diagonally on the same level, check both corner blocks at feet and head level
        corner1 = (origin[0] + offset[0], origin[1], origin[2])
        corner2 = (origin[0], origin[1], origin[2] + offset[2])
        corner3 = (origin[0] + offset[0], origin[1] + 1, origin[2])
        corner4 = (origin[0], origin[1] + 1, origin[2] + offset[2])
        return all("air" in world_data.get(corner, "air") for corner in (corner1, corner2, corner3, corner4))

    return True


def find_path(start_pos: BlockPos, end_pos: BlockPos, world_data: WorldData) -> list[BlockPos]:
    start_node = Node(tuple(map(int, start_pos)), None, _distance(start_pos, end_pos))
    end_node = Node(tuple(map(int, end_pos)), None)

    frontier = PriorityQueue()
    frontier.push(start_node)
    explored, open_dict = set(), {}
    open_dict[start_node.position] = start_node

    while frontier:
        current_node = frontier.pop()
        open_dict.pop(current_node.position, None)
        if current_node.position in explored:
            continue
        explored.add(current_node.position)

        # If goal reached -> reconstruct path
        if current_node == end_node:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        (x, y, z) = current_node.position
        for dx, dy, dz in NEIGHBOR_OFFSETS:
            neighbor_pos = (x + dx, y + dy, z + dz)
            if neighbor_pos in explored or not _is_walkable((x, y, z), neighbor_pos, world_data, (dx, dy, dz)):
                continue

            move_cost = current_node.cost + math.sqrt(dx**2 + dy**2 + dz**2) + (0.5 if dy > 0 else 0)
            if neighbor_pos in open_dict and open_dict[neighbor_pos].cost <= move_cost:
                continue

            neighbor_node = Node(neighbor_pos, current_node)
            neighbor_node.cost = move_cost
            neighbor_node.heuristic_cost = _distance(neighbor_pos, end_node.position)
            neighbor_node.total_cost = neighbor_node.cost + neighbor_node.heuristic_cost

            frontier.push(neighbor_node)
            open_dict[neighbor_pos] = neighbor_node

    return []


def get_path(end_pos: BlockPos, scan_margin: int = 10) -> Union[List[BlockPos], int]:
    decho("§a[A* Pathfinder] Starting pathfinding...")

    START_POS: BlockPos = tuple(map(math.floor, minescript.player_position()))
    END_POS = end_pos

    decho("§e[A* Pathfinder] Preparing list of coordinates to scan...")

    min_x = min(START_POS[0], END_POS[0]) - scan_margin
    max_x = max(START_POS[0], END_POS[0]) + scan_margin
    min_y = min(START_POS[1], END_POS[1]) - scan_margin
    max_y = max(START_POS[1], END_POS[1]) + scan_margin
    min_z = min(START_POS[2], END_POS[2]) - scan_margin
    max_z = max(START_POS[2], END_POS[2]) + scan_margin

    positions_to_scan = [
        list(p)
        for p in product(
            range(min_x, max_x + 1),
            range(min_y, max_y + 1),
            range(min_z, max_z + 1),
        )
    ]

    decho(f"§e[A* Pathfinder] Scanning {len(positions_to_scan)} blocks...")
    block_names_list = minescript.getblocklist(positions_to_scan)

    # fmt: off
    world_data: WorldData = {
        BlockPos(pos): name
        for pos, name in zip(positions_to_scan, block_names_list)
        if name not in PASSABLE_BLOCKS
    }
    # fmt: on

    decho("§a[A* Pathfinder] Checking if destination is reachable...")
    if not _is_walkable(END_POS, END_POS, world_data, (0, 0, 0)):
        echo("§c[A* Pathfinder] Failure: Destination is not reachable (blocked or floating).")
        return -1

    decho("§e[A* Pathfinder] Calculating path...")
    return find_path(START_POS, END_POS, world_data)


def compress_path(path: List[BlockPos]) -> List[BlockPos]:
    """Compresses the path by only keeping turning points (direction vectors change)."""
    if len(path) < 3:
        return path

    compressed_path = [path[0]]
    prev_direction = (path[1][0] - path[0][0], path[1][1] - path[0][1], path[1][2] - path[0][2])

    for i in range(2, len(path)):
        current_direction = (path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1], path[i][2] - path[i - 1][2])
        if current_direction != prev_direction:
            compressed_path.append(path[i - 1])
            prev_direction = current_direction

    compressed_path.append(path[-1])
    return compressed_path


def mark_path(path: List[BlockPos], block_type: str = "minecraft:glowstone"):
    """Adds glowstone blocks to each node in the path for visualization."""
    for pos in path:
        cmd = f"setblock {pos[0]} {pos[1]} {pos[2]} {block_type}"
        minescript.execute(cmd)


def walk_path(path: List[BlockPos], sprint: bool):
    prev = path[0]
    idx = 1
    while idx < len(path):
        node = path[idx]
        next_node = path[idx + 1] if idx + 1 < len(path) else None

        # Align yaw roughly before moving
        while True:
            humanized_look_at_block(node[0], node[1] + 1, node[2])
            o = minescript.player_orientation()
            dx = node[0] + 0.5 - minescript.player_position()[0]
            dz = node[2] + 0.5 - minescript.player_position()[2]
            target_yaw = -math.degrees(math.atan2(dx, dz))
            delta_yaw = (target_yaw - o[0] + 180) % 360 - 180
            if abs(delta_yaw) < 40:
                break
            if abs(delta_yaw) > 90:
                minescript.player_press_forward(False)
                minescript.player_press_sprint(False)
                minescript.player_press_jump(False)
                decho("§e[A* Pathfinder] Warning: Large yaw adjustment needed. Stopping to re-align.")
                return False
            time.sleep(TICK_DURATION)

        decho(f"Walking to {node}...")
        minescript.player_press_forward(True)
        if sprint:
            minescript.player_press_sprint(True)

        want_jump = node[1] > prev[1]
        if want_jump:
            minescript.player_press_jump(True)

        prev_horiz_dist = float("inf")
        stagnation_ticks = 0

        while True:
            px, py, pz = minescript.player_position()
            dist_to_target = _distance((px, py, pz), (node[0] + 0.5, node[1], node[2] + 0.5))
            horiz_dist_to_current = math.hypot((node[0] + 0.5) - px, (node[2] + 0.5) - pz)

            # Overshoot detection: if we've passed the current node, advance immediately
            # -> Idea: check if if current distance to target increased and we were close enough
            if dist_to_target < 2.3 and horiz_dist_to_current > prev_horiz_dist:
                decho("§e[A* Pathfinder] Detected overshoot, advancing to next node.")
                break

            # Stuck detection based on horizontal distance trend
            if horiz_dist_to_current >= prev_horiz_dist:
                stagnation_ticks += 1
            else:
                stagnation_ticks = 0
            prev_horiz_dist = horiz_dist_to_current
            if stagnation_ticks > 15:
                echo("§c[A* Pathfinder] Warning: Stuck while walking the path. Stopping.")
                minescript.player_press_forward(False)
                minescript.player_press_sprint(False)
                minescript.player_press_jump(False)
                return False

            # Look-ahead orientation blending near current node
            if next_node is not None and horiz_dist_to_current <= LOOKAHEAD_TRESHOLD:
                humanized_look_at_block(next_node[0], next_node[1] + 1, next_node[2])

            if dist_to_target < 0.5:
                break
            time.sleep(TICK_DURATION / 10)

        minescript.player_press_jump(False)
        minescript.player_press_sprint(False)
        prev = node
        idx += 1

    minescript.player_press_forward(False)
    minescript.player_press_sprint(False)
    return True


def pathfind_to(x: int, y: int, z: int, sprint: bool):
    path = get_path((x, y, z), scan_margin=10)

    if path == -1:
        return

    if not path:
        echo("§c[A* Pathfinder] Failure: No path could be found.")
        echo("§e[A* Pathfinder] Retrying with an increased margin.")
        path = get_path((x, y, z), scan_margin=20)
        if not path:
            echo("§c[A* Pathfinder] Failure: No path could be found on retry. Exiting.")
            return

    echo(f"§a[A* Pathfinder] New path found! walking across {len(path)} points...")
    # echo(path)
    # mark_path(path)

    path = compress_path(path)
    decho(f"§a[A* Pathfinder] Compressed path to {len(path)} points.")
    # echo(path)
    # mark_path(path, block_type="minecraft:redstone_block")

    # Walk the path...
    if not walk_path(path, sprint):
        pathfind_to(x, y, z, sprint)
        return
    echo("§a[A* Pathfinder] Success: Reached destination!")


if __name__ == "__main__":
    pathfind_to(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), True)
