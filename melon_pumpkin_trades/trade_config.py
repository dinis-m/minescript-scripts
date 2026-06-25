from dataclasses import dataclass


BlockPos = tuple[int, int, int]
PathPos = tuple[int, int, int, bool]


@dataclass(frozen=True)
class TradeConfig:
    version: str = "1.4.4"

    max_trades: int = 12
    villager_count: int = 63
    villager_type: str = "Farmer"

    trade_items: tuple[str, str] = (
        "minecraft:pumpkin",
        "minecraft:melon",
    )

    emerald_block: str = "minecraft:emerald_block"

    teleport_command: str = "/home farmers"

    base_pos: BlockPos = (-2176, 49, 1059)

    storage_path_pos: PathPos = (-2181, 50, 1064, True)
    storage_valid_positions: tuple[BlockPos, ...] = (
        (-2181, 50, 1064),
        (-2180, 50, 1064),
    )

    pumpkin_chest: BlockPos = (-2182, 49, 1065)
    melon_chest: BlockPos = (-2182, 49, 1066)

    craft_path_pos: PathPos = (-2174, 50, 1064, True)
    craft_wait_pos: BlockPos = (-2173, 50, 1064)
    craft_block: BlockPos = (-2173, 50, 1064)
    emerald_storage_chest: BlockPos = (-2173, 50, 1066)

    bed_path_pos: PathPos = (-2175, 50, 1067, True)
    bed_block: BlockPos = (-2176, 50, 1069)

    first_restock_start: int = 2100
    first_restock_end: int = 5999

    late_day_start: int = 6000
    late_day_end: int = 11999

    night_start: int = 12550
    night_end: int = 20000

    restock_wait_seconds: float = 7.5

    @property
    def target_per_item(self) -> int:
        return self.villager_count * self.max_trades

    @property
    def required_stacks(self) -> int:
        return (self.target_per_item + 63) // 64