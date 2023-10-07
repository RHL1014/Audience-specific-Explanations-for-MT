from tqdm import tqdm
import universal_func as uf


def get_align_res(res_file_road, sent_nums):
    all_align_index = []
    print("get align res begin...\n")
    with open(res_file_road, 'r', encoding='utf-8') as align_res_file:
        with tqdm(total=sent_nums) as pbar:
            for align_res_line in align_res_file:
                each_res = align_res_line.strip().split(" ")
                each_line = []
                for ele in each_res:
                    each_align = ele.strip().split("-")
                    each_line.append((int(each_align[0]), int(each_align[1])))
                all_align_index.append(each_line)
                pbar.update(1)
    print("get align res finish...\n")
    return all_align_index


def get_align_from_file(align_file_road):
    align = []
    align_file = open(align_file_road, 'r', encoding='utf-8')
    align_res = align_file.readlines()
    for line in align_res:
        res_each_align = line.strip().split()
        if len(res_each_align) != 3:
            raise ValueError('Lengths of the input line should be 3!')
        word = res_each_align[0]
        sentence_idx = int(res_each_align[1])
        align_idx = int(res_each_align[2])
        new_ele_align = (word, sentence_idx, align_idx)
        align.append(new_ele_align)
    align_file.close()
    return align


def get_align_index_sou(cand_list: list, align_all: list):
    cand_align_list = []
    with tqdm(total=len(cand_list)) as pbar:
        for cand in cand_list:
            (word, sent_idx, word_idx, word_count) = cand
            align_res_each_sent = align_all[sent_idx]
            for align_idx in range(len(align_res_each_sent)):
                align = align_res_each_sent[align_idx]
                (sou_idx, tar_idx) = align
                if sou_idx == word_idx:
                    new_ele = (word, sent_idx, align_idx, word_count)
                    cand_align_list.append(new_ele)
            pbar.update(1)
    return cand_align_list
    

def get_align_index_tar(cand_list: list, align_all: list):
    cand_align_list = []
    with tqdm(total=len(cand_list)) as pbar:
        for cand in cand_list:
            (word, sent_idx, word_idx, word_count) = cand
            align_res_each_sent = align_all[sent_idx]
            for align_idx in range(len(align_res_each_sent)):
                align = align_res_each_sent[align_idx]
                (sou_idx, tar_idx) = align
                if tar_idx == word_idx:
                    new_ele = (word, sent_idx, align_idx, word_count)
                    cand_align_list.append(new_ele)
            pbar.update(1)
    return cand_align_list


def get_index_candidates_sou(word_sentence_align, index_res):
    final_res = []
    with tqdm(total=len(word_sentence_align)) as bar_4:
        for item in word_sentence_align:
            (word, sent_index, align_idx, word_count) = item
            (word_sou_idx, word_tar_idx) = index_res[sent_index][align_idx]

            list_for_max = []
            for ele in index_res[sent_index]:
                (sou_idx_for_max, _) = ele
                list_for_max.append(sou_idx_for_max)
            max_index_sou = max(list_for_max)

            if word_sou_idx == max_index_sou:
                next_sou_idx = word_sou_idx
            else:
                next_sou_idx = word_sou_idx + 1

            next_word_align = []
            for (sou_idx, tar_idx) in index_res[sent_index]:
                if sou_idx == next_sou_idx:
                    next_word_align.append((sou_idx, tar_idx))

            # first:ending
            if next_sou_idx == word_sou_idx:
                if len(next_word_align) >= 2:
                    tar_idx_list = []
                    for (sou_idx_1, tar_idx_1) in next_word_align:
                        tar_idx_list.append(tar_idx_1)
                    tar_idx_max = max(tar_idx_list)
                    if tar_idx_max != word_tar_idx:
                        final_res.append((word, sent_index, align_idx, word_sou_idx, word_tar_idx,
                                          word_sou_idx, tar_idx_max, word_count))
            # second: not ending
            else:
                if len(next_word_align) == 1:
                    (sou_idx_1, tar_idx_1) = next_word_align[0]
                    final_res.append((word, sent_index, align_idx, word_sou_idx, word_tar_idx,
                                      sou_idx_1, tar_idx_1, word_count))
                elif len(next_word_align) >= 2:
                    find_max_tar = []
                    for (sou_idx_1, tar_idx_1) in next_word_align:
                        find_max_tar.append(tar_idx_1)
                    tar_max = max(find_max_tar)
                    final_res.append((word, sent_index, align_idx, word_sou_idx, word_tar_idx,
                                      word_sou_idx+1, tar_max, word_count))
            bar_4.update(1)
    return final_res


def get_index_candidates_tar(word_sentence_align, index_res):
    final_res = []
    with tqdm(total=len(word_sentence_align)) as bar_4:
        for item in word_sentence_align:
            (word, sent_index, align_index, word_count) = item
            (word_sou_idx, word_tar_idx) = index_res[sent_index][align_index]

            list_for_max = []
            for ele in index_res[sent_index]:
                (_, tar_idx_for_max) = ele
                list_for_max.append(tar_idx_for_max)
            max_index_tar = max(list_for_max)

            if word_tar_idx == max_index_tar:
                next_tar_idx = word_tar_idx
            else:
                next_tar_idx = word_tar_idx + 1

            next_word_align = []
            for (sou_idx, tar_idx) in index_res[sent_index]:
                if tar_idx == next_tar_idx:
                    next_word_align.append((tar_idx, sou_idx))

            # first:ending
            if next_tar_idx == word_tar_idx:
                if len(next_word_align) >= 2:
                    sou_idx_list = []
                    for (tar_idx_1, sou_idx_1) in next_word_align:
                        sou_idx_list.append(sou_idx_1)
                    sou_idx_max = max(sou_idx_list)
                    if sou_idx_max != word_sou_idx:
                        final_res.append((word, sent_index, align_index, word_tar_idx, word_sou_idx,
                                          word_tar_idx, sou_idx_max, word_count))

            else:  # second: not ending
                if len(next_word_align) == 1:
                    (tar_idx_1, sou_idx_1) = next_word_align[0]
                    final_res.append((word, sent_index, align_index, word_tar_idx, word_sou_idx,
                                        tar_idx_1, sou_idx_1, word_count))
                elif len(next_word_align) >= 2:
                    find_max_sou = []
                    for (tar_idx_1, sou_idx_1) in next_word_align:
                        find_max_sou.append(sou_idx_1)
                    sou_max = max(find_max_sou)
                    final_res.append((word, sent_index, align_index, word_tar_idx, word_sou_idx,
                                      word_tar_idx+1, sou_max, word_count))

            bar_4.update(1)

    return final_res


def get_candidates_distance_sou(candidates_sou, min_distance):
    # do not consider the negative distance
    cand_dis = []
    with tqdm(total=len(candidates_sou)) as pbar:
        for ele in candidates_sou:
            (_, _, _, _, word_tar_idx, _, tar_idx_1, _) = ele
            if tar_idx_1 - word_tar_idx >= min_distance:
                cand_dis.append(ele)
            pbar.update(1)
    return cand_dis


def get_candidates_distance_tar(candidates_tar, min_distance):
    cand_dis = []
    with tqdm(total=len(candidates_tar)) as pbar:
       for ele in candidates_tar:
            (_, _, _, _, word_sou_idx, _, sou_idx_1, _) = ele
            if sou_idx_1 - word_sou_idx >= min_distance:
                cand_dis.append(ele)
            pbar.update(1)
    return cand_dis


def check_redun_part_no_align_sou(candidates_sou, index_res):
    candidates = []
    with tqdm(total=len(candidates_sou)) as pbar:
        for cand_dis in candidates_sou:
            (_, sent_index, _, _, word_tar_idx, _, tar_idx_1, word_count) = cand_dis
            tar_align_list = []
            align_res_this_line = index_res[sent_index]
            for align_ele in align_res_this_line:
                (_, tar_idx) = align_ele
                tar_align_list.append(tar_idx)
            num = 0
            for tar_align_idx in range(word_tar_idx + 1, tar_idx_1):
                if tar_align_idx in tar_align_list:
                    num = num + 1
            length_redund = tar_idx_1 - word_tar_idx

            if check_distance_and_num(length_redund, num):
                candidates.append(cand_dis)
            pbar.update(1)
    return candidates


def check_redun_part_no_align_tar(candidates_tar, index_res):
    candidates = []
    with tqdm(total=len(candidates_tar)) as pbar:
        for cand_dis in candidates_tar:
            (_, sent_index, _, _, word_sou_idx, _, sou_idx_1, word_count) = cand_dis
            sou_align_list = []
            align_res_this_line = index_res[sent_index]
            for align_ele in align_res_this_line:
                (sou_idx, _) = align_ele
                sou_align_list.append(sou_idx)
            num = 0
            for sou_align_idx in range(word_sou_idx + 1, sou_idx_1):
                if sou_align_idx in sou_align_list:
                    num = num + 1
            length_redund = sou_idx_1 - word_sou_idx

            if check_distance_and_num(length_redund, num):
                candidates.append(cand_dis)
            pbar.update(1)
    return candidates


def check_distance_and_num(distance, num):
    res = True
    if distance <= 4:
        if num == 0:
            res = True
        else:
            res = False
    elif 4 < distance <= 7:
        if num <= 1:
            res = True
        else:
            res = False
    else:
        if num <= 2:
            res = True
        else:
            res = False
    return res


def check_distance_and_num_strict(distance, num):
    res = True
    if num == 0:
        res = True
    else:
        res = False
    return res


if __name__ == '__main__':
    road = "/export/data4/rlou/exp/cc_matrix/en_de/test/"
    total_num_2 = 0
    total_num_3 = 0
    total_num_4 = 0
    wiki_sou_th = 5000
    total_nums_file_2 = road + "total_num/2_filter_one_align_sou_" + str(wiki_sou_th) + "_total_nums.txt"
    total_nums_file_3 = road + "total_num/3_filter_distance_sou_" + str(wiki_sou_th) + "_total_nums.txt"
    total_nums_file_4 = road + "total_num/4_filter_distance_no_align_sou_" + str(wiki_sou_th) + "_total_nums.txt"
    num_f_t_2 = open(total_nums_file_2, 'w', encoding='utf-8')
    num_f_t_3 = open(total_nums_file_3, 'w', encoding='utf-8')
    num_f_t_4 = open(total_nums_file_4, 'w', encoding='utf-8')
    for idx in range(1, 6):
        sou_road = road + str(idx)+ "/sou/"
        res_road = road + str(idx)+ "/res/"
        file_in = sou_road + "en_de_res_" + str(idx) + ".txt"
        nums_sentences = 5000000
        align_res = get_align_res(file_in, nums_sentences)
        
        cand_file = res_road + "cand/cand_1_check_wiki_sou_" + str(wiki_sou_th) + ".txt"
        cand_1 = uf.get_cand_1_from_file(cand_file)
    
        # first transfer word_idx to align_idx
        # then get candidate with only one alignment
        cand_1_new = get_align_index_sou(cand_1, align_res)
        cand_2_one_align = get_index_candidates_sou(cand_1_new, align_res)
        cand_file_2 = res_road + "cand/cand_2_one_align_sou_" + str(wiki_sou_th)+".txt"
        uf.save_cand_alignment_filter_sou_in_file(cand_2_one_align, cand_file_2)
        nums_file_2 = res_road + "nums/2_filter_one_align_sou_" + str(wiki_sou_th) + "_nums.txt"
        num_cand_2 = uf.get_nums_for_alignment_filter_sou(cand_2_one_align, nums_file_2)
        total_num_2 = total_num_2 + num_cand_2
        # get candidate with redundant part
        min_distance = 4
        cand_3_distance = get_candidates_distance_sou(cand_2_one_align, min_distance)
        cand_file_3 = res_road + "cand/cand_3_distance_sou_" + str(wiki_sou_th) + ".txt"
        uf.save_cand_alignment_filter_sou_in_file(cand_3_distance, cand_file_3)
        nums_file_3 = res_road + "nums/3_filter_distance_sou_" + str(wiki_sou_th) + "_nums.txt"
        num_cand_3 = uf.get_nums_for_alignment_filter_sou(cand_3_distance, nums_file_3)
        total_num_3 = total_num_3 + num_cand_3
        # get candidate with redundant part and no alignment for the redundant part
        cand_4_dis_no_align = check_redun_part_no_align_sou(cand_3_distance, align_res)
        cand_file_4 = res_road + "cand/cand_4_distance_no_align_sou_" + str(wiki_sou_th) + ".txt"
        uf.save_cand_alignment_filter_sou_in_file(cand_4_dis_no_align, cand_file_4)
        nums_file_4 = res_road + "nums/4_filter_distance_no_align_sou_" + str(wiki_sou_th) + "_nums.txt"
        num_cand_4 = uf.get_nums_for_alignment_filter_sou(cand_4_dis_no_align, nums_file_4)
        total_num_4 = total_num_4 + num_cand_4

    num_f_t_2.write("total: " + str(total_num_2) + "\n")
    num_f_t_3.write("total: " + str(total_num_3) + "\n")
    num_f_t_4.write("total: " + str(total_num_4) + "\n")
    num_f_t_2.close()
    num_f_t_3.close()
    num_f_t_4.close()
    
