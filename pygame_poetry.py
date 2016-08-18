import sys
import pygame
from random import *
from pygame.locals import *
import time
from tkinter import *
from techno_poet import gen_text
from tkinter.filedialog import askopenfilename, asksaveasfilename

source_text = ''
fill_text = ''
savefile = ''


def get_source():
    global source_text
    source_text = askopenfilename(title='Select a source text')
    return source_text


def get_fill():
    global fill_text
    fill_text = askopenfilename(title='Select a fill text')
    return fill_text


def get_savefile():
    global savefile
    savefile = asksaveasfilename(title='Save generated text as:')
    return savefile


def rand_colors(scrn):
    red = randint(0, 255)
    green = randint(0, 255)
    blue = randint(0, 255)
    scrn.fill((red, green, blue))


top = Tk()
top.title('Poetry Generator')
Label(top, text='Choose source and fill texts:', bg='gray60', fg='black', font=('arial', 16,)).pack(side=TOP)
top.geometry('400x200')
button1 = Button(top, text='Source Text', command=(lambda: get_source()))
button1.pack(fill=X)
button2 = Button(top, text='Fill Text', command=(lambda: get_fill()))
button2.pack(fill=X)
button3 = Button(top, text='Save As', command=(lambda: get_savefile()))
button3.pack(fill=X)


def run_game():
    global source_text, fill_text, savefile
    if source_text and fill_text and savefile:
        gen_text(source_text, fill_text, savefile)
    else:
        gen_text()
        savefile = '/users/jason/python/digital_poetry/logs/newlog.txt'
    pygame.init()

    scrn_wdth = 1200
    scrn_hght = 500
    speed = 0.5
    txt_centerx = 600
    # msx = 0
    # msy = 0
    font_size = 20
    screen = pygame.display.set_mode((scrn_wdth, scrn_hght), 0, 32)
    pygame.display.set_caption("Pygame Template")
    fontobj = pygame.font.Font('freesansbold.ttf', font_size)
    pygame.mixer.music.load('/users/jason/py_game/music/taof01.mid')
    pygame.mixer.music.play(-1, 0.0)
    num_lines = int(scrn_hght / (font_size + 5))
    count = 0
    while True:
        for line in open(savefile):
            lstart = ((font_size + 5) * (count % num_lines) + (int((font_size + 5) / 2)))
            if count % num_lines == 0:
                rand_colors(screen)
            textsurf = fontobj.render(line.rstrip(), True, (0, 0, 0))
            textrect = textsurf.get_rect()
            textrect.center = (txt_centerx, lstart)
            screen.blit(textsurf, textrect)
            time.sleep(speed)
            count += 1
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                    # elif event.type == MOUSEMOTION:
                    # msx, msy = event.pos
                    # elif event.type == MOUSEBUTTONDOWN:
                    # msx, msy = event.pos
                elif event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        if speed < 10:
                            speed += 0.1
                    elif event.key == K_UP:
                        if speed >= 0.1:
                            speed -= 0.1
                    elif event.key == K_SPACE:
                        rand_colors(screen)
                    elif event.key == K_LEFT:
                        if textrect.left > 0:
                            txt_centerx -= 20
                    elif event.key == K_RIGHT:
                        if textrect.right < scrn_wdth:
                            txt_centerx += 20
            pygame.display.update()


button3 = Button(top, text='Generate', command=(lambda: run_game()))
button3.pack()

top.mainloop()
