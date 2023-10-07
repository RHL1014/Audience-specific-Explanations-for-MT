import random


def get_random_sent_idx(start_num, total_num, req_num):
    return random.sample(range(start_num ,total_num), req_num)


def get_sent_num_from_file(input_file):
    num_list = []
    with open(input_file, 'r', encoding='utf-8') as inp_f:
        for line in inp_f:
            num = int(line.strip())
            num_list.append(num)
    return num_list

def get_sent_from_file(input_file):
    sent_list = []
    with open(input_file, 'r', encoding='utf-8') as inp_f:
        for line in inp_f:
            sent = line.strip()
            sent_list.append(sent)
    return sent_list


def get_sent_cand_with_nums(sent_list: list, num_list:list, start_num: int, end_num: int, step: int):
    sent_list_select = []
    for num_s in num_list:
        if start_num <= num_s < end_num:
            sent = sent_list[num_s-step]
            sent_list.append(sent)
    return sent_list_select
    


if __name__ == '__main__':
    #total_nums = 247470557
    #req_nums = 5000000
    #start_num = 5000000
    #rand_res = get_random_sent_idx(start_num, total_nums, req_nums)
    #output_file = "/export/data4/rlou/exp/cc_matrix/en_de/test/sent_num.txt"
    #with open(output_file, 'w', encoding='utf-8') as output_f:
    #    for sent_num in rand_res:
    #        output_f.write(str(sent_num)+"\n")
    output_road = "D:\\thesis_data\\cc_Matrix\\en_fr\\test\\"
    num_file = output_road + "sent_num_1.txt"
    num_list = get_sent_num_from_file(num_file)
    input_road = "E:\\cc_matrix\\en-fr\\exp\\"
    sent_final = []
    for file_idx in range(1, 10):
        file_road = input_road + "en_token_"+str(file_idx)+".txt"
        sent_all_list = get_sent_from_file(file_road)
        start_nums = (file_idx - 1) * 33000000
        end_nums = file_idx * 33000000
        step = start_nums
        sent_sep_list = get_sent_cand_with_nums(sent_all_list, num_list, start_nums, end_nums, step)
        sent_final.extend(sent_sep_list)
    output_file = "en_test_1.txt"
    with open(output_road + output_file, 'w', encoding='utf-8') as output_f:
        for sent in sent_final:
            output_f.write(sent + "\n")
    
    

