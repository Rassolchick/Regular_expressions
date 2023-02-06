from pprint import pprint
import csv
import re

def merge_lists(list1, list2):
    new_list = []
    for i in range(len(list2)):
        if list2[i] == '':
            new_list.append(list1[i])
        else:
            new_list.append(list2[i])
    return new_list

with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

for line in contacts_list:
    # result_ext, result_phone = '', ''
    FIO = ' '.join(line[0:3]).strip().split(' ')
    FIO = FIO + [''] * (3 - len(FIO))
    line[:3] = FIO[:3]

    result_phone = re.sub(
        r"(\+7|8)\W*(\d{3})\W*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})",
        r"+7(\2)\3-\4-\5", line[5])
    result = re.sub(r"\(*доб.\s*(\d{4})\)*", r"доб.\1", result_phone)
    line[5] = result

contacts_list_new = []
contacts_list_new.append(contacts_list[0])
done_index_list = []
for index in range(1, len(contacts_list)):
    line = contacts_list[index]
    coincidence_list = [
        n for n, x in enumerate(contacts_list) if x[:2] == line[:2]
    ]
    merge_list = [''] * len(line)
    for coincidence in coincidence_list:
        if coincidence not in done_index_list:
            merge_list = merge_lists(contacts_list[coincidence], merge_list)
            done_index_list.append(coincidence)
    if ''.join(merge_list) != '':
      contacts_list_new.append(merge_list)

with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list_new)
