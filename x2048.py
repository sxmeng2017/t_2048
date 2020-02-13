import random
import math

actions = ['Left', 'Right', 'Up', 'Down']
class game():

    def __init__(self, height=4, width=4):
        self.height = height
        self.width = width
        self.win_value = 2048
        self.score = 0
        self.reset()
        self.move('')


    def reset(self):
        """
        初始化棋盘布局
        布局为有两个随机生成的2，其余全为0
        :return:
        """
        self.field = [[0 for i in range(self.width)] for j in range(self.height)]
        self.fill2(self.field)
        self.fill2(self.field)

    def fill2(self, field):
        """
        在棋盘的空白位置随机找到一个，放入2.如果没有空位则返回false。
        :return:
        """
        count = 0
        candidate = []
        for i in range(self.height):
            for j in range(self.width):
                if self.field[i][j] == 0:
                    count += 1
                    candidate.append((i, j))
        if count == 0:
            return False
        else:
            des = random.randint(0, count - 1)
            x, y = candidate[des][0], candidate[des][1]
            field[x][y] = 2

    def _move_row_left(self, row):
        return self._tighten(self._merge(self._tighten(row)))

    def _tighten(self, row):
        new_row = [i for i in row if i > 0]
        new_row += [0 for i in range(self.width - len(new_row))]

        return new_row

    def _merge(self, row):
        new_row = []
        pair = False
        for i in range(len(row)):
            if pair:
                new_row.append(row[i] * 2)
                pair = False
            else:
                if i + 1 < len(row) and row[i] == row[i + 1]:
                    pair = True
                    new_row.append(0)
                else:
                    new_row.append(row[i])
        return new_row

    def _transpose(self, field):
        new_row = [list(r) for r in zip(*field)]
        return new_row

    def _invert(self, field):
        new_row = [r[::-1] for r in field]
        return new_row

    def move(self, direction):
        moves = {}
        moves['Left'] = lambda field: [self._move_row_left(row) for row in field]
        moves['Right'] = lambda field: self._invert(moves['Left'](self._invert(field)))
        moves['Up'] = lambda field: self._transpose(moves['Left'](self._transpose(field)))
        moves['Down'] = lambda field: self._transpose(moves['Right'](self._transpose(field)))
        self.moves = moves

        if direction in moves:
            if self.is_move_possible(direction):
                self.field = moves[direction](self.field)
                self.fill2(self.field)
                return True
            else:
                return False

    def is_move_possible(self, direction):
        check = {}
        check['Left'] = lambda field: any(self.is_left_movable(r) for r in field)
        check['Right'] = lambda field: check['Left'](self._invert(field))
        check['Up'] = lambda field: check['Left'](self._transpose(field))
        check['Down'] = lambda field: check['Right'](self._transpose(field))

        if direction in check:
            return check[direction](self.field)
        else:
            return False

    def is_left_movable(self, row):
        def change(i):
            if row[i] == 0 and row[i+1] != 0:
                return True
            if row[i] !=0 and row[i+1] == row[i]:
                return True
            return False
        return any(change(i) for i in range(len(row) - 1))

    def is_win(self):
        return any(any(i >= self.win_value for i in row) for row in self.field)

    def is_gameover(self):
        return not any(self.is_move_possible(move) for move in actions)

    def get_score(self):
        score = 0
        for row in self.field:
            for c in row:
                score += 0 if c < 4 else c * int((math.log(c, 2) - 1.0))
        return score



#****************************游戏流程控制****************************************
from tkinter import *
from tkinter import messagebox


class Screen:

    game_bg_color = "#bbada0"  # 设置背景颜色

    mapcolor = {
        0: ("#cdc1b4", "#776e65"),
        2: ("#eee4da", "#776e65"),
        4: ("#ede0c8", "#f9f6f2"),
        8: ("#f2b179", "#f9f6f2"),
        16: ("#f59563", "#f9f6f2"),
        32: ("#f67c5f", "#f9f6f2"),
        64: ("#f65e3b", "#f9f6f2"),
        128: ("#edcf72", "#f9f6f2"),
        256: ("#edcc61", "#f9f6f2"),
        512: ("#e4c02a", "#f9f6f2"),
        1024: ("#e2ba13", "#f9f6f2"),
        2048: ("#ecc400", "#f9f6f2"),
        4096: ("#ae84a8", "#f9f6f2"),
        8192: ("#b06ca8", "#f9f6f2"),
        # ----其它颜色都与8192相同---------
        2 ** 14: ("#b06ca8", "#f9f6f2"),
        2 ** 15: ("#b06ca8", "#f9f6f2"),
        2 ** 16: ("#b06ca8", "#f9f6f2"),
        2 ** 17: ("#b06ca8", "#f9f6f2"),
        2 ** 18: ("#b06ca8", "#f9f6f2"),
        2 ** 19: ("#b06ca8", "#f9f6f2"),
        2 ** 20: ("#b06ca8", "#f9f6f2"),
    }

    def __init__(self, g=game(4, 4), title='2048游戏'):
        self.g = g
        self.root = Tk()
        self.root.title(title)
        self.root.resizable(width=False, height=False)
        self.draw_frame()
        self.draw_labels_map()
        self.draw_score_label()

    def draw_frame(self):
        self.frame = Frame(self.root, bg=self.game_bg_color)
        self.frame.grid(sticky=N + E + W + E)
        self.frame.focus_set()

    def draw_labels_map(self):
        map_labels = []
        for i in range(self.g.height):
            row = []
            for j in range(self.g.width):
                value = self.g.field[i][j]
                text = str(value)
                label = Label(self.frame, text=text, width=4, height=2,
                              font=("黑体", 30, "bold"))
                label.grid(row=i, column=j, padx=5, pady=5, sticky=N + E + W + E)
                row.append(label)
            map_labels.append(row)
        self.map_labels = map_labels

    def draw_score_label(self):
        label = Label(self.frame, text='分数', font=("黑体", 30, "bold"),
                      bg="#bbada0", fg="#eee4da")
        label.grid(row=4, column=0, padx=5, pady=5)
        label_score = Label(self.frame, text='0', font=("黑体", 30, "bold"),
                            bg="#bbada0", fg="#ffffff")
        label_score.grid(row=4, columnspan=2, column=1, padx=5, pady=5)
        self.label_score = label_score

    def draw_restart(self):
        self.restart_button = Button(self.frame, text='重新开始', font=("黑体", 16, "bold"),
                                bg="#8f7a66", fg="#f9f6f2", command=self.reset_game)
        self.restart_button.grid(row=4, column=3, padx=5, pady=5)

    def run(self):
        self.frame.bind("<Key>", self.on_key_down)

        self.update_ui()  # 更新界面
        self.root.mainloop()  # 进入tkinter主事件循环

    def reset_game(self):
        self.g.reset()
        self.update_ui()

    def on_key_down(self, event):
        keysym = event.keysym
        if keysym in actions:
            self.g.move(keysym)
        self.update_ui()
        if self.g.is_gameover():
            mb = messagebox.askyesno(
                title="gameover", message='游戏结束，是否退出游戏'
            )
            if mb:
                self.root.quit()
            else:
                self.g.reset()
                self.update_ui()

    def update_ui(self):
        for i in range(self.g.height):
            for j in range(self.g.width):
                number = self.g.field[i][j]
                label = self.map_labels[i][j]
                label['text'] = str(number)
                label['bg'] = self.mapcolor[number][0]
                label['foreground'] = self.mapcolor[number][1]
        self.label_score['text'] = str(self.g.get_score())

g = game(4,4)
s = Screen(g=g)
s.run()















