import pygame
import sys
import pygame.transform as pt
import random
from pygame.time import get_ticks

FPS = 60
WINDOWSWIDTH = 960  # 窗口大小
WINDOWSHEIGHT = 840
FONTTYPE = 'Courier New'

pygame.init()
screen_size = (WINDOWSWIDTH, WINDOWSHEIGHT)  # 宽  高
screen = pygame.display.set_mode(screen_size)
FPSCLOCK = pygame.time.Clock()
pygame.display.set_caption("minesweeper")  # 标题

red = (255, 0, 0)
grey = (190, 190, 190)
white = (255, 255, 255)
blue = (0, 0, 255)
background_color = white  # 背景颜色
text_color = blue  # 文字颜色

MINESNUMBER = 50  # 雷个数
MINESWIDTH = 30  # 格子横向个数
MINESHEIGHT = 16  # 格子纵向个数

ori_size = 16  # 每个格子图片原本大小
cell_size = 30  # 每个正方形格子的大小
scale_fator = cell_size / ori_size  # 缩放程度
closed_img = pt.smoothscale(pygame.image.load('./images/closed.png'), (cell_size, cell_size))
flag_img = pt.smoothscale(pygame.image.load('./images/flag.png'), (cell_size, cell_size))
mine_img = pt.smoothscale(pygame.image.load('./images/mine.png'), (cell_size, cell_size))
mines_red_img = pt.smoothscale(pygame.image.load('./images/mine_red.png'), (cell_size, cell_size))
mines_wrong_img = pt.smoothscale(pygame.image.load('./images/mine_wrong.png'), (cell_size, cell_size))
type0_img = pt.smoothscale(pygame.image.load('./images/type0.png'), (cell_size, cell_size))
type1_img = pt.smoothscale(pygame.image.load('./images/type1.png'), (cell_size, cell_size))
type2_img = pt.smoothscale(pygame.image.load('./images/type2.png'), (cell_size, cell_size))
type3_img = pt.smoothscale(pygame.image.load('./images/type3.png'), (cell_size, cell_size))
type4_img = pt.smoothscale(pygame.image.load('./images/type4.png'), (cell_size, cell_size))
type5_img = pt.smoothscale(pygame.image.load('./images/type5.png'), (cell_size, cell_size))
type6_img = pt.smoothscale(pygame.image.load('./images/type6.png'), (cell_size, cell_size))
type7_img = pt.smoothscale(pygame.image.load('./images/type7.png'), (cell_size, cell_size))
type8_img = pt.smoothscale(pygame.image.load('./images/type8.png'), (cell_size, cell_size))
face_active_img = pt.smoothscale(pygame.image.load('./images/face_active.png'), (cell_size, cell_size))
face_lose_img = pt.smoothscale(pygame.image.load('./images/face_lose.png'), (cell_size, cell_size))
face_win_img = pt.smoothscale(pygame.image.load('./images/face_win.png'), (cell_size, cell_size))
nums_bg_img = pt.smoothscale_by(pygame.image.load('./images/nums_background.png'), (scale_fator, scale_fator))
d0_img = pt.smoothscale_by(pygame.image.load('./images/d0.png'), (scale_fator, scale_fator))
d1_img = pt.smoothscale_by(pygame.image.load('./images/d1.png'), (scale_fator, scale_fator))
d2_img = pt.smoothscale_by(pygame.image.load('./images/d2.png'), (scale_fator, scale_fator))
d3_img = pt.smoothscale_by(pygame.image.load('./images/d3.png'), (scale_fator, scale_fator))
d4_img = pt.smoothscale_by(pygame.image.load('./images/d4.png'), (scale_fator, scale_fator))
d5_img = pt.smoothscale_by(pygame.image.load('./images/d5.png'), (scale_fator, scale_fator))
d6_img = pt.smoothscale_by(pygame.image.load('./images/d6.png'), (scale_fator, scale_fator))
d7_img = pt.smoothscale_by(pygame.image.load('./images/d7.png'), (scale_fator, scale_fator))
d8_img = pt.smoothscale_by(pygame.image.load('./images/d8.png'), (scale_fator, scale_fator))
d9_img = pt.smoothscale_by(pygame.image.load('./images/d9.png'), (scale_fator, scale_fator))
# 调用图片

nums_bg_height = 25 * scale_fator  # 数字框高度
d_width = 11 * scale_fator  # 数字宽度

start_x = WINDOWSWIDTH // 2 - MINESWIDTH // 2 * cell_size  # 左上格子的左上角横坐标
start_y = 100

face_x = WINDOWSWIDTH // 2  # 笑脸的横坐标
face_y = 50
face_rect = pygame.Rect(face_x, face_y, cell_size, cell_size)

gameEnd = False  # 记录游戏是否结束
firstClick = True  # 记录是否有过点击格子，没有时为True
succeeded = False  # 游戏胜利
failed = False  # 游戏失败
starttime = 0  # 游戏开始时间


def main():
    global gameEnd, firstClick
    mines, zerolist, revealed, marked = createMine()  # 置雷
    # mines 记录是否为雷及周围雷数量    二维矩阵
    # zerolist 记录被揭开的周围雷数量为0的格子的[x,y]  列表
    # revealed 记录格子是否被揭开  二维矩阵
    # marked 记录被标记的格子[x,y] 列表

    mouse_x = 0  # 记录鼠标位置
    mouse_y = 0

    while True:

        MouseLeftClicked = False  # 记录左键是否点击
        MouseRightClicked = False  # 记录右键是否点击

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                left, mid, right = mouse_presses
                if left:
                    MouseLeftClicked = True
                    mouse_x, mouse_y = event.pos
                elif right:
                    MouseRightClicked = True
                    mouse_x, mouse_y = event.pos

        if MouseLeftClicked:
            ResponseForMouseLeft(mouse_x, mouse_y, mines, zerolist, revealed, marked)  # 响应鼠标左键点击

        if MouseRightClicked:
            ResponseForMouseRight(revealed, marked, mouse_x, mouse_y)  # 响应鼠标右键点击

        if not gameEnd:  # 游戏未结束时，更新画面
            screen.fill(background_color)
            screen.blit(face_active_img, (face_x, face_y))  # 画脸
            draw_closed(revealed)  # 画未揭开格子
            draw_revealed(mines, revealed)  # 已揭开格子
            draw_marked(marked)  # 被标记格子
            draw_minesnum(marked)  # 左上角剩余雷总数
            draw_starttime()  # 右上角游戏开始时间

        if not gameEnd:
            checkWinGame(mines, revealed)  # 判断游戏是否结束
        if gameEnd:
            drawGameEnd()  # 游戏结束时更新画面
        if MouseLeftClicked:
            if face_rect.collidepoint(mouse_x, mouse_y):  # 如果点击脸，重启游戏
                mines, zerolist, revealed, marked = reset()

        FPSCLOCK.tick(FPS)  # 锁帧
        pygame.display.update()


def calAround(rect):
    # 计算周围雷数量
    dx = [0, 1, 1, 1, 0, -1, -1, -1]
    dy = [1, 1, 0, -1, -1, -1, 0, 1]
    for x in range(MINESWIDTH):
        for y in range(MINESHEIGHT):
            if rect[x][y] != '[x]':
                minesnum = 0
                for step in range(8):
                    nx = dx[step] + x
                    ny = dy[step] + y
                    if nx < 0 or nx >= MINESWIDTH or ny < 0 or ny >= MINESHEIGHT:
                        continue
                    if rect[nx][ny] == '[x]':
                        minesnum += 1
                rect[x][y] = '[%s]' % (minesnum)


def calCellPos(x, y):
    # 计算格子的实际位置  i为横坐标
    i = x * cell_size + start_x
    j = y * cell_size + start_y
    return i, j


def calMousePos(mx, my):
    # 计算此时鼠标点击到哪个格子，或是点击其他位置
    for x in range(MINESWIDTH):
        for y in range(MINESHEIGHT):
            i, j = calCellPos(x, y)
            tmpRect = pygame.Rect(i, j, cell_size, cell_size)
            if tmpRect.collidepoint(mx, my):
                return x, y

    return None, None  # 未点击格子


def checkWinGame(mines, revealed):
    # 判断游戏是否胜利，条件：所有非雷格子都被揭开
    flag = True
    for x in range(MINESWIDTH):
        for y in range(MINESHEIGHT):
            if mines[x][y] != '[x]':
                if not revealed[x][y]:
                    flag = False

    if flag:
        WinGame(mines)


def clickCell(mines, zerolist, revealed, marked, x, y):
    global firstClick, starttime
    # 对未揭开的格子进行点击操作
    tmp = firstClick
    if [x, y] in marked:
        marked.remove([x, y])
    if mines[x][y] == '[x]':
        # 若此格子为雷，则游戏结束
        if not firstClick:
            LoseGame(mines, marked, x, y)
        else:
            while mines[x][y] == '[x]':
                mines, zerolist, revealed, marked = reset()
            RevealCell(mines, zerolist, revealed, marked, x, y)
            firstClick = False
    else:
        # 否则揭开格子
        RevealCell(mines, zerolist, revealed, marked, x, y)
        firstClick = False

    if tmp and not firstClick:
        starttime = get_ticks()


def createMine():
    # 初始化并放雷
    mines = randomPlaceMine()
    calAround(mines)

    zerolist = []
    revealed = initRevealed()
    marked = []
    return mines, zerolist, revealed, marked


def draw_closed(revealed):
    # 画未揭开且未被标记的格子
    for x in range(MINESWIDTH):
        for y in range(MINESHEIGHT):
            if not revealed[x][y]:
                i, j = calCellPos(x, y)
                screen.blit(closed_img, (i, j))


def drawGameEnd():
    # 画下方语句
    global succeeded, failed
    tipFont = pygame.font.SysFont(FONTTYPE, 16)
    tail = 'You can press the face above to restart the game.'
    if succeeded:
        text = 'Congratulations on your win!'
    else:
        text = 'You lose.'
    drawText(text + tail, tipFont, text_color,
             WINDOWSWIDTH / 2, WINDOWSHEIGHT - 60)


def draw_marked(marked):
    # 画被标记的格子
    for x, y in marked:
        i, j = calCellPos(x, y)
        screen.blit(flag_img, (i, j))


def draw_minesnum(marked):
    # 画剩余雷数量
    left = MINESNUMBER - len(marked)
    if left < 0:
        left = 0
    d100 = left // 100
    d10 = (left // 10) % 10
    d1 = left % 10
    pos_x = start_x
    pos_y = start_y - 10 - nums_bg_height
    p1 = switch(d100)
    p2 = switch(d10)
    p3 = switch(d1)
    draw_num(p1, p2, p3, pos_x, pos_y)


def draw_num(p1, p2, p3, posx, posy):
    # 画数字框及其中数字
    screen.blit(nums_bg_img, (posx, posy))
    dis = 2 * scale_fator
    screen.blit(p1, (posx + dis, posy + dis))
    screen.blit(p2, (posx + dis + d_width, posy + dis))
    screen.blit(p3, (posx + dis + 2 * d_width, posy + dis))


def draw_revealed(mines, revealed):
    # 画已揭开的格子
    for x in range(MINESWIDTH):
        for y in range(MINESHEIGHT):
            if revealed[x][y]:
                i, j = calCellPos(x, y)
                num = int(mines[x][y][1])
                if num == 0:
                    screen.blit(type0_img, (i, j))
                if num == 1:
                    screen.blit(type1_img, (i, j))
                if num == 2:
                    screen.blit(type2_img, (i, j))
                if num == 3:
                    screen.blit(type3_img, (i, j))
                if num == 4:
                    screen.blit(type4_img, (i, j))
                if num == 5:
                    screen.blit(type5_img, (i, j))
                if num == 6:
                    screen.blit(type6_img, (i, j))
                if num == 7:
                    screen.blit(type7_img, (i, j))
                if num == 8:
                    screen.blit(type8_img, (i, j))


def draw_starttime():
    # 画游戏开始时间
    t = 0
    if not firstClick:
        now = get_ticks()
        t = now - starttime
        t = t // 1000
    if t > 999:
        t = 999
    t = int(t)
    d100 = t // 100
    d10 = (t // 10) % 10
    d1 = t % 10
    pos_x = start_x + cell_size * (MINESWIDTH - 3)
    pos_y = start_y - 10 - nums_bg_height
    p1 = switch(d100)
    p2 = switch(d10)
    p3 = switch(d1)
    draw_num(p1, p2, p3, pos_x, pos_y)


def drawText(text, font, color, x, y):
    # 画文本
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.centerx = x
    textrect.centery = y
    screen.blit(textobj, textrect)


def ForRevealedClicked(mines, zerolist, revealed, marked, x, y):
    # 若点击已揭开的格子,判断周围标记数是否正好等于周围雷数，若等于则将未标记且未揭开的格子打开
    dx = [0, 1, 1, 1, 0, -1, -1, -1]
    dy = [1, 1, 0, -1, -1, -1, 0, 1]
    count = 0
    num = int(mines[x][y][1])
    if num == 0:
        return
    for i in range(8):  # 统计数量
        nx = dx[i] + x
        ny = dy[i] + y
        if nx < 0 or nx >= MINESWIDTH or ny < 0 or ny >= MINESHEIGHT:
            continue
        if [nx, ny] in marked and not revealed[nx][ny]:
            count += 1
    if num == count:
        # 相等时
        for i in range(8):
            nx = dx[i] + x
            ny = dy[i] + y
            if nx < 0 or nx >= MINESWIDTH or ny < 0 or ny >= MINESHEIGHT:
                continue
            if [nx, ny] not in marked and not revealed[nx][ny]:
                clickCell(mines, zerolist, revealed, marked, nx, ny)


def initRevealed():
    # 创建二维矩阵，初值置为false，表示未揭开
    revealed = []
    for x in range(MINESWIDTH):
        revealed.append([False] * MINESHEIGHT)
    return revealed


def LoseGame(mines, marked, x, y):
    # 游戏失败时，保持画面不变，同时显示雷的位置
    global gameEnd, failed
    gameEnd = True
    failed = True
    screen.blit(face_lose_img, (face_x, face_y))
    showMines(mines, marked, x, y)


def randomPlaceMine():
    # 返回随机生成的二维矩阵,有雷则为'[x]'
    # 第一维为横坐标
    mines = []
    for i in range(MINESWIDTH):
        mines.append([])
        for j in range(MINESHEIGHT):
            mines[i].append('[ ]')
    step = 0
    while step < MINESNUMBER:
        x = step % MINESWIDTH
        y = step // MINESWIDTH
        mines[x][y] = '[x]'
        step += 1

    for i in range(MINESWIDTH * MINESHEIGHT - 1, -1, -1):
        nowx = i % MINESWIDTH
        nowy = i // MINESWIDTH
        number = random.randint(0, i)
        nx = number % MINESWIDTH
        ny = number // MINESWIDTH
        str = mines[nowx][nowy]
        mines[nowx][nowy] = mines[nx][ny]
        mines[nx][ny] = str

    return mines


def RevealCell(mines, zerolist, revealed, marked, x, y):
    # 揭开格子
    # 对非0格子，若周围有0格子，则将其揭开
    # 对0格子，揭开周围所有格子
    revealed[x][y] = True  # 揭开所在格子
    if [x, y] in marked:
        # 若之前被标记，则取消标记
        marked.remove([x, y])
    if mines[x][y] == '[0]' and [x, y] not in zerolist:
        # 为0的格子被揭开时
        zerolist.append([x, y])
        dx = [0, 1, 1, 1, 0, -1, -1, -1]
        dy = [1, 1, 0, -1, -1, -1, 0, 1]
        for i in range(8):  # 遍历周围格子
            nx = dx[i] + x
            ny = dy[i] + y
            if nx < 0 or nx >= MINESWIDTH or ny < 0 or ny >= MINESHEIGHT:
                continue
            if mines[nx][ny] != '[x]':
                RevealCell(mines, zerolist, revealed, marked, nx, ny)

    if mines[x][y] != '[x]':
        dx = [0, 1, 1, 1, 0, -1, -1, -1]
        dy = [1, 1, 0, -1, -1, -1, 0, 1]
        for i in range(8):  # 遍历周围格子
            nx = dx[i] + x
            ny = dy[i] + y
            if nx < 0 or nx >= MINESWIDTH or ny < 0 or ny >= MINESHEIGHT:
                continue
            if mines[nx][ny] == '[0]' and not revealed[nx][ny]:
                RevealCell(mines, zerolist, revealed, marked, nx, ny)


def ResponseForMouseLeft(mouse_x, mouse_y, mines, zerolist, revealed, marked):
    # 当鼠标左键点击时
    x, y = calMousePos(mouse_x, mouse_y)
    if (x, y) != (None, None):
        # 当点击到格子
        if not gameEnd:
            if revealed[x][y]:
                # 该格子已被揭开
                ForRevealedClicked(mines, zerolist, revealed, marked, x, y)
            else:
                # 该格子未被揭开
                clickCell(mines, zerolist, revealed, marked, x, y)


def ResponseForMouseRight(revealed, marked, mouse_x, mouse_y):
    # 当右键点击时，对未揭开的格子进行标记或取消标记
    x, y = calMousePos(mouse_x, mouse_y)
    if (x, y) != (None, None):
        if not revealed[x][y]:
            if [x, y] in marked:
                marked.remove([x, y])
            else:
                marked.append([x, y])


def reset():
    global gameEnd, firstClick, succeeded, failed
    mines, zerolist, revealed, marked = createMine()
    gameEnd = False
    firstClick = True
    succeeded = False
    failed = False
    return mines, zerolist, revealed, marked


def showMines(mines, marked, posx, posy):
    # 游戏失败时，显示雷位置
    for x in range(MINESWIDTH):
        for y in range(MINESHEIGHT):
            if mines[x][y] == '[x]':
                if (x, y) != (posx, posy):
                    i, j = calCellPos(x, y)
                    screen.blit(mine_img, (i, j))
                else:
                    i, j = calCellPos(x, y)
                    screen.blit(mines_red_img, (i, j))
            else:
                if (x, y) in marked:
                    i, j = calCellPos(x, y)
                    screen.blit(mines_wrong_img, (i, j))


def switch(num):
    # 将数字转为对应图片
    if num == 0:
        return d0_img
    if num == 1:
        return d1_img
    if num == 2:
        return d2_img
    if num == 3:
        return d3_img
    if num == 4:
        return d4_img
    if num == 5:
        return d5_img
    if num == 6:
        return d6_img
    if num == 7:
        return d7_img
    if num == 8:
        return d8_img
    if num == 9:
        return d9_img


def WinGame(mines):
    # 游戏胜利时将gameEnd,succeeded置为True,同时改变脸表情
    global gameEnd, succeeded
    gameEnd = True
    succeeded = True
    screen.blit(face_win_img, (face_x, face_y))
    print("succeed!")


if __name__ == '__main__':
    main()
