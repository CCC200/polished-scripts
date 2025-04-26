import os, sys
from PIL import Image

dir = ''
mons = []
mon_exceptions = ['unown', 'magikarp', 'arbok', 'pikachu', 'pichu', 'dudunsparce']

def make_img(mon, type, pal):
    filepath_pal = dir + mon + f'/{pal}.pal'
    filepath_sprite = dir + mon + f'/{type}.png'
    palette = [
        [0,0,0],
        [255,255,255]
    ]
    # exception handling
    for exception in mon_exceptions:
        if mon.find(exception) > -1:
            filepath_pal = dir + exception + f'/{pal}.pal'
    if mon == 'gyarados': # hardcoded for red & normal gyarados forms
        return
    elif mon.find('gyarados') > -1 and type == 'back':
        filepath_sprite = dir + 'gyarados/back.png'
    elif mon == 'ninetales_alolan' or mon == 'vulpix_alolan':
        if type == 'back':
            # hardcoded bw swap for vulpix alola line
            palette = [
                [255,255,255],
                [0,0,0],
            ]
    if not os.path.exists(filepath_pal):
        print(f'No {pal} palette for {mon}, skipping')
        return
    # read palette data from normal.pal
    pal_file = open(filepath_pal, 'r')
    content = pal_file.read()
    pal_file.close()
    for line in content.split('\n'):
        line = line.split(';')[0].lstrip()
        if line.startswith('RGB'):
            rgbs = [int(c, 10) * 8 for c in line[3:].split(',')]
            assert not len(rgbs) % 3
            while rgbs:
                rgb, rgbs = tuple(rgbs[:3]), rgbs[3:]
                rgb_val = []
                for x in rgb:
                    rgb_val.append(x)
                palette.insert(1, rgb_val)
    palette = [value for color in palette for value in color]
    # build sprite
    if os.path.exists(filepath_sprite):
        back = Image.open(filepath_sprite)
        back = back.convert('P')
        back.putpalette(palette)
        back.save(f'sprites/{type}{'-shiny' if pal == 'shiny' else ''}/{mon}.png')
# main
if len(sys.argv) < 2:
	print('Point to gfx/pokemon dir')
	sys.exit(1)
dir = sys.argv[1] + '/'
mons = next(os.walk(dir))[1]
if not os.path.isdir('sprites'):
    os.mkdir('sprites')
    os.mkdir('sprites/front')
    os.mkdir('sprites/front-shiny')
    os.mkdir('sprites/back')
    os.mkdir('sprites/back-shiny')
for mon in mons:
    make_img(mon, 'front', 'normal')
    make_img(mon, 'front', 'shiny')
    make_img(mon, 'back', 'normal')
    make_img(mon, 'back', 'shiny')
