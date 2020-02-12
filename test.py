from x2048 import game

example = game(3, 4)

def test_reset(example):
    example.reset()
    print(example.field)

def test_tighten(row):
    print('原数组', row)
    n = example._tighten(row)
    print('压缩后', n)

def test_merge(row):
    print('原数组', row)
    n = example._merge(row)
    print('合并后', n)

def test_move_left(row):
    print('原数组', row)
    n = example._move_row_left(row)
    print('合并后', n)

def test_transpose(field):
    print('原数组', field)
    n = example._transpose(field)
    print('转置后', n)

def test_invert(field):
    print('原数组', field)
    n = example._invert(field)
    print('翻转后', n)

def test_move_right(field):
    print('原数组', field)
    n = example.moves['right'](field)
    print('右转后', n)

def test_move_up(field):
    print('原数组', field)
    n = example.moves['up'](field)
    print('上转后', n)

def test_move_down(field):
    print('原数组', field)
    n = example.moves['down'](field)
    print('下转后', n)

def t(field):
    n = example._transpose(field)
    print(n)

if __name__ == '__main__':
    test_reset(example)
    test_tighten([0, 2, 0, 2])
    test_merge([2, 2, 2, 0])
    test_move_left([2, 2, 2, 0])
    test_invert([[2, 2, 0, 0],
                 [2, 0, 0, 2],
                 [0, 0, 0, 0]])
    test_transpose([[2, 2, 0, 0],
                 [2, 0, 0, 2],
                 [0, 0, 0, 0]])
    test_move_down([[2, 2, 0, 0],
                 [2, 0, 0, 2],
                 [2, 2, 0, 0],
                [0, 2, 0, 0]])
    test_move_right([[2, 2, 0, 0],
                 [2, 0, 0, 2],
                 [0, 0, 0, 0],
                    [0, 2, 0, 0]])
    test_move_up([[2, 2, 0, 0],
                 [2, 0, 0, 2],
                 [2, 0, 2, 2],
                 [0, 2, 0, 0]])
