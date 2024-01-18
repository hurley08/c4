class Board:
    def __init__(self, h=5, w=8, index={}):
        self.colors = {-1: "⚫", 0: "🔴", 1: "🟡", 2: "🔵", 3: "🟢"}
        # self.colors = {-1:'⚫',1:'🔴',2:'🔵','🔴':'🟡','🔵':'🟢'}
        self.height = h
        self.width = w
        if len(index) < 1:
            boardIndex = {}
            for i in range(self.width * self.height):
                boardIndex.update({i: {"color": -1, "moveNumber": -1}})
        self.index = boardIndex
        # these define the relative positions of necessary pieces to connect lines
        self.diag1 = [
            -(w - 1) * 3,
            -(w - 1) * 2,
            -(w - 1),
            0,
            w - 1,
            (w - 1) * 2,
            (w - 1) * 3,
        ]
        self.diag2 = [
            -(w + 1) * 3,
            -(w + 1) * 2,
            -(w + 1),
            0,
            w + 1,
            (w + 1) * 2,
            (w + 1) * 3,
        ]
        self.vertical = [-3 * w, -2 * w, -w, 0, w, 2 * w, 3 * w]
        self.horizontal = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
        self.spaces = [(h * w) - w + i for i in range(w)]

    def draw(self):
        width = self.width
        height = self.height
        print("0\t| ", end="")
        print(self.index)
        for key in self.index.keys():
            piece = self.colors[self.index[key]["color"]]
            print(piece + " | ", end="")
            if int(key) != height * width and (int(key) + 1) % width == 0:
                print(f"\n{str(key+1)}\t| ", end="")

    def is_connect4(self, player, target):  # checks if move results in a connect 4
        target = int(target)
        print(f"{player=}, {target=}")
        self.printLineBreak(
            text=f"Checking if occupying {target} led to connect4", prefix=True
        )
        l = self.width
        h = self.height
        self.index

        sequence = []
        self.printLineBreak(text="Checking Diagonals", prefix=True)
        self.printLineBreak(text="checking diagonal 1")
        for i in self.diag1:
            if 0 <= i + target < (self.height * self.width) - 1:
                if self.index[target + i]["color"] == player:
                    print("verif", target + i, self.index[target + i])
                    sequence.append(i + target)
                else:
                    sequence = []
                if len(sequence) == 4:
                    if self.locate_col(sequence):
                        return 1, sequence, self.index

        self.printLineBreak(text="checking diagonal 1")
        sequence = []
        for i in self.diag2:
            if 0 <= i + target < (self.width * self.height):
                if self.index[target + i]["color"] == player:
                    sequence.append(i + target)
                if len(sequence) == 4:
                    sequence.reverse()
                    fa = self.locate_col(sequence)
                    if fa:
                        return 1, sequence, self.index
        sequence = []

        self.printLineBreak(text="Checking Laterals", prefix=True)
        sequence = []
        self.printLineBreak(text="checking vertical")
        print(self.vertical)
        for i in self.vertical:
            if 0 <= i + target < (self.height * self.width):
                if self.index[target + i]["color"] == player:
                    sequence.append(i + target)
                    if len(sequence) == 4:
                        print(f"CONNECT 4 {player=} {sequence=}")
                        return 1, sequence, self.index
                else:
                    sequence = []
        sequence = []
        self.printLineBreak(text="checking horizontal")
        for i in self.horizontal:
            if 0 <= target + i < self.width * self.height:
                if self.index[target + i]["color"] == player:
                    sequence.append(target + i)

                    if len(sequence) == 4:
                        print(sequence)
                        fa = self.check_spillover(sequence, direction="horizontal")
                        if fa:
                            return 1, sequence, self.index
                        else:
                            sequence = []
                    else:
                        sequence = []
                else:
                    sequence = []

        sequence = []
        # if (i*(i%self.width   ))<=i+target<(i+1)*(i%self.width   ):
        return 0, None, self.index

    def update_open_spaces(self):
        open_spaces = self.spaces
        for i in range(len(open_spaces)):
            if not open_spaces[i] == "-":
                if self.index[open_spaces[i]]["color"] > -1:
                    new_val = (
                        open_spaces[i] - self.width
                        if open_spaces[i] - self.width >= 0
                        else "-"
                    )
                    open_spaces[i] = new_val
                    # open_spaces.sort()
        self.spaces = open_spaces

    def take_move(self, target, player, turnNumber):
        self.index[int(target)] = {"color": player, "moveNumber": turnNumber}
        self.update_open_spaces()
        return 0, self.index

    def is_target_legal(self, player, desiredMove):

        #        if not self.lastMove:
        #            print("this is the first turn")
        if self.lastMove != None:
            if self.index[desiredMove]["occupied"] == True:
                print("the desired space is occuppied")
                return False
            if self.index[self.lastMove]["color"] == player:
                print("this player took the last turn ")
                return False
            if desiredMove not in possible_moves(self.index):
                print("the desired move is not currently accessible")
                return False
        return True

    def define_win_dim(self):
        l = self.width
        h = self.height
        self.diag1 = [
            -(w - 1) * 3,
            -(w - 1) * 2,
            -(w - 1),
            0,
            w - 1,
            (w - 1) * 2,
            (w - 1) * 3,
        ]
        self.diag2 = [
            -(w + 1) * 3,
            -(w + 1) * 2,
            -(w + 1),
            0,
            w + 1,
            (w + 1) * 2,
            (w + 1) * 3,
        ]
        self.vertical = [-3 * w, -2 * w, -l, 0, l, 2 * w, 3 * w]
        self.horizontal = [-4, -3, -2, -1, 0, 1, 2, 3, 4]

    def check_spillover(self, array, direction="vertical"):
        k = int(game.width / array[0])
        frame = [i for i in range(k * self.width, self.width * (k + 1))]
        frame2 = [
            i for i in range(16 * int(array[0] / 16), 16 * (int(array[0] / 16) + 1))
        ]
        print(f"{frame=}, {array=}")
        if direction == "vertical":
            for i in array:
                if i not in frame:
                    return False
            return True
        if direction == "horizontal":
            for i in array:
                if i not in frame2:
                    return False
            return True

    def locate_col(self, array):
        print(array)
        sequence = []
        for address in array:
            prel = (int(address / self.width) + 1) * self.width - address
            sequence.append(prel)
        result = sorted(sequence) == list(range(min(sequence), max(sequence) + 1))
        self.printLineBreak(dbl_space=True, text=f"{sequence:}")
        return result

    def printLineBreak(self, text="", dbl_space=False, prefix=False):
        filler = "="
        buffer = 100 - len(text)
        prefixStr = filler * 25
        if not prefix:
            prefixStr = ""
            buffer += 25

        dbl_space = "\n\n" if dbl_space else None
        print(f"{prefixStr}{text}{filler*buffer:}", end=dbl_space)
