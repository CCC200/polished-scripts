import os, sys

dir = sys.argv[1] + '/base_stats/' # polishedcrystal/data/pokemon
config = open('pokedex.ts', 'w')
config.write('export const Pokedex: {[k: string]: ModdedSpeciesData} = {\n')
for file in sorted(os.listdir(dir)):
    mon = file.replace('.asm', '')
    if mon.find('_plain') > -1:
        mon = mon.replace('_plain', '')
    elif mon.find('_galarian') > -1:
        mon = mon.replace('_galarian', 'galar')
    elif mon.find('_alolan') > -1:
        mon = mon.replace('_alolan', 'alola')
    elif mon.find('_hisuian') > -1:
        mon = mon.replace('_hisuian', 'hisui')
    elif mon.find('_paldean') > -1:
        mon = mon.replace('_paldean', 'paldea')
    if mon.find('_') > -1:
        mon = mon.replace('_', '')
    if mon.find('paldeafire') > -1:
        mon = mon.replace('paldeafire', 'paldeablaze')
    elif mon.find('paldeawater') > -1:
        mon = mon.replace('paldeawater', 'paldeaaqua')
    elif mon.find('tauros-paldea') > -1:
        mon = mon.replace('tauros-paldea', 'taurospaldeacombat')
    config.write("\t" + mon + ": {\n\t\tinherit: true,\n\t},\n")
config.write('};\n')
config.close()
