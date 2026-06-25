from dataclasses import dataclass
from time import sleep

from minescript import echo, player_press_use, world_info

from rotation_1 import look_at_block

from melon_pumpkin_trades.trade_config import TradeConfig
from melon_pumpkin_trades.script_utils import start_exit_watcher
from melon_pumpkin_trades.stock_handler import ensure_trade_items
from melon_pumpkin_trades.villager_trader import trade_round
from melon_pumpkin_trades.movement import go_to_bed


@dataclass
class DayState:
    trades_today: int = 0
    warned: bool = False
    sleeping: bool = False
    depleted_announced: bool = False
    last_ticks: int = 0


def is_new_day(ticks: int, state: DayState) -> bool:
    return ticks < state.last_ticks


def reset_day_state(state: DayState) -> None:
    state.trades_today = 0
    state.warned = False
    state.sleeping = False
    state.depleted_announced = False


def run_trade_cycle(config: TradeConfig, state: DayState) -> None:
    ensure_trade_items(config)
    trade_round(config)

    state.trades_today += 1
    state.depleted_announced = False


def announce_depleted_once(state: DayState) -> None:
    if not state.depleted_announced:
        echo("§cTrades depleted for the day,\nwaiting for new day.")
        state.depleted_announced = True


def sleep_in_bed(config: TradeConfig, state: DayState) -> None:
    if state.sleeping:
        return

    go_to_bed(config)

    look_at_block(*config.bed_block)

    player_press_use(True)
    sleep(0.2)
    player_press_use(False)

    state.sleeping = True


def in_first_restock_window(config: TradeConfig) -> bool:
    ticks = world_info().day_ticks
    return config.first_restock_start <= ticks <= config.first_restock_end


def main() -> None:
    config = TradeConfig()
    state = DayState(last_ticks=world_info().day_ticks)

    echo(f"Melon and Pumpkin Auto Trade Script v{config.version}")

    start_exit_watcher()

    while True:
        sleep(0.1)

        ticks = world_info().day_ticks

        if is_new_day(ticks, state):
            reset_day_state(state)

        state.last_ticks = ticks

        if config.first_restock_start <= ticks <= config.first_restock_end:
            state.warned = False
            state.sleeping = False

            while state.trades_today < 2 and in_first_restock_window(config):
                run_trade_cycle(config, state)

                if state.trades_today < 2 and in_first_restock_window(config):
                    echo("Giving enough time for all\nvillagers to restock.")
                    sleep(config.restock_wait_seconds)

            if state.trades_today >= 2:
                announce_depleted_once(state)

        elif config.late_day_start <= ticks <= config.late_day_end:
            state.warned = False
            state.sleeping = False

            if state.trades_today < 1:
                run_trade_cycle(config, state)

            announce_depleted_once(state)

        elif config.night_start <= ticks <= config.night_end:
            state.warned = False

            if state.trades_today < 1:
                run_trade_cycle(config, state)

            sleep_in_bed(config, state)

        else:
            if not state.warned:
                echo("§aWaiting for daytime")
                state.warned = True


main()