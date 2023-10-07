import sys
from tqdm import tqdm


def get_entity_from_file(file):
    res_entity_list = set()
    with open(file, 'r', encoding='utf-8') as entity_f:
        for line in entity_f:
            ent_1 = line.strip()
            res_entity_list.add(ent_1)
    return res_entity_list


def get_sent_pair_from_file(sou_file, tar_file):
    sentence_pairs = []
    src = open(sou_file, encoding='utf-8').readlines()
    tgt = open(tar_file, encoding='utf-8').readlines()
    if not len(src) == len(tgt):
        raise ValueError('Lengths of the two input files should be the same!')
    
    for sent_pair in zip(src, tgt):
        sentence_pairs.append(sent_pair)
    return sentence_pairs


def get_sent_pair_with_entity(entity_list_in: set[str], sentence_pairs: list[tuple[str, str]]):
    tar_sent_pairs = []
    tar_nums_list = []
    with tqdm(total=len(entity_list_in)) as bar:
        for entity in entity_list_in:
            entity_count = 0
            for sent_pair in sentence_pairs:
                (s, t) = sent_pair
                if entity in s:
                    tar_sent_pairs.append(sent_pair)
                    entity_count = entity_count + 1
            tar_nums_list.append((entity, entity_count))
            bar.update(1)
    return tar_sent_pairs, tar_nums_list


def save_tar_sent_pairs(out_file, tar_sent_pairs: list[tuple[str, str]], entity_list_in: set[str]):
    with open(out_file, 'w', encoding='utf-8') as out_f:
        for sent_pair in tar_sent_pairs:
            (s, t) = sent_pair
            s, t = s.strip(), t.strip()
            for entity in entity_list_in:
                if entity in s:
                    tar_sent_pair = (' ||| ').join([s, t]) + '\n'
                    out_f.write(entity + ": " + tar_sent_pair)
                    out_f.write("\n")
      
                    
def save_tar_nums(out_nums_file, tar_nums_res: list[tuple[str, int]]):
    with open(out_nums_file, 'w', encoding='utf-8') as out_f:
        for nums_res in tar_nums_res:
            (entity, count) = nums_res
            out_f.write(entity + ": " + str(count) + "\n")


def caculate_per(in_f_1, in_f_2, out_f):
    total_num = {}
    check_res = {}
    per_res = {}
    with open(in_f_1, 'r', encoding='utf-8') as inp_1:
        for line in inp_1:
            word = line.strip().split(':')[0].strip()
            num = line.strip().split(':')[1].strip()
            total_num[word] = int(num)
    with open(in_f_2, 'r', encoding='utf-8') as inp_2:
        for line in inp_2:
            word_1 = line.strip().split(':')[0].strip()
            num_1 = line.strip().split(':')[1].strip()
            check_res[word_1] = int(num_1)
    for word in total_num.keys():
        percent = float(check_res[word])/float(total_num[word])
        per_res[word] = percent
    with open(out_f, 'w', encoding='utf-8') as out_p:
        for word in per_res.keys():
            out_p.write(word + ": " + str(per_res[word]) + "\n")
        out_p.write("\n")
        total_num = len(per_res)
        one_num = 0
        greater_half_num = 0
        for word in per_res.keys():
            if per_res[word] == 1.0:
                one_num = one_num +1
            if per_res[word] >= 0.5:
                greater_half_num = greater_half_num +1
        out_p.write("total_num: " + str(total_num) + "\n")
        out_p.write("1_num: " + str(one_num) + "\n")
        out_p.write(">=0.5_num: " + str(greater_half_num) + "\n")
        
        
            
    

if __name__ == '__main__':
    road = "D:\\thesis_data\\writing\\cc_matrix\\en_zh\\writing\\check_entity\\"
    total_num_f_name = "nums_total.txt"
    res_f_name = "res.txt"
    per_res_f_name = "per_res.txt"
    caculate_per(road + total_num_f_name, road + res_f_name, road + per_res_f_name)
    
    '''
    entity_file_name = "11.1+13_word.txt"
    entity_list = get_entity_from_file(road+entity_file_name)
    
    res_road = road + "check_entity\\"
    nums_list = []
    for file_idx in range(1, 6):
        sou_road = road + str(file_idx) + "\\sou\\"
        sou_sent_file = sou_road + "en_token_1000k_" + str(file_idx) + ".txt"
        tar_sent_file = sou_road + "fr_token_1000k_" + str(file_idx) + ".txt"
        sent_pairs = get_sent_pair_from_file(sou_sent_file, tar_sent_file)
        target_sentence_pairs, tar_nums_res = get_sent_pair_with_entity(entity_list, sent_pairs)
        nums_list = nums_list + tar_nums_res
        output_file = res_road + "sent_in_file_" + str(file_idx) + ".txt"
        output_nums_file = res_road + "nums_in_file_" + str(file_idx) + ".txt"
        save_tar_sent_pairs(output_file, target_sentence_pairs, entity_list)
        save_tar_nums(output_nums_file, tar_nums_res)
        
    output_nums_file_total = res_road + "nums_total.txt"
    with open(output_nums_file_total, 'w', encoding='utf-8') as out_f:
        for entity_s in entity_list:
            count_total = 0
            for nums_res_s in nums_list:
                (ent, cot) = nums_res_s
                if ent == entity_s:
                    count_total = count_total + cot
            out_f.write( entity_s + ": " + str(count_total) + "\n")
    '''
            
    
    
