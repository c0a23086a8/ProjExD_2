import os
import random
import sys
import pygame as pg

WIDTH, HEIGHT = 1600, 900


DELTA = {  # 移動量辞書（押下キー：移動量タプル）
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: 
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg") 

    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk2_img = pg.transform.flip(kk_img, True, False)

    ALFA = {
        (-5, 0): kk_img, # 左
        (-5, -5): pg.transform.rotozoom(kk_img, 315, 1.0), # 左上
        (0, -5): pg.transform.rotozoom(kk2_img, 90, 1.0), # 上
        (+5, -5): pg.transform.rotozoom(kk2_img, 45, 1.0), # 右上
        (+5, 0): kk2_img, # 右
        (+5, +5): pg.transform.rotozoom(kk2_img, 315, 1.0), # 右下
        (0, +5): pg.transform.rotozoom(kk2_img, 270, 1.0), # 下
        (-5, +5): pg.transform.rotozoom(kk_img, 45, 1.0), # 左下
        (0, 0): kk_img # はじめ
    }
    """
    辞書ALFA
    飛ぶ方向に従って画像を切り替える
    key=移動量:value=表示する画像
    関数にする
    """

    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400

    enn=pg.Surface((20,20))
    pg.draw.circle(enn, (255,0,0),(10,10),10)
    enn_rct=enn.get_rect()
    enn_rct.center=random.randint(0,WIDTH), random.randint(0,HEIGHT)
    vx, vy=+5,+5
    enn.set_colorkey((0,0,0))

    clock = pg.time.Clock()
    tmr = 0

    accs = [a for a in range(1, 11)]
    """
    追加機能2
    加速度のリストを生成
    """


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(enn_rct):
            print("Game Over")
            return
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0]+=v[0]
                sum_mv[1]+=v[1]
            for i in ALFA.items():
                if (k,v):
                    kk_img = i

            """
            移動量に対して画像を決める
            """

        
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        kk_img = ALFA[tuple(sum_mv)]
        screen.blit(kk_img, kk_rct)
        enn_rct.move_ip(vx,vy)
        screen.blit(enn, enn_rct)
        yoko, tate = check_bound(enn_rct)
        if not yoko:  # 横方向にはみ出てたら
            vx *= -1
        if not tate:  # 縦方向にはみ出てたら
            vy *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
