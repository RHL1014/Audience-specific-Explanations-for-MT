from tqdm import tqdm
import universal_func as uf


def get_word_list(input_file: str, nums_sent: int):
    word_list_res = []
    print("get word list begin...\n")
    with open(input_file, 'r', encoding='utf-8') as word_file:
        with tqdm(total=nums_sent) as bar:
            for sent in word_file:
                words = sent.strip().split()
                word_list_res.append(words)
                bar.update(1)
    print("get word list finish...\n")
    return word_list_res


def get_word_count_dict_from_file(input_file: str):
    word_count_dict = {}
    print("get word count dict from file begin...\n")
    with open(input_file, 'r', encoding='utf-8') as word_count_file:
        for line in word_count_file:
            word_count = line.strip().split()
            word = word_count[0]
            count = int(word_count[1])
            word_count_dict[word] = count
    print("get word count dict from file finish...\n")
    return word_count_dict
    
    
def get_word_count_under_threshold(word_count_dict: dict, threshold_num: int):
    dict_threshold = {}
    for word in word_count_dict.keys():
        count = word_count_dict[word]
        if count <= threshold_num:
            dict_threshold[word] = count
    return dict_threshold


def save_dict_to_file(word_count_dict: dict, output_file: str):
    output_f = open(output_file, 'w', encoding='utf-8')
    words_count_dict_sorted = sorted(
        word_count_dict.items(),
        key=lambda x: x[0],
        reverse=False
    )
    words_count_dict_sorted = sorted(
        words_count_dict_sorted,
        key=lambda x: x[1],
        reverse=False
    )
    for (word, count) in words_count_dict_sorted:
        output_one = word + " " + str(count) + "\n"
        output_f.write(output_one)
    output_f.close()

    
def is_word_rare_in_file(file_word_count_dict: dict, word: str, threshold_num_lower: int, threshold_num_upper: int):
    res = False
    count = 0
    if word in file_word_count_dict:
        count = file_word_count_dict[word]
    if threshold_num_lower <= count <= threshold_num_upper:
        res = True
    return res


def is_word_rare_in_wiki(wiki_word_count_dict: dict, word: str, wiki_threshold_num: int):
    res = False
    count = 0
    if word in wiki_word_count_dict:
        count = wiki_word_count_dict[word]
    if count <= wiki_threshold_num:
        res = True
    return res


def has_punctuation_in_sent_part(sent_index: int, index_begin: int, index_end: int, all_word_res: list[list[str]]):
    #punc = "{}()[].|&*/#\~.,:;?!'-<>$%^_=+\""
    punc = "（）［］〔〕【】「」『』“”’‘《》〈〉，：——{}()[]<>,:-=\""
    #punc = "{}()[] <>,: -= \""
    # half_width_punc = ""
    # full_width_punc = ""
    res = False
    for word_idx in range(index_begin + 1, index_end):
        word = all_word_res[sent_index][word_idx]
        for p in list(punc):
            if p in word:
                res = True
    return res


def has_only_explain_word_in_sent_part(sent_index: int, index_begin: int, index_end: int,
                                  all_word_res: list[list[str]], exp_word: str):
    res = False
    word_list = []
    #punc = "{}()[].|&*/#\~.,:;?!'-<>$%^_=+\""
    #punc = "{}()[]<>,:-=\""
    punc = "（）［］〔〕【】「」『』“”’‘《》〈〉，：——{}()[]<>,:-=\""
    for word_idx in range(index_begin + 1, index_end):
        word = all_word_res[sent_index][word_idx]
        if (word not in list(punc)) and (word != exp_word):
            word_list.append(word)
    if len(word_list) == 0:
        res = True

    return res


def get_rare_word_in_all_sent(all_sent: list[list[str]], wc_dict: dict, threshold_num_lower: int, threshold_num_upper: int):
    res_dict = {}
    nums_sent = len(all_sent)
    with tqdm(total=nums_sent) as pbar:
        for sent_idx in range(nums_sent):
            sentence = all_sent[sent_idx]
            for word_idx in range(len(sentence)):
                word = sentence[word_idx]
                if is_word_rare_in_file(wc_dict, word, threshold_num_lower, threshold_num_upper):
                    ele_saved = (word, sent_idx, word_idx)
                    count = 0
                    if word in wc_dict:
                        count = wc_dict[word]
                    res_dict[ele_saved] = count
            pbar.update(1)
    return res_dict


def get_rare_word_with_wiki(cand_1: dict, wiki_dict: dict, threshold_num: int):
    res_dict = {}
    cand_nums = len(cand_1)
    with tqdm(total=cand_nums) as pbar:
        for ele in cand_1.keys():
            (word, _, _) = ele
            if is_word_rare_in_wiki(wiki_dict, word, threshold_num):
                res_dict[ele] = cand_1[ele]
            pbar.update(1)
    return res_dict
    

def add_target_word_into_cand_sou(cand_sou: list, target_sent_list: list, target_word_dict: dict):
    cand_sou_new = []
    with tqdm(total=len(cand_sou)) as pbar:
        for cand in cand_sou:
            (word, sent_index, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, word_count) = cand
            tar_word = target_sent_list[sent_index][word_tar_idx]
            tar_word_count = 0
            if tar_word in target_word_dict:
                tar_word_count = target_word_dict[tar_word]
            new_cand = (word, tar_word, sent_index, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1,
                        word_count, tar_word_count)
            cand_sou_new.append(new_cand)
            pbar.update(1)
    return cand_sou_new


def check_target_word_rare_cand_sou(cand_sou: list, threshold_num_lower: int, threshold_num_upper: int):
    cand_sou_new = []
    with tqdm(total=len(cand_sou)) as pbar:
        for cand in cand_sou:
            (_, tar_word, _, _, _, _, _, _, _, tar_word_count) = cand
            if threshold_num_lower <= tar_word_count <= threshold_num_upper:
                cand_sou_new.append(cand)
            pbar.update(1)
    return cand_sou_new


def check_punctuation_in_redundant_part_sou(cand_sou: list, target_sent_list: list):
    cand_sou_new = []
    with tqdm(total=len(cand_sou)) as pbar:
        for cand in cand_sou:
            (_, _, sent_index, _, _, word_tar_idx, _, tar_idx_1, _, _) = cand
            if has_punctuation_in_sent_part(sent_index, word_tar_idx, tar_idx_1, target_sent_list):
                cand_sou_new.append(cand)
            pbar.update(1)
    return cand_sou_new


def check_not_only_explained_word_in_redundant_part_sou(cand_sou: list, target_sent_list: list):
    cand_sou_new = []
    with tqdm(total=len(cand_sou)) as pbar:
        for cand in cand_sou:
            (_, tar_word, sent_index, _, _, word_tar_idx, _, tar_idx_1, _, _) = cand
            if not has_only_explain_word_in_sent_part(sent_index, word_tar_idx, tar_idx_1, target_sent_list, tar_word):
                cand_sou_new.append(cand)
            pbar.update(1)
    return cand_sou_new


def add_count_in_file_into_cand_sou(cand_sou: list, wiki_sou_dict: dict, wiki_tar_dict: dict):
    new_cand_sou = []
    with tqdm(total=len(cand_sou)) as pbar:
        for cand in cand_sou:
            (word, tar_word, sent_index, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1,
             word_count, tar_word_count) = cand
            wiki_sou_count = 0
            wiki_tar_count = 0
            if word in wiki_sou_dict:
                wiki_sou_count = wiki_sou_dict[word]
            if tar_word in wiki_tar_dict:
                wiki_tar_count = wiki_tar_dict[tar_word]
            new_cand = (word, tar_word, sent_index, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1,
                        word_count, tar_word_count, wiki_sou_count, wiki_tar_count)
            new_cand_sou.append(new_cand)
            pbar.update(1)
    return new_cand_sou


def check_count_in_file_cand_sou(cand_sou: list, threshold_num_sou: int, threshold_num_tar: int):
    cand_sou_new = []
    with tqdm(total=len(cand_sou)) as pbar:
        for cand in cand_sou:
            (_, _, _, _, _, _, _, _, _, _, wiki_sou_count, wiki_tar_count) = cand
            if wiki_sou_count <= threshold_num_sou and wiki_tar_count <= threshold_num_tar:
                cand_sou_new.append(cand)
            pbar.update(1)
    return cand_sou_new
    
    
if __name__ == '__main__':
    road = "D:\\thesis_data\\cc_Matrix\\en_zh\\"

    '''
    # filter 1.part
    en_wiki_dict_file = "D:\\thesis_data\\wiki\\word_count\\en_wiki_word_count_all.txt"
    en_wiki_dict = get_word_count_dict_from_file(en_wiki_dict_file)
    total_num_1 = 0
    wiki_threshold_nums_sou_lower = 0
    wiki_threshold_nums_sou_upper = 100
    total_nums_file = road + "total_num_desktop\\1_filter_check_wiki_sou_" + str(
        wiki_threshold_nums_sou_upper) + "_total_nums.txt"
    num_f_t_1 = open(total_nums_file, 'w', encoding='utf-8')
    for idx in range(1, 6):
        sou_road = road + str(idx) + "\\sou\\"
        res_road = road + str(idx) + "\\res\\"
        file_in = sou_road + "en_token_1000k_" + str(idx) + ".txt"
        nums_sentences = 1000000
        en_list = get_word_list(file_in, nums_sentences)
        
        rare_word = get_rare_word_in_all_sent(en_list, en_wiki_dict, wiki_threshold_nums_sou_lower,
                                              wiki_threshold_nums_sou_upper)
        cand_file = res_road + "cand\\cand_1_check_wiki_sou_"+str(wiki_threshold_nums_sou_upper)+".txt"
        uf.save_cand_1_in_file(rare_word, cand_file)
        nums_file = res_road + "nums\\1_filter_check_wiki_sou_"+str(wiki_threshold_nums_sou_upper)+"_nums.txt"
        num_cand_1 = uf.get_nums_for_1_filter(rare_word, nums_file)
        total_num_1 = total_num_1 + num_cand_1
    num_f_t_1.write("total: " + str(total_num_1) + "\n")
    num_f_t_1.close()
    '''
    '''
    tar_wiki_dict_file = "D:\\thesis_data\\wiki\\word_count\\zh_wiki_word_count_all.txt"
    tar_wiki_dict = get_word_count_dict_from_file(tar_wiki_dict_file)
    total_num_5 = 0
    total_num_6 = 0
    total_num_7 = 0
    wiki_sou_th = 5000
    threshold_nums_lower = 0
    threshold_nums_upper = 1000
    total_nums_file_5 = road + "total_num_desktop\\5_filter_check_wiki_tar_" + str(wiki_sou_th) + "_" + str(
        threshold_nums_upper) + "_total_nums.txt"
    total_nums_file_6 = road + "total_num_desktop\\6_filter_punctuation_in_redundant_" + str(wiki_sou_th) + "_" + str(
        threshold_nums_upper) + "_total_nums.txt"
    total_nums_file_7 = road + "total_num_desktop\\7_filter_not_only_exp_word_in_redundant_" + str(wiki_sou_th) + "_" + str(
        threshold_nums_upper) + "_total_nums.txt"
    num_f_t_5 = open(total_nums_file_5, 'w', encoding='utf-8')
    num_f_t_6 = open(total_nums_file_6, 'w', encoding='utf-8')
    num_f_t_7 = open(total_nums_file_7, 'w', encoding='utf-8')
    for idx in range(1, 6):
        # filter 3. part
        sou_road = road + str(idx) + "\\sou\\"
        res_road = road + str(idx) + "\\res\\"
        file_in = sou_road + "zh_token_1000k_" + str(idx) + ".txt"
        nums_sentences = 1000000
        tar_list = get_word_list(file_in, nums_sentences)
        
        # get 4. filter's candidate from file
        cand_file_4 = res_road + "cand\\cand_4_distance_no_align_sou_"+str(wiki_sou_th)+".txt"
        cand_4_dis_no_align = uf.get_cand_alignment_filter_sou_from_file(cand_file_4)
    
        # get candidate with target word is rare
        cand_4_new = add_target_word_into_cand_sou(cand_4_dis_no_align, tar_list, tar_wiki_dict)
        cand_5 = check_target_word_rare_cand_sou(cand_4_new, threshold_nums_lower, threshold_nums_upper)
        cand_5_file = res_road + "cand\\cand_5_check_wiki_tar_"+str(wiki_sou_th)+"_"+str(threshold_nums_upper)+".txt"
        uf.save_cand_word_filter_sou_in_file(cand_5, cand_5_file)
        nums_5_file = res_road + "nums\\5_filter_check_wiki_tar_"+str(wiki_sou_th)+"_"+str(threshold_nums_upper)+"_nums.txt"
        num_cand_5 = uf.get_nums_for_word_filter_sou(cand_5, nums_5_file)
        total_num_5 = total_num_5 + num_cand_5
        # get candidate with redundant part and punctuation in redundant part.
        cand_6 = check_punctuation_in_redundant_part_sou(cand_5, tar_list)
        cand_6_file = res_road + "cand\\cand_6_punctuation_in_redundant_"+str(wiki_sou_th)+"_"+str(threshold_nums_upper)+".txt"
        uf.save_cand_word_filter_sou_in_file(cand_6, cand_6_file)
        nums_6_file = res_road + "nums\\6_filter_punctuation_in_redundant_"+str(wiki_sou_th)+"_"+str(threshold_nums_upper)+"_nums.txt"
        num_cand_6 = uf.get_nums_for_word_filter_sou(cand_6, nums_6_file)
        total_num_6 = total_num_6 + num_cand_6
        # get candidate with redundant part and not only the explained word in redundant part
        cand_7 = check_not_only_explained_word_in_redundant_part_sou(cand_6, tar_list)
        cand_7_file = res_road +"cand\\cand_7_not_only_exp_word_in_redundant_"+str(wiki_sou_th)+"_"+str(threshold_nums_upper)+".txt"
        uf.save_cand_word_filter_sou_in_file(cand_7, cand_7_file)
        nums_7_file = res_road + "nums\\7_filter_not_only_exp_word_in_redundant_"+str(wiki_sou_th)+"_"+str(threshold_nums_upper)+"_nums.txt"
        num_cand_7 = uf.get_nums_for_word_filter_sou(cand_7, nums_7_file)
        total_num_7 = total_num_7 + num_cand_7
    num_f_t_5.write("total: " + str(total_num_5) + "\n")
    num_f_t_6.write("total: " + str(total_num_6) + "\n")
    num_f_t_7.write("total: " + str(total_num_7) + "\n")
    num_f_t_5.close()
    num_f_t_6.close()
    num_f_t_7.close()
    '''
    
    # filter 4. part
    for idx in range(1, 6):
        sou_road = road + str(idx) + "\\sou\\"
        res_road = road + str(idx) + "\\res\\"
        en_dict_file = res_road + "word_count\\en_word_count.txt"
        de_dict_file = res_road + "word_count\\zh_word_count.txt"
        en_dict = get_word_count_dict_from_file(en_dict_file)
        de_dict = get_word_count_dict_from_file(de_dict_file)
        wiki_sou_th = 5000
        wiki_tar_th = 4000
        
        # add word_count into candidate
        cand_7_file = res_road + "cand\\cand_7_not_only_exp_word_in_redundant_"+str(wiki_sou_th)+"_"+str(wiki_tar_th)+".txt"
        cand_7 = uf.get_cand_word_filter_sou_from_file(cand_7_file)
        new_cand_7 = add_count_in_file_into_cand_sou(cand_7, en_dict, de_dict)
    
        #save check cand
        cand_7_file = res_road + "cand\\cand_7_before_count_in_file_"+str(wiki_sou_th)+"_"+str(wiki_tar_th)+".txt"
        uf.save_cand_count_in_file_filter_sou_in_file(new_cand_7, cand_7_file)
        nums_7_file = res_road + "nums\\7_filter_before_count_in_file_"+str(wiki_sou_th)+"_"+str(wiki_tar_th)+"_nums.txt"
        uf.get_nums_for_count_in_file_filter_sou(new_cand_7, nums_7_file)
        check_7_file = res_road + "check\\check_before_count_in_file_filter_"+str(wiki_sou_th)+"_"+str(wiki_tar_th)+".txt"
        uf.save_cand_check_count_in_file_filter_sou_with_file(new_cand_7, check_7_file)
    
        
        # get candidate with wiki count check
        sou_th_num = 100
        tar_th_num = 50
        cand_8 = check_count_in_file_cand_sou(new_cand_7, sou_th_num, tar_th_num)
        cand_8_file = res_road + "cand\\cand_8_count_in_file_"+str(wiki_sou_th)+"_"+str(wiki_tar_th)+".txt"
        uf.save_cand_count_in_file_filter_sou_in_file(cand_8, cand_8_file)
        nums_8_file = res_road + "nums\\8_filter_count_in_file_nums_"+str(wiki_sou_th)+"_"+str(wiki_tar_th)+".txt"
        uf.get_nums_for_count_in_file_filter_sou(cand_8, nums_8_file)

        check_8_file = res_road + "check\\check_after_count_in_file_filter_"+str(wiki_sou_th)+"_"+str(wiki_tar_th)+".txt"
        uf.save_cand_check_count_in_file_filter_sou_with_file(cand_8, check_8_file)
    

    '''
    for idx in range(1, 6):
        sou_road = road + str(idx) + "\\sou\\"
        res_road = road + str(idx) + "\\res\\"
        # get final candidate with sentences
        sent_en_file = sou_road + "en_token_1000k_" + str(idx) + ".txt"
        sent_en_list = uf.get_sentences_all_list(sent_en_file)
        sent_de_file = sou_road + "zh_token_1000k_" + str(idx) + ".txt"
        sent_de_list = uf.get_sentences_all_list(sent_de_file)
        
        wiki_sou_th = 15000
        wiki_tar_th = 15000
        cand_7_file = res_road + "cand\\cand_7_before_count_in_file_"+str(wiki_sou_th)+"_"+str(wiki_tar_th)+".txt"
        cand_7 = uf.get_cand_count_in_file_sou_from_file(cand_7_file)
        
        cand_7_final_file = res_road + "final_res\\cand_with_sent_before_count_in_file_"+str(wiki_sou_th)+"_"+str(wiki_tar_th)+".txt"
        uf.save_sent_cand_sou_count_in_file(cand_7, sent_en_list, sent_de_list, cand_7_final_file)

        #cand_8_file = res_road + "cand/cand_8_count_in_file_"+str(wiki_sou_th)+"_"+str(wiki_tar_th)+".txt"
        #cand_8 = uf.get_cand_count_in_file_sou_from_file(cand_8_file)

        #cand_8_final_file = res_road + "final_res/cand_with_sent_after_count_in_file_"+str(wiki_sou_th)+"_"+str(wiki_tar_th)+".txt"
        #uf.save_sent_cand_sou_count_in_file(cand_8, sent_en_list, sent_de_list, cand_8_final_file)
    '''
