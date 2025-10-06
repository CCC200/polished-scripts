dexf = open('pokedex.ts')
dex = dexf.readlines()
dexf.close()
basef = open('pokedex-base.ts') # copy this from damage-calc
basedex = basef.read()
basef.close()
f = open('calc-patch.ts', 'w')
f.write('const POLISHED_PATCH: {[name: string]: DeepPartial<SpeciesData>} = {\n')
name = ''
bst_update = False
type_update = False
ability_update = False
written_first = False
written_name = False
for line in dex:
    if 'export const' in line:
        continue
    if ': {\n' in line:
        nameflat = line.split(':')[0].strip()
        if nameflat in basedex:
            name = basedex[basedex.find(nameflat+':'):]
            name = name[name.find('name:')+7:name.find('",')]
            if '-' in name or 'Farfetch' in name or '.' in name or ' ' in name:
                name = f"'{name}'"
            if written_first and written_name:
                f.write('  },\n')
            else:
                written_first = True
            written_name = False
    elif '// BST update' in line:
        bst_update = True
        continue
    elif '// Types update' in line:
        type_update = True
        continue
    elif '// Abilities update' in line:
        ability_update = True
        continue
    if bst_update or type_update or ability_update:
        if not written_name:
            f.write('  ' + name + ': {\n')
            written_name = True
    if bst_update:
        bst_update = False
        bst = line.strip()
        # bs: {hp: 90, at: 75, df: 75, sa: 115, sd: 90, sp: 55},
        # baseStats: {hp: 95, atk: 75, def: 90, spa: 125, spd: 95, spe: 65},
        bst = bst.replace('baseStats:', 'bs:').replace('atk:', 'at:').replace('def:', 'df:').replace('spa:', 'sa:').replace('spd:', 'sd:').replace('spe:', 'sp:')
        f.write('    ' + bst + '\n')
    elif type_update:
        type_update = False
        f.write('    ' + line.strip() + '\n')
    elif ability_update:
        ability_update = False
        abil = line.strip()
        abil = abil[:abil.find(',')] + '},'
        f.write('    ' + abil + '\n')
f.write('};')
f.close()
