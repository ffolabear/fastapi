assignment = open('../data/text_data_practice.txt', 'w', encoding='utf-8-sig')
assignment.write('유치원A\n')
assignment.write('초등학교B\n')
assignment.write('중학교C\n')
assignment.write('고등학교D\n')
assignment.close()

assignment = open('../data/text_data_practice.txt', 'a', encoding='utf-8-sig')
assignment.write('대학교E\n')
assignment.close()

assignment = open('../data/text_data_practice.txt', 'r', encoding='utf-8-sig')
print(assignment.read())