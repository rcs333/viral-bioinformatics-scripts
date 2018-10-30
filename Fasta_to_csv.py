


def read_fasta(fasta_file_loc):
    strain_list = []
    genome_list = []
    dna_string = ''


    for line in open(fasta_file_loc):
        if line[0] == '>':
            strain_list.append(line.strip())
            if dna_string != '':
                # strip leading and trailing Ns or ?s because there's no reason to submit them
                xip = 0
                while dna_string[xip] == 'N' or dna_string[xip] == '?':
                    xip += 1

                y = len(dna_string)
                while dna_string[y-1] == 'N' or dna_string[y-1] == '?':
                    y -= 1

                dna_string = dna_string[xip:y]

                genome_list.append(dna_string)
                dna_string = ''
        else:
            dna_string += line.strip()
    # Just to make sure all our sequences are on the same page

    return strain_list, genome_list

if __name__ == '__main__':
    strain_list, genome_list = read_fasta('All_hn.fasta')

    a = open('NP.csv', 'w')
    b = open('NS1.csv', 'w')
    c = open('M1.csv', 'w')
    d = open('PA.csv', 'w')
    e = open('PB2.csv', 'w')
    f = open('PB1.csv', 'w')
    g = open('HA.csv', 'w')
    h = open('NA.csv', 'w')

    for x in range(0, len(genome_list)):
        if 'X' not in genome_list[x] and '*' not in genome_list[x]:
            prot = strain_list[x].split('_')[0]
            if prot == '>NP':
                a.write(strain_list[x] + ',' + genome_list[x] + '\n')
            elif prot == '>NS1':
                b.write(strain_list[x] + ',' + genome_list[x] + '\n')
            elif prot == '>M1':
                c.write(strain_list[x] + ',' + genome_list[x] + '\n')
            elif prot == '>PA':
                d.write(strain_list[x] + ',' + genome_list[x] + '\n')
            elif prot == '>PB2':
                e.write(strain_list[x] + ',' + genome_list[x] + '\n')
            elif prot == '>PB1':
                f.write(strain_list[x] + ',' + genome_list[x] + '\n')
            elif prot == '>HA':
                g.write(strain_list[x] + ',' + genome_list[x] + '\n')
            elif prot == '>NA':
                h.write(strain_list[x] + ',' + genome_list[x] + '\n')
    a.close()
    b.close()
    c.close()
    d.close()
    f.close()
    g.close()
    h.close()

