from minescript_plus import Trading, Screen

def process_trade(item_name: str):
    try:
        for index in range(0, 10):
            if str(Trading.get_result(index)).split()[-1] == item_name:
                Trading.trade_offer(index)
                return
            elif str(Trading.get_costA(index)).split()[-1] == item_name:
                Trading.trade_offer(index)
                return
            elif str(Trading.get_costB(index)).split()[-1] == item_name:
                Trading.trade_offer(index)
                return
    except:
        Screen.close_screen()
        print("Item index out of bounds.")
        return
