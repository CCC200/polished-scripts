import os, sys
from PIL import Image

dir = ''
mons = []
crop = False
ps = False
mon_exceptions = ['unown', 'magikarp', 'arbok', 'pikachu', 'pichu', 'dudunsparce']

def get_psname(n):
    # forme parsing
    if '_plain' in n:
        n = n.replace('_plain', '')
    elif '_galarian' in n:
        n = n.replace('_galarian', '-galar')
    elif '_alolan' in n:
        n = n.replace('_alolan', '-alola')
    elif '_hisuian' in n:
        n = n.replace('_hisuian', '-hisui')
    elif '_paldean' in n:
        n = n.replace('_paldean', '-paldea')
    elif '_bloodmoon' in n:
        n = n.replace('_bloodmoon', '-bloodmoon')
    elif 'unown' in n:
        n = n.replace('_', '-')
    # remove underscore
    if '_' in n:
        n = n.replace('_', '')
    # hardcodes
    if n == 'arbokjohto':
        n = 'arbok'
    if n == 'tauros-paldea':
        n = 'tauros-paldeacombat'
    elif 'tauros-paldea' in n:
        n = n.replace('water', 'aqua').replace('fire', 'blaze')
    if n == 'dudunsparcetwosegment':
        n = 'dudunsparce'
    if n == 'dudunsparcethreesegment':
        n = 'dudunsparce-threesegment'
    return n

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
            # use standard palette for formes
            filepath_pal = dir + exception + f'/{pal}.pal'
    if mon == 'gyarados' or ps and mon == 'egg':
        # special cases, see below for gyara
        return
    elif mon.find('gyarados') > -1 and type == 'back':
        # hardcoded backsprite for red & normal gyarados
        filepath_sprite = dir + 'gyarados/back.png'
    elif mon == 'growlithe_hisuian' and type == 'back':
        # hardcoded bw swap for growlithe hisui
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
        sprite = Image.open(filepath_sprite)
        sprite = sprite.convert('P')
        sprite.putpalette(palette)
        if crop and 'front' in type:
            width, height = sprite.size
            sprite = sprite.crop((0, 0, width, height / (height / width)))
        sprite.save(f'sprites/{type}{'-shiny' if pal == 'shiny' else ''}/{get_psname(mon) if ps else mon}.png')
# main
if len(sys.argv) < 2:
	print('Point to polishedcrystal directory')
	sys.exit(1)
if '-crop' in sys.argv:
    # Crop frontsprites
    crop = True
if '-ps' in sys.argv:
    # Showdown name formatting
    ps = True
dir = sys.argv[1] + '/gfx/pokemon/'
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
