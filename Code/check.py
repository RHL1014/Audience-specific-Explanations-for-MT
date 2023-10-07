import time
from tqdm import tqdm


def get_cand(file_road):
    file = open(file_road, 'r', encoding='utf-8')
    all_cand = file.readlines()
    cand_res = []
    for each_cand in all_cand:
        ele_list = each_cand.strip().split()
        word = ele_list[0]
        sentence_idx = int(ele_list[1])
        word_idx = int(ele_list[2])
        # new_ele = (word, sentence_idx, word_idx)
        cand_res.append(sentence_idx)
    file.close()
    return cand_res


def get_cand_new(file_road):
    file = open(file_road, 'r', encoding='utf-8')
    all_cand = file.readlines()
    cand_res = []
    for each_cand in all_cand:
        num_cand = each_cand.strip()
        sentence_idx = int(num_cand)
        cand_res.append(sentence_idx)
    file.close()
    return cand_res


def get_cand_wiki(wiki_file_road):
    file = open(wiki_file_road, 'r', encoding='utf-8')
    all_cand = file.readlines()
    cand_res = []
    
    for cand in all_cand:
        ele = cand.strip().split()
        sou_word_freq = int(ele[0]) + 1
        sou_word = ele[1]
        tar_word = ele[2]
        sentence_index = int(ele[3])
        word_pair_index = int(ele[4])
        sou_idx_1 = int(ele[5])
        tar_idx_1 = int(ele[6])
        sou_idx_2 = int(ele[7])
        tar_idx_2 = int(ele[8])
        en_freq = int(ele[9])
        de_freq = int(ele[10])
        new_ele = (sou_word, sentence_index, sou_idx_1)
        cand_res.append(new_ele)
    file.close()
    return cand_res


def check_cand(man_sel_res, cand_res):
    check_res = []
    for ele_1 in man_sel_res:
        if ele_1 in cand_res:
            check_res.append(ele_1)
    return check_res


def write_check_res(check_res, file_road):
    file = open(file_road, 'w', encoding='utf-8')
    temp_1_s = set()
    for ele_c in check_res:
        sent_idx_1 = ele_c
        output = str(sent_idx_1) + "\n"
        file.write(output)
        temp_1_s.add(sent_idx_1)
    file.write("\n")
    file.write(str(len(temp_1_s)))
    file.close()
    return len(temp_1_s)


def get_negative_cand(pos_res, cand_res):
    neg_res = []
    for ele in cand_res:
        if ele not in pos_res:
            neg_res.append(ele)
    return neg_res


if __name__ == '__main__':
    sou_th = 15000
    tar_th = 15000
    
    total_num_1 = 0
    total_num_2 = 0
    total_num_3 = 0
    total_num_4 = 0
    total_num_5 = 0
    total_num_6 = 0
    total_num_7 = 0
    total_num_8 = 0
    total_num_9 = 0
    total_num_10 = 0
    
    num_road = "D:\\thesis_data\\cc_Matrix\\en_zh\\total_num_check_desktop\\"
    file_num_name = "num_total" + "_" + str(sou_th) + "_" + str(tar_th)+".txt"
    file_num = open(num_road+file_num_name, 'w', encoding='utf-8')
    for file_index in range(1, 6):
        res_road = "D:\\thesis_data\\cc_Matrix\\en_zh\\" + str(file_index) + "\\res\\"
        check_road = res_road + "check\\"
        sou_man_positive_file = check_road + "sou_man_positive_check_15000_15000.txt"
        cand_man_positive = get_cand_new(sou_man_positive_file)
        temp_1 = set()
        for ele in cand_man_positive:
            sent_idx = ele
            temp_1.add(sent_idx)
        print(str(len(temp_1)))
        sou_before_count_in_file_file = check_road + "check_before_count_in_file_filter_" + str(sou_th) + "_" + str(
            tar_th) + ".txt"
        sou_ner_file_flair = check_road + "check_after_ner_flair_large_" + str(sou_th) + "_" + str(tar_th) + ".txt"
        sou_ner_file_spacy = check_road + "check_after_ner_spacy_large_" + str(sou_th) + "_" + str(tar_th) + ".txt"
        sou_ner_file_stanza = check_road + "check_after_ner_stanza_" + str(sou_th) + "_" + str(tar_th) + ".txt"
        
        sou_both_wiki_title_file = check_road + "check_after_both_wiki_title_flair_large_" + str(sou_th) + "_" + str(
            tar_th) + ".txt"
        sou_para_wiki_title_file = check_road + "check_after_para_wiki_title_flair_large_" + str(sou_th) + "_" + str(
            tar_th) + ".txt"
        sou_not_para_wiki_title_file = check_road + "check_after_not_para_wiki_title_flair_large_" + str(sou_th) + "_" + str(
            tar_th) + ".txt"
        sou_para_wiki_title_same_file = check_road + "check_after_para_wiki_tar_title_same_flair_large_" + str(sou_th) + "_" + str(
            tar_th) + ".txt"
        sou_para_wiki_title_not_same_file = check_road + "check_after_para_wiki_tar_title_not_same_flair_large_" + str(sou_th) + "_" + str(
            tar_th) + ".txt"
        sou_para_wiki_article_size_file = check_road + "check_after_para_wiki_article_size_flair_large_" + str(sou_th) + "_" + str(
            tar_th) + ".txt"
        
        cand_before_count = get_cand_new(sou_before_count_in_file_file)
        cand_ner_flair_han = get_cand(sou_ner_file_flair)
        cand_ner_spacy = get_cand(sou_ner_file_spacy)
        cand_ner_stanza = get_cand(sou_ner_file_stanza)
        cand_both_wiki_title = get_cand_new(sou_both_wiki_title_file)
        cand_para_wiki_title = get_cand_new(sou_para_wiki_title_file)
        cand_not_para_wiki_title = get_cand_new(sou_not_para_wiki_title_file)
        cand_para_wiki_title_same = get_cand_new(sou_para_wiki_title_same_file)
        cand_para_wiki_title_not_same = get_cand_new(sou_para_wiki_title_not_same_file)
        cand_para_wiki_article_size = get_cand_new(sou_para_wiki_article_size_file)

        check_pos_before_count_res = check_cand(cand_man_positive, cand_before_count)
        check_pos_ner_flair_han = check_cand(cand_man_positive, cand_ner_flair_han)
        check_pos_ner_spacy = check_cand(cand_man_positive, cand_ner_spacy)
        check_pos_ner_stanza = check_cand(cand_man_positive, cand_ner_stanza)
        check_pos_both_wiki_title = check_cand(cand_man_positive, cand_both_wiki_title)
        check_pos_para_wiki_title = check_cand(cand_man_positive, cand_para_wiki_title)
        check_pos_not_para_wiki_title = check_cand(cand_man_positive, cand_not_para_wiki_title)
        check_pos_para_wiki_title_same = check_cand(cand_man_positive, cand_para_wiki_title_same)
        check_pos_para_wiki_title_not_same = check_cand(cand_man_positive, cand_para_wiki_title_not_same)
        check_pos_para_wiki_article_size = check_cand(cand_man_positive, cand_para_wiki_article_size)
        
        
        check_pos_before_count_res_file = check_road + "res_check_positive_before_count_" + str(sou_th) + "_" + str(
            tar_th) + ".txt"
        check_pos_ner_flair_file = check_road + "res_check_positive_ner_flair_large_" + str(sou_th) + "_" + str(
            tar_th) + "_after_count.txt"
        check_pos_ner_spacy_file = check_road + "res_check_positive_ner_spacy_large_" + str(sou_th) + "_" + str(
            tar_th) + "_after_count.txt"
        check_pos_ner_stanza_file = check_road + "res_check_positive_ner_stanza_" + str(sou_th) + "_" + str(
            tar_th) + "_after_count.txt"
        
        check_pos_both_wiki_title_flair_file = check_road + "res_check_positive_both_wiki_title_flair_" + str(
            sou_th) + "_" + str(tar_th) + ".txt"
        check_pos_para_wiki_title_flair_file = check_road + "res_check_positive_para_wiki_title_flair_" + str(
            sou_th) + "_" + str(tar_th) + ".txt"
        check_pos_not_para_wiki_title_flair_file = check_road + "res_check_positive_not_para_wiki_title_flair_" + str(
            sou_th) + "_" + str(tar_th) + ".txt"
        check_pos_para_wiki_title_same_flair_file = check_road + "res_check_positive_para_wiki_title_same_flair_" + str(
            sou_th) + "_" + str(tar_th) + ".txt"
        check_pos_para_wiki_title_not_same_flair_file = check_road + "res_check_positive_para_wiki_title_not_same_flair_" + str(
            sou_th) + "_" + str(tar_th) + ".txt"
        check_pos_para_wiki_article_size_flair_file = check_road + "res_check_positive_para_wiki_article_size_flair_" + str(
            sou_th) + "_" + str(tar_th) + ".txt"
        
        num_before = write_check_res(check_pos_before_count_res, check_pos_before_count_res_file)
        num_ner_flair = write_check_res(check_pos_ner_flair_han, check_pos_ner_flair_file)
        num_ner_spacy = write_check_res(check_pos_ner_spacy, check_pos_ner_spacy_file)
        num_ner_stanza = write_check_res(check_pos_ner_stanza, check_pos_ner_stanza_file)
        num_both = write_check_res(check_pos_both_wiki_title, check_pos_both_wiki_title_flair_file)
        num_para = write_check_res(check_pos_para_wiki_title, check_pos_para_wiki_title_flair_file)
        num_not_para = write_check_res(check_pos_not_para_wiki_title, check_pos_not_para_wiki_title_flair_file)
        num_para_same = write_check_res(check_pos_para_wiki_title_same, check_pos_para_wiki_title_same_flair_file)
        num_para_not_same = write_check_res(check_pos_para_wiki_title_not_same, check_pos_para_wiki_title_not_same_flair_file)
        num_para_article_size = write_check_res(check_pos_para_wiki_article_size, check_pos_para_wiki_article_size_flair_file)

        total_num_1 = total_num_1 + num_before
        total_num_2 = total_num_2 + num_ner_flair
        total_num_3 = total_num_3 + num_ner_spacy
        total_num_4 = total_num_4 + num_ner_stanza
        total_num_5 = total_num_5 + num_both
        total_num_6 = total_num_6 + num_para
        total_num_7 = total_num_7 + num_not_para
        total_num_8 = total_num_8 + num_para_same
        total_num_9 = total_num_9 + num_para_not_same
        total_num_10 = total_num_10 + num_para_article_size
        
    file_num.write("total_num_1 before: " + str(total_num_1) + "\n")
    file_num.write("total_num_2 ner_flair_large: " + str(total_num_2) + "\n")
    file_num.write("total_num_3 ner_spacy_large: " + str(total_num_3) + "\n")
    file_num.write("total_num_4 ner_stanza: " + str(total_num_4) + "\n")
    file_num.write("total_num_5 both: " + str(total_num_3) + "\n")
    file_num.write("total_num_6 para: " + str(total_num_4) + "\n")
    file_num.write("total_num_7 not_para: " + str(total_num_5) + "\n")
    file_num.write("total_num_8 para_same: " + str(total_num_6) + "\n")
    file_num.write("total_num_9 para_not_same: " + str(total_num_7) + "\n")
    file_num.write("total_num_10 para_article_size: " + str(total_num_8) + "\n")
    
    file_num.close()
