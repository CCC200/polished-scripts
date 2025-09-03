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
    elif mon.find('taurospaldea') > -1:
        mon = mon.replace('taurospaldea', 'taurospaldeacombat')
    # hardcode mewtwo-armored data
    if mon == 'mewtwoarmored':
        config.write('\tmewtwoarmored: {\n\t\tnum: -2000,\n\t\tname: "Mewtwo-Armored",\n\t\tbaseSpecies: "Mewtwo",\n\t\tforme: "Armored",\n\t\theightm: 2.2,\n\t\tweightkg: 137,\n\t\tcolor: "Purple",\n\t\teggGroups: ["Undiscovered"],\n\t\ttags: ["Restricted Legendary"],\n')
    else:
        config.write("\t" + mon + ": {\n\t\tinherit: true,\n")
    # read stat data
    skip_line = False
    statfile = open(dir + file, 'r')
    for line in statfile:
        #skip 'faithful' data
        if skip_line:
            skip_line = False
            continue
        if line.find('if DEF(FAITHFUL)') > -1:
            skip_line = True
            continue
        # base stats
        if line.find('BST\n') > -1:
            line = line[:line.find(';')] # skip comment
            line = line[4:]
            bst = line.replace(' ', '').split(',')
            for i in range(len(bst)):
                bst[i] = str(int(bst[i])) # smooths out single digit stats
            buf = "\t\tbaseStats: {hp: [0], atk: [1], def: [2], spa: [4], spd: [5], spe: [3]},\n"
            buf = buf.replace('[0]', bst[0]).replace('[1]', bst[1]).replace('[2]', bst[2]).replace('[3]', bst[3]).replace('[4]', bst[4]).replace('[5]', bst[5])
            config.write(buf)
        # typing
        if line.find('; type') > -1:
            line = line[:line.find(';')] # skip comment
            line = line[4:]
            types = line.replace(' ', '').split(',')
            if types[0] == types[1]:
                types = [types[0]] # remove duplicate
            for i in range(len(types)):
                types[i] = types[i].capitalize()
            if len(types) == 2:
                buf = '\t\ttypes: ["[0]", "[1]"],\n'
                buf = buf.replace('[0]', types[0]).replace('[1]', types[1])
            else:
                buf = '\t\ttypes: ["[0]"],\n'
                buf = buf.replace('[0]', types[0])
            config.write(buf)
        # abilities
        if line.find('abilities_for') > -1:
            line = line[14:]
            abil = line.replace(' ', '').replace('_', ' ').replace('\n', '').split(',')
            abil.pop(0) # remove mon name
            # check if hidden ability is 2 or 3
            hidden_two = False
            if abil[0] == abil[1] and abil[1] != abil[2]:
                hidden_two = True
            # cleanup and insert
            abil = list(dict.fromkeys(abil)) # remove duplicates
            buf = '\t\tabilities: {'
            for i in range(len(abil)):
                abil[i] = abil[i].title()
                if i == 0:
                    buf += '0: "' + abil[i] + '"'
                elif i == 2 or hidden_two:
                    buf += ', H: "' + abil[i] + '"'
                elif i == 1:
                    buf += ', 1: "' + abil[i] + '"'
            buf += '},\n'
            config.write(buf)
    statfile.close()
    # hardcoded forme data
    buf = ''
    if mon == 'arbok':
        buf += '\t\tcosmeticFormes: ["Arbok-Kanto", "Arbok-Agatha", "Arbok-Ariana", "Arbok-Koga"],\n'
        buf += '\t\tformeOrder: ["Arbok", "Arbok-Kanto", "Arbok-Agatha", "Arbok-Ariana", "Arbok-Koga"],\n'
    elif mon == 'dudunsparce':
        buf += '\t\tcosmeticFormes: ["Dudunsparce-Three-Segment"],\n'
        buf += '\t\tformeOrder: ["Dudunsparce", "Dudunsparce-Three-Segment"],\n'
    elif mon == 'gyarados':
        buf += '\t\tcosmeticFormes: ["Gyarados-Red"],\n'
        buf += '\t\tformeOrder: ["Gyarados", "Gyarados-Red"],\n'
    elif mon == 'magikarp':
        buf += '\t\tcosmeticFormes: ["Magikarp-Bubbles", "Magikarp-Calico-One", "Magikarp-Calico-Two", "Magikarp-Calico-Three", "Magikarp-Dapples", "Magikarp-Diamonds", "Magikarp-Forehead-One", "Magikarp-Forehead-Two", "Magikarp-Mask-One", "Magikarp-Mask-Two", "Magikarp-Orca", "Magikarp-Patches", "Magikarp-Raindrop", "Magikarp-Saucy", "Magikarp-Skelly", "Magikarp-Stripe", "Magikarp-Tiger", "Magikarp-Two-Tone", "Magikarp-Zebra"],\n'
        buf += '\t\tformeOrder: ["Magikarp", "Magikarp-Bubbles", "Magikarp-Calico-One", "Magikarp-Calico-Two", "Magikarp-Calico-Three", "Magikarp-Dapples", "Magikarp-Diamonds", "Magikarp-Forehead-One", "Magikarp-Forehead-Two", "Magikarp-Mask-One", "Magikarp-Mask-Two", "Magikarp-Orca", "Magikarp-Patches", "Magikarp-Raindrop", "Magikarp-Saucy", "Magikarp-Skelly", "Magikarp-Stripe", "Magikarp-Tiger", "Magikarp-Two-Tone", "Magikarp-Zebra"],\n'
    elif mon == 'pichu':
        buf += '\t\tcosmeticFormes: ["Pichu-Spiky-eared"],\n'
        buf += '\t\tformeOrder: ["Pichu", "Pichu-Spiky-eared"],\n'
    elif mon == 'pikachu':
        buf += '\t\tcosmeticFormes: ["Pikachu-Chu-Chu", "Pikachu-Fly", "Pikachu-Pika", "Pikachu-Spark", "Pikachu-Surf"],\n'
        buf += '\t\tformeOrder: ["Pikachu", "Pikachu-Chu-Chu", "Pikachu-Fly", "Pikachu-Pika", "Pikachu-Spark", "Pikachu-Surf"],\n'
    elif mon == 'mewtwo':
        buf += '\t\totherFormes: ["Mewtwo-Armored"],\n'
        buf += '\t\tformeOrder: ["Mewtwo", "Mewtwo-Armored"],\n'
    if len(buf) > 0:
        config.write(buf)
    config.write("\t},\n")
# hardcoded cosmetic forme entries
formes = [
    'Arbok-Kanto', 'Arbok-Agatha', 'Arbok-Ariana', 'Arbok-Koga', 'Dudunsparce-Three-Segment', 'Gyarados-Red',
    'Magikarp-Bubbles', 'Magikarp-Calico-One', 'Magikarp-Calico-Two', 'Magikarp-Calico-Three', 'Magikarp-Dapples', 'Magikarp-Diamonds', 'Magikarp-Forehead-One', 'Magikarp-Forehead-Two', 'Magikarp-Mask-One', 'Magikarp-Mask-Two', 'Magikarp-Orca', 'Magikarp-Patches', 'Magikarp-Raindrop', 'Magikarp-Saucy', 'Magikarp-Skelly', 'Magikarp-Stripe', 'Magikarp-Tiger', 'Magikarp-Two-Tone', 'Magikarp-Zebra',
    'Pichu-Spiky-eared', 'Pikachu-Chu-Chu', 'Pikachu-Fly', 'Pikachu-Pika', 'Pikachu-Spark', 'Pikachu-Surf'
]
config.write('\t// COSMETIC FORMES\n\t// Handled in scripts.ts\n')
for f in formes:
    flat = f.replace('-', '').lower()
    config.write('\t' + flat + ': {\n\t\tname: "' + f + '",\n\t\tisCosmeticForme: true,\n\t},\n')
config.write('};\n')
config.close()
