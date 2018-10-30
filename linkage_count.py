read_next = False
id_list = []
nt_list = []
for line in open('shit.fasta'):
    if read_next:
        nt_list.append(line.strip())
        read_next = False
    else:
        id = ''
        print(line)
        s = line.split('-')[1]
        id = s.split(':')[2]
        id += s.split(':')[3]
        id += s.split(':')[4].split('#')[0]

        read_next = True
        id_list.append(id)

print(len(id_list))
print(len(nt_list))

mapmap = {}

for x in range(0, len(id_list)):
    if id_list[x] in mapmap.keys():
        mapmap[id_list[x]] += '#' + nt_list[x]
    else:
        mapmap[id_list[x]] = nt_list[x]
print(mapmap.values())
final_map = {}
for item in mapmap.values():
    print(item)
    one = item.split('#')[0]
    if len(item.split('#')) < 2:
        two = '-----'
    else:
        two = item.split('#')[1]
    name = ''
    if one[0] == 'T' or two[0] == 'T':
        name += '1'
    if one[1] == 'G' or two[1] =='G':
        name += '2'
    if one[2] == 'A' or two[2] == 'A':
        name += '3'
    if one[3] == 'T' or two[3] == 'T':
        name += '4'
    if one[4] == 'A' or two[4] == 'A':
        name += '5'
    if name in final_map.keys():
        final_map[name] += 1
    else:
        final_map[name] = 1

print(final_map)

