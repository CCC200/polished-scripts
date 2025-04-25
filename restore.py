import os, sys
from PIL import Image

dir = ''
mons = ''

def make_img():
    for mon in mons:
        filepath_pal = dir + mon + '/normal.pal'
        filepath_front = dir + mon + '/front.png'
        filepath_back = dir + mon + '/back.png'
        if not os.path.exists(filepath_pal):
            print(f'No palette for {mon}, skipping')
            continue
        # read palette data from normal.pal
        palette = [
            [0,0,0],
            [255,255,255]
        ]
        pal_file = open(dir + mon + '/normal.pal', 'r')
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
        # build sprites
        if os.path.exists(filepath_back):
            back = Image.open(filepath_back)
            back = back.convert('P')
            back.putpalette(palette)
            back.save(f'sprites/back/{mon}.png')
        if os.path.exists(filepath_front):
            front = Image.open(filepath_front)
            front = front.convert('P')
            front.putpalette(palette)
            front.save(f'sprites/front/{mon}.png')
# main
if len(sys.argv) < 2:
	print('Point to gfx/pokemon dir')
	sys.exit(1)
dir = sys.argv[1] + '/'
mons = next(os.walk(dir))[1]
if not os.path.isdir('sprites'):
    os.mkdir('sprites')
    os.mkdir('sprites/front')
    os.mkdir('sprites/back')
make_img()
