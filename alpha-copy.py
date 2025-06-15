import os, sys
from PIL import Image

sprite_dir = ''

def translate_img(mon, type):
    sprite = Image.open(f'{sprite_dir}/{type}/{mon}')
    sprite_shiny = Image.open(f'sprites/{type}-shiny/{mon}').convert('RGBA')
    # create canvas and paste
    partw, parth = sprite_shiny.size
    pastex = int(48 - (partw / 2))
    pastey = int(48 - (parth / 2))
    sprite_alpha = Image.new('RGBA', (96, 96), (255, 255, 255, 0))
    sprite_alpha.paste(sprite_shiny, (pastex, pastey))
    # iterate over pixels
    pixels = list(sprite.getdata())
    pixels_shiny = list(sprite_alpha.getdata())
    for i in range(len(pixels)):
        # copy transparent pixels
        if pixels[i][3] == 0 and pixels_shiny[i][3] != 0:
            pixels_shiny[i] = pixels[i]
    sprite_alpha.putdata(pixels_shiny)
    sprite_alpha.save(f'{sprite_dir}/{type}-shiny/{mon}')

sprite_dir = sys.argv[1]
if not os.path.isdir(sprite_dir + '/front-shiny'):
    os.mkdir(sprite_dir + '/front-shiny')
if not os.path.isdir(sprite_dir + '/back-shiny'):
    os.mkdir(sprite_dir + '/back-shiny')
for mon in os.listdir(sprite_dir + '/front'):
    translate_img(mon, 'front')
for mon in os.listdir(sprite_dir + '/back'):
    translate_img(mon, 'back')
