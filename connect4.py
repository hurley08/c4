import random
import sys
import time
import board_manager as brd
import turn_mgr as tmgr


# board needs to be made into a subclass or separate class
class Game:
    def printLineBreak(self, text="", dbl_space=False, prefix=False):
        filler = "="
        buffer = 100 - len(text)
        prefixStr = filler * 25
        if not prefix:
            prefixStr = ""
            buffer += 25

        dbl_space = "\n\n" if dbl_space else None
        print(f"{prefixStr}{text}{filler*buffer:}", end=dbl_space)

    def __init__(
        self,
        waitTime=0.1,
        height=5,
        width=8,
        isBot=True,
        serial=False,
        debug=True,
    ):
        self.dummy = 5
        self.waitTime = waitTime
        self.isBot = isBot
        self.debug = debug
        self.inProgress = True
        self.winner = False
        print("done. commencing game")
        if serial:
            self.serial = serial_manager(
                baud=115200, port="dev/tty.usbmodem11101", sleep=10
            )
        self.board = brd.Board(height, width)
        self.num_players = 2  # input("How many players?")
        self.turn = tmgr.Turns(player_count=self.num_players, isBot=self.isBot)

    def init_log(self):
        moveLog = {}
        log = (i + 1 for i in range(len(self.board)))
        for i in log:
            moveLog[i] = False
        return moveLog

    def start_game():
        if self.serial:
            while self.serialConnected == False:
                self.init_serial()
            self.clear_board_serial()

    def draw_win(self, sequence, board={}):
        if not board:
            board = self.board
        for i in sequence:
            f = self.colors[board[i]["color"]]
            board[i]["color"] = f.upper()
        return board

    def game_over(self, reason, data1, data2):
        reasons = {
            4: {
                "no space for moves": "last_player's"
            },  # code:{reason for end:data field should include this inforamation
            1: {"Connect 4!": "player number"},
            2: {"Empty": True},
            -1: {"youNeedToModifyThis": "orDeleteThis"},
        }
        if reason in reasons.keys():
            if reason == 1:
                self.winner = data
        print(
            "\n",
            reasons[reason],
        )
        self.inProgress = False
        self.printLineBreak()
        return self.inProgress

        # if self.serialConnected:

    # 		self.ardu.close()
    # + i for i in range(8)]def #pcvpc(self):


if __name__ == "__main__":
    game = Game(height=5, width=8)
    brd_obj = game.board
    height = brd_obj.height
    width = brd_obj.width
    while game.turn.number <= width * height and game.inProgress == True:
        ret = game.turn.next(brd_obj)
        brd_obj = brd.Board(w=ret[1].width, h=ret[1].height, index=ret[1].index)
        print(f"{ret=}")
        if ret[0] == 0:
            brd_obj = ret[1]
            print(game.board.index)
            brd_obj.draw()
        else:
            game.winner = game.turn.current_player
            game.inProgress = False
            print(f"line:226 {ret[2]=}")
            game.game_over(reason=ret[0], data=ret[1])
