import os, sys

move_name_array = []
move_data_array = []
egg_parent_array = []
egg_child_array = []
movelist = []

def insert_move(move, data, mon):
    if move == 'rocksmash':
        move = 'brickbreak'
    elif move == 'furystrikes':
        move = 'furyswipes'
    elif move == 'healinglight':
        move = 'moonlight'
    elif move == 'psychicm':
        move = 'psychic'
    elif move == 'freshsnack':
        if mon == 'miltank':
            move = 'milkdrink'
        else:
            move = 'softboiled'
    elif move == 'dazzlingleam':
        move = 'dazzlinggleam'
    elif move == 'disarmvoice':
        move = 'disarmingvoice'
    try:
        index = move_name_array.index(move)
        move_data_array[index] = move_data_array[index] + f', "{data}"'
    except:
        move_name_array.append(move)
        move_data_array.append(f'"{data}"')
        if move not in movelist:
            movelist.append(move)

def get_egg_index(mon):
    try:
        index = egg_parent_array.index(mon)
        return index
    except:
        return -1

dir = sys.argv[1] # polishedcrystal
dir_base = dir + '/data/pokemon/base_stats/'

# build egg groups
eggpointers = open(dir + '/data/pokemon/egg_move_pointers.asm', 'r')
for line in eggpointers:
    if line.find('NoEggSpeciesMoves') > -1 or line.find('Three Segment Form') > -1 or line.find('Red Form') > -1:
        continue
    if line.find('dw') > -1:
        # parse egg names
        egg_name = line[4:]
        egg_name = egg_name[:egg_name.find('EggSpeciesMoves')]
        egg_name = egg_name.strip()
        if egg_name.find('Plain') > -1:
            egg_name = egg_name[:egg_name.find('Plain')]
        elif egg_name.find('Alolan') > -1:
            egg_name = egg_name[:egg_name.find('Alolan')] + 'Alola'
        elif egg_name.find('Galarian') > -1:
            egg_name = egg_name[:egg_name.find('Galarian')] + 'Galar'
        elif egg_name.find('Hisuian') > -1:
            egg_name = egg_name[:egg_name.find('Hisuian')] + 'Hisui'
        elif egg_name.find('Paldean') > -1:
            egg_name = egg_name[:egg_name.find('Paldean')] + 'Paldea'
        egg_name = egg_name.lower()
        # parse mon names
        mon_name = line[line.find(';')+1:]
        mon_name = mon_name.strip()
        if mon_name.find('Alolan Form') > -1:
            mon_name = mon_name[:mon_name.find('(Alolan Form)')] + 'Alola'
        elif mon_name.find('Galarian Form') > -1:
            mon_name = mon_name[:mon_name.find('(Galarian Form)')] + 'Galar'
        elif mon_name.find('Hisuian Form') > -1:
            mon_name = mon_name[:mon_name.find('(Hisuian Form)')] + 'Hisui'
        elif mon_name.find('Paldean Form') > -1:
            mon_name = mon_name[:mon_name.find('(Paldean Form)')] + 'Paldea'
        elif mon_name.find('Bloodmoon Form') > -1:
            mon_name = mon_name[:mon_name.find('(Bloodmoon Form)')] + 'Bloodmoon'
        if mon_name.find(' ') > -1:
            mon_name = mon_name.replace(' ', '')
        mon_name = mon_name.lower()
        # build arrays
        if(mon_name != egg_name):
            egg_parent_array.append(mon_name)
            egg_child_array.append(egg_name)
eggpointers.close()

# build learnsets
config = open('learnsets.ts', 'w')
config.write('export const Learnsets: {[k: string]: ModdedLearnsetData} = {\n')
for file in sorted(os.listdir(dir_base)):
    move_name_array.clear()
    move_data_array.clear()
    mon = file.replace('.asm', '')
    if mon == 'egg':
        continue
    # separate name for levelup searching
    mon_evo_name = mon
    if mon_evo_name.find('_') > -1:
        mon_evo_name = mon_evo_name.replace('_', '')
    # name formatting
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
    if mon.find('taurospaldeafire') > -1:
        mon = mon.replace('taurospaldeafire', 'taurospaldeablaze')
    elif mon.find('taurospaldeawater') > -1:
        mon = mon.replace('taurospaldeawater', 'taurospaldeaaqua')
    elif mon.find('taurospaldea') > -1:
        mon = mon.replace('taurospaldea', 'taurospaldeacombat')
    config.write("\t" + mon + ": {\n\t\tlearnset: {\n")
    # read levelup moves
    search_table = False
    skip_line = False
    evosfile = open(dir + '/data/pokemon/evos_attacks.asm', 'r')
    for line in evosfile:
        # skip 'faithful' moves
        if skip_line:
            skip_line = False
            continue
        if line.find('if DEF(FAITHFUL)') > -1:
            skip_line = True
            continue
        # check if current mons' table
        line = line.lower()
        if line.find('evos_attacks ' + mon_evo_name) > -1:
            search_table = True
            continue
        if search_table and line.find('evos_attacks') > -1 or line.find('terminates') > -1:
            break
        # parse move
        if search_table and line.find('learnset') > -1:
            if line.find(';') > -1:
                line = line[:line.find(';')] # skip comments
            line = line[10:]
            evo_move = line.split(',')
            if evo_move[1].find('_') > -1:
                evo_move[1] = evo_move[1].replace('_', '')
            evo_move[1] = evo_move[1].strip()
            insert_move(evo_move[1], f'2L{evo_move[0]}', mon)
    evosfile.close()
    # read base stats for tm/hm
    basefile = open(dir_base + file, 'r')
    for line in basefile:
        if line.find('tmhm') > -1 and len(line) > 6:
            list = line[6:]
            list_data = list.split(',')
            for move in list_data:
                if move.find('_') > -1:
                    move = move.replace('_', '')
                move = move.lower()
                move = move.strip()
                insert_move(move, '2M', mon)
    basefile.close()
    # read egg moves
    search_table = False
    eggfile = open(dir + '/data/pokemon/egg_moves.asm')
    for line in eggfile:
        if line.find('EggSpeciesMoves') > -1:
            egg_name = line[:line.find('EggSpeciesMoves')]
            egg_name = egg_name.strip()
            if egg_name.find('Plain') > -1:
                egg_name = egg_name[:egg_name.find('Plain')]
            elif egg_name.find('Alolan') > -1:
                egg_name = egg_name[:egg_name.find('Alolan')] + 'Alola'
            elif egg_name.find('Galarian') > -1:
                egg_name = egg_name[:egg_name.find('Galarian')] + 'Galar'
            elif egg_name.find('Hisuian') > -1:
                egg_name = egg_name[:egg_name.find('Hisuian')] + 'Hisui'
            elif egg_name.find('Paldean') > -1:
                egg_name = egg_name[:egg_name.find('Paldean')] + 'Paldea'
            egg_name = egg_name.lower()
            egg_pointer = get_egg_index(mon)
            if mon == egg_name or egg_pointer > -1 and egg_name == egg_child_array[egg_pointer]:
                search_table = True
                continue
        if search_table and line.find('$ff') > -1:
            break
        if search_table and line.find('db') > -1:
            if line.find(';') > -1:
                line = line[:line.find(';')] # skip comments
            move = line[4:]
            move = move.replace('_', '')
            move = move.lower()
            move = move.strip()
            insert_move(move, '2E', mon)
    eggfile.close()
    # insert all moves
    for i in range(len(move_name_array)):
        config.write(f'\t\t\t{move_name_array[i]}: [{move_data_array[i]}],\n')
    config.write('\t\t},\n\t},\n')
config.write('};\n')
config.close()

movefile = open('moves.ts', 'w')
for move in movelist:
    movefile.write('\t' + move + ': {\n\t\tinherit: true,\n\t},\n')
movefile.close()
