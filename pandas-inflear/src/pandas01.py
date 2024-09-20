# 파일 오픈 (Plain Text)

# 프로그래밍에서 파일은 다음과 같은 3가지 명령의 순서로 처리할 수 있음
# 파일 오픈
# 파일 읽기 또는 쓰기
# 파일 닫기


# 형식

# 파일디스크립터변수 = open(파일이름, 파일열기모드, 인코딩(선택))

# r	읽기 모드: 파일을 읽기만 할 때 사용함
# w	쓰기 모드: 파일에 데이터를 쓸 때 사용함 (기존 파일 데이터는 삭제됨)
# a	추가 모드: 파일의 기존 데이터 끝에서부터 데이터를 추가할 때 사용함

data_file = open('../data/text_data.txt', 'r', encoding='utf-8-sig')
# 파일을 읽은 다음에 항상 닫아야 함
data_file.close()

# with 와 함께 사용하면 작업이 끝난 뒤에 자동으로 해당 파일을 닫아줌
with open('../data/text_data.txt', 'r', encoding='utf-8-sig') as file_desc:
    print('test')

# -------------------------------------------------------

# 파일 읽기

# 전체 데이터를 한줄씩 리스트타입으로 읽기
data_lines = open('../data/text_data.txt', 'r', encoding='utf-8-sig').readlines()
print("\n전체 데이터를 한줄씩 리스트타입으로 읽기 : ", data_lines)

# 현재까지 읽은 파일 데이터의 다음 한 줄을 문자열 타입으로 읽기
data_line = open('../data/text_data.txt', 'r', encoding='utf-8-sig').readline()
print("\n현재까지 읽은 파일 데이터의 다음 한 줄을 문자열 타입으로 읽기 : ", '\n' + data_line)

# 전체 파일 데이터를 문자열 타입으로 읽기
data_all_line = open('../data/text_data.txt', 'r', encoding='utf-8-sig').read()
print("\n전체 파일 데이터를 문자열 타입으로 읽기:", '\n' + data_all_line)

# -------------------------------------------------------

# 파일 쓰기

data_to_write = open('../data/text_data_write.txt', 'w', encoding='utf-8-sig')
data_to_write.write('안녕하세요.')
data_to_write.write('감사해요.')
# 파일을 쓴 후 닫지 않으면 읽지 못함
data_to_write.close()

data_write_read = open('../data/text_data_write.txt', 'r', encoding='utf-8-sig').read()
print("\n쓴 파일 읽기 :", '\n' + data_write_read)

# -------------------------------------------------------

# 파일 수정

data_to_update = open('../data/text_data_write.txt', 'a', encoding='utf-8-sig')
data_to_update.write('\n잘있어요.')
data_to_update.write('\n다시만나요.')
data_to_update.close()

data_update_read = open('../data/text_data_write.txt', 'r', encoding='utf-8-sig').read()
print("\n수정한 파일 읽기 :", '\n' + data_update_read)
