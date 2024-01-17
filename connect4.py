import random
import sys
import time
import board_manager as brd


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
        board={},
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
        self.turn = Turns(player_count=self.num_players, isBot=self.isBot)

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

    def game_over(self, reason, data):
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
        print("\n", reasons[reason], "🔵>🟢||🔴>🟡")
        self.inProgress = False
        self.printLineBreak()
        return self.inProgress

        # if self.serialConnected:

    # 		self.ardu.close()
    # + i for i in range(8)]def #pcvpc(self):


class Turns:
    def __init__(self, player_count=2, isBot=False):
        self.colors = ["🔴", "🟡", "🔵", "🟢"]
        # self.colors = {-1:'⚫',1:'🔴',2:'🔵','🔴':'🟡','🔵':'🟢'}
        self.players = {}
        self.start = True
        self.number = 0
        self.isBot = isBot

        if player_count > 4:
            print(f"Max number of players is 4")
            player_count = 4
        self.numPlayers = player_count
        print(f"{player_count=}")
        for i in range(player_count):
            self.players[i] = self.colors[i]
        self.current_player = random.randint(0, player_count - 1)
        print("1st turn randomly selected and order is sequential")

    def whose(self):
        if self.number > 0:
            return self.current_player
        else:
            return f"No one has taken a turn yet"

    def next(self, board):
        self.number += 1
        if self.current_player + 1 > self.numPlayers - 1:
            self.current_player = 0
        else:
            self.current_player += 1
        print(
            f"\nMove Number: {self.number} Current Player: {self.current_player}|{self.colors[self.current_player]}"
        )
        # Get possible moves

        target = -1
        # print(f"{board=}")
        if not self.isBot:
            while not target in board.spaces:
                target = int(
                    input(
                        f"The following positions are available {board.spaces}. Please choose one. "
                    )
                )
        else:
            viable_choices = []
            for i in board.spaces:
                if type(i) == int:
                    viable_choices.append(i)
            print(f"{viable_choices=}")
            if len(viable_choices) > 0:
                target = random.choice(viable_choices)
            else:
                return 4, board
        ret = board.take_move(target, self.current_player, self.number)
        if ret[0] == 0:
            board.index = ret[1]
        ret = board.is_connect4(self.current_player, target)
        if ret[0] == 1:
            return 1, board, ret[1], ret[2]
        else:
            board.index = ret[1]
        return 0, board
        # print(f"Current move belongs to player {self.current_player}:{self.players[self.current_player]}")

    def printLineBreak(self, text="", dbl_space=False, prefix=False):
        filler = "="
        buffer = 100 - len(text)
        prefixStr = filler * 25
        if not prefix:
            prefixStr = ""
            buffer += 25

        dbl_space = "\n\n" if dbl_space else None
        print(f"{prefixStr}{text}{filler*buffer:}", end=dbl_space)

        self.printLineBreak(text="starting turn")

        msg = f"{self.lastTurn=}, {self.currentTurn=}, {self.nextTurn=}, {self.lastMove=}, {self.currentPlayer=}"
        self.printLineBreak(text=msg, dbl_space=False)

        msg = f"current player: {game.currentPlayer} desired move: {choice}"

        self.printLineBreak(text=msg, prefix=True)
        # print(f"lastTurn: {self.lastTurn} currentTurn: {self.currentTurn} nextTurn: {self.nextTurn}")
        self.lastTurn = self.currentTurn
        self.currentTurn = self.nextTurn
        # self.nextTurn = self.nextTurn + 1

        openSpaces = self.possible_moves(self.board)
        choiceAccepted = self.check_move(self.currentPlayer, choice)
        while choiceAccepted == False:
            if len(openSpaces) < 1:
                return False

            choiceAccepted = self.check_move(
                self.currentPlayer,
                int(
                    input("Integers 1-39 represent the spaces on the board. Choose one")
                ),
            )
        if choiceAccepted:
            self.currentMove = choice
        self.printLineBreak(text="Submitting Move", prefix=True)
        return self.take_move(self.currentPlayer, choice)

    def move(self, player, choice):

        self.board[choice]["color"] = self.currentPlayer
        self.board[choice]["occupied"] = True
        self.board[choice]["moveNumber"] = self.currentTurn
        self.printLineBreak(text="Move Taken", prefix=True)
        if self.serialConnected:
            self.output_to_serial(choice, player)
        return self.end_turn(self.currentPlayer, choice)

    def end(self, player, choice):
        if self.start:
            self.start = False

        isWinner = self.check_win(player, choice, self.board)
        if isWinner[0]:
            (f"{isWinner[0]=}, sequence: {isWinner[1]}, lastMove: {isWinner[2]}")
            jsd = self.draw_win(isWinner[1])
            draw_board(jsd)
            self.game_over(1, player)
            return True

        try:

            # draw_board(self.board)
            self.printLineBreak(text=f"This turn is over", dbl_space=True)
            # print(f"turnKey: {self.turnKey} lastTurn: {self.lastTurn} currentTurn: {self.currentTurn} mextTurn: {self.nextTurn} lastMove: {self.lastMove}")
            return True
        except:
            print("something failed in endTurn")
            return False


if __name__ == "__main__":
    game = Game()
    height = game.board.height
    width = game.board.width
    print(game.board.height, game.board.width)
    while game.turn.number <= width * height and game.inProgress == True:
        ret = game.turn.next(game.board)
        if ret[0] == 0:
            game.board = ret[1]
            game.board.draw()
        else:
            game.winner = game.turn.current_player
            game.inProgress = False
            print(f"line:226 {ret[2]=}")
            game.game_over(reason=ret[0], data=ret[1])
