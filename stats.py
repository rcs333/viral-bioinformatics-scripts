import datetime

format = '%m/%d/%y'
final_data = []
length = []
count = 0
new_count = 0
gud_loc_freqs = [0, 0, 0, 0]
wack_loc_freqs = [0, 0, 0, 0]
fem_tot = 0
fem_bingos = 0
m_tot = 0
m_bingo = 0
bin_map = {}

for line in open('bin_maps.csv'):
    bin_map[line.split(',')[0]] = line.split(',')[1].rstrip().lower()

for line in open('file.csv'):
    data_list = line.split(',')
    location = data_list[0]
    result = data_list[4].rstrip()
    if result == '':
        result = 'negative'
    admit_date = datetime.datetime.strptime(data_list[1], format)
    discharge_date = datetime.datetime.strptime(data_list[2], format)
    #print(line.strip())
    collection_date = datetime.datetime.strptime(data_list[3].split()[0].strip(), format)
    admit_delta = collection_date - admit_date
    discharge_delta = collection_date - discharge_date
    stay_len = admit_delta.days - discharge_delta.days
 #   if int(admit_delta.days) > 2 and data_list[0] == '4':
 #       print(data_list[4].strip())
    #if data_list[0] == '4':
    if admit_delta.days >= 0 and discharge_delta.days <= 0:# and location != 'outside':# and data_list[6] in bin_map.keys():
        final_data.append(location + ',' + str(admit_delta.days) + ',' + str(stay_len) + ',' + result + '\n')
        # if data_list[4].rstrip() == 'F':
        #
        #     fem_tot += 1
        #     if admit_delta.days == 0:
        #         fem_bingos += 1
        # elif data_list[4].rstrip() == 'M':
        #     #final_data.append(
        #       #  data_list[0] + ',' + str(admit_delta.days) + ',' + str(discharge_delta.days) + ',' + data_list[4])
        #     m_tot += 1
        #     if admit_delta.days == 0:
        #         m_bingo += 1

        #
        # gud_loc_freqs[int(data_list[0]) - 1] += 1
        # #if int(admit_delta.days) > 2 and data_list[0] == '4':
        #     #print(data_list[4].strip())
    # else:
    #     wack_loc_freqs[int(data_list[0]) - 1] += 1
    #if data_list[0] == '2':
    #    count += 1
    #    stay_delta = discharge_date - admit_date
    #    if stay_delta.days == 1:
    #        new_count += 1
     #   length.append(stay_delta.days)

f = open('viral_pos_neg.txt', 'w')
f.write('location,delta,stay_len,result\n')
for x in final_data:
    f.write(x)
f.close()
#
print(fem_bingos)
print(fem_tot)

print(m_bingo)
print(m_tot)


# print('total ' + str(count))
#
# print('avg ' + str(float(sum(length)) / count))
# print(length)
# print(new_count)
#
# print('good ones')
# print gud_loc_freqs
# print('bad')
# print(wack_loc_freqs)