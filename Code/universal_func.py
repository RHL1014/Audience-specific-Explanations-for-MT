"This file defines commonly used functions. For example, functions for reading and storing experimental results."

def get_nums_for_1_filter(cand_1: dict, file_road):
    w_file = open(file_road, 'w', encoding='utf-8')
    sent_list_all = set()
    for ele in cand_1.keys():
        (_, sent_idx, _) = ele
        sent_list_all.add(sent_idx)
    w_file.write("total: " + str(len(sent_list_all)) + "\n")
    w_file.close()
    return len(sent_list_all)


def save_cand_1_in_file(cand_1: dict, file_road):
    w_file = open(file_road, 'w', encoding='utf-8')
    for ele in cand_1.keys():
        (word, sent_idx, word_idx) = ele
        word_count = cand_1[ele]
        w_file.write(word + " " + str(sent_idx) + " " + str(word_idx) + " " + str(word_count) + "\n")
    w_file.close()


def get_cand_1_from_file(file_road):
    cand_1 = []
    with open(file_road, 'r', encoding='utf-8') as cand_1_f:
        for line in cand_1_f:
            in_line = line.strip().split()
            word = in_line[0]
            sent_idx = int(in_line[1])
            word_idx = int(in_line[2])
            word_count = int(in_line[3])
            ele = (word, sent_idx, word_idx, word_count)
            cand_1.append(ele)
    return cand_1
   
    
def get_nums_for_alignment_filter_sou(cand_sou, file_road):
    w_file = open(file_road, 'w', encoding='utf-8')
    sent_list_all = set()
    for ele in cand_sou:
        (_, sent_index, _, _, _, _, _, _) = ele
        sent_list_all.add(sent_index)
    w_file.write("total: " + str(len(sent_list_all)) + "\n")
    w_file.close()
    return len(sent_list_all)


def save_cand_alignment_filter_sou_in_file(cand_sou, file_road):
    w_file = open(file_road, 'w', encoding='utf-8')
    for ele in cand_sou:
        (word, sent_index, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, word_count) = ele
        output = word + " " + str(sent_index) + " " + str(align_idx) + " " \
                 + str(word_sou_idx) + " " + str(word_tar_idx) + " " \
                 + str(sou_idx_1) + " " + str(tar_idx_1) + " " \
                 + str(word_count)
        w_file.write(output + "\n")
    w_file.close()


def get_cand_alignment_filter_sou_from_file(file_road):
    cand_2 = []
    with open(file_road, 'r', encoding='utf-8') as cand_1_f:
        for line in cand_1_f:
            in_line = line.strip().split()
            word = in_line[0]
            sent_idx = int(in_line[1])
            align_idx = int(in_line[2])
            word_sou_idx = int(in_line[3])
            word_tar_idx = int(in_line[4])
            sou_idx_1 = int(in_line[5])
            tar_idx_1 = int(in_line[6])
            word_count = int(in_line[7])
            ele = (word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, word_count)
            cand_2.append(ele)
    return cand_2


def get_nums_for_word_filter_sou(cand_sou, file_road):
    w_file = open(file_road, 'w', encoding='utf-8')
    sent_list_all = set()
    for ele in cand_sou:
        (_, _, sent_index, _, _, _, _, _, _, _) = ele
        sent_list_all.add(sent_index)
    w_file.write("total: " + str(len(sent_list_all)) + "\n")
    w_file.close()
    return len(sent_list_all)


def save_cand_word_filter_sou_in_file(cand_sou, file_road):
    w_file = open(file_road, 'w', encoding='utf-8')
    for ele in cand_sou:
        (word, tar_word, sent_index, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, word_count,
         word_tar_count) = ele
        output = word + " " + tar_word + " " \
                 + str(sent_index) + " " + str(align_idx) + " " \
                 + str(word_sou_idx) + " " + str(word_tar_idx) + " " \
                 + str(sou_idx_1) + " " + str(tar_idx_1) + " " \
                 + str(word_count) + " " + str(word_tar_count)
        w_file.write(output + "\n")
    w_file.close()


def get_cand_word_filter_sou_from_file(file_road):
    cand = []
    with open(file_road, 'r', encoding='utf-8') as cand_f:
        for line in cand_f:
            in_line = line.strip().split()
            word = in_line[0]
            tar_word = in_line[1]
            sent_idx = int(in_line[2])
            align_idx = int(in_line[3])
            word_sou_idx = int(in_line[4])
            word_tar_idx = int(in_line[5])
            sou_idx_1 = int(in_line[6])
            tar_idx_1 = int(in_line[7])
            word_count = int(in_line[8])
            word_tar_count = int(in_line[9])
            ele = (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, word_count,
                   word_tar_count)
            cand.append(ele)
    return cand


def save_cand_check_count_in_file_filter_sou_with_file(cand_sou, file_road):
    w_file = open(file_road, 'w', encoding='utf-8')
    for ele in cand_sou:
        (word, tar_word, sent_index, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, word_count,
         word_tar_count, sou_count_in_file, tar_count_in_file) = ele
        #output = word + " " + str(sent_index) + " " +  str(word_sou_idx)
        w_file.write(str(sent_index) + "\n")
    w_file.close()


def save_cand_check_wiki_filter_sou_without_file(cand_sou, file_road):
    w_file = open(file_road, 'w', encoding='utf-8')
    for ele in cand_sou:
        (word, tar_word, sent_index, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, wiki_sou_count,
         wiki_tar_count) = ele
        output = word + " " + str(sent_index) + " " +  str(word_sou_idx)
        w_file.write(output + "\n")
    w_file.close()


def get_nums_for_count_in_file_filter_sou(cand_sou, file_road):
    w_file = open(file_road, 'w', encoding='utf-8')
    sent_list_all = set()
    for ele in cand_sou:
        (_, _, sent_index, _, _, _, _, _, _, _, _, _) = ele
        sent_list_all.add(sent_index)
    w_file.write("total: " + str(len(sent_list_all)) + "\n")
    w_file.close()


def save_cand_count_in_file_filter_sou_in_file(cand_sou, file_road):
    w_file = open(file_road, 'w', encoding='utf-8')
    for ele in cand_sou:
        (word, tar_word, sent_index, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, wiki_sou_count,
         wiki_tar_count, word_sou_count, word_tar_count) = ele
        output = word + " " + tar_word + " " \
                 + str(sent_index) + " " + str(align_idx) + " " \
                 + str(word_sou_idx) + " " + str(word_tar_idx) + " " \
                 + str(sou_idx_1) + " " + str(tar_idx_1) + " " \
                 + str(wiki_sou_count) + " " + str(wiki_tar_count) + " " \
                 + str(word_sou_count) + " " + str(word_tar_count)
        w_file.write(output + "\n")
    w_file.close()


def get_cand_count_in_file_sou_from_file(file_road):
    cand = []
    with open(file_road, 'r', encoding='utf-8') as cand_f:
        for line in cand_f:
            in_line = line.strip().split()
            word = in_line[0]
            tar_word = in_line[1]
            sent_idx = int(in_line[2])
            align_idx = int(in_line[3])
            word_sou_idx = int(in_line[4])
            word_tar_idx = int(in_line[5])
            sou_idx_1 = int(in_line[6])
            tar_idx_1 = int(in_line[7])
            wiki_sou_count = int(in_line[8])
            wiki_tar_count = int(in_line[9])
            word_count = int(in_line[10])
            word_tar_count = int(in_line[11])
            ele = (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1,
                   wiki_sou_count, wiki_tar_count, word_count, word_tar_count)
            cand.append(ele)
    return cand


def get_sentences_all_list(file_sentence):
    sent_list = []
    with open(file_sentence, 'r', encoding='utf-8') as f_sent:
        for line in f_sent:
            sentence = line.strip()
            sent_list.append(sentence)
    return sent_list


def save_sent_cand_sou_count_in_file(wiki_cand, sent_en_list, sent_de_list, file_out):
    with open(file_out, 'w', encoding='utf-8') as f_out:
        for cand in wiki_cand:
            (word, tar_word, sentence_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_2, tar_idx_2,
             sou_wiki_freq, tar_wiki_freq, sou_word_freq, tar_word_freq) = cand
            sent_en = sent_en_list[sentence_idx].strip()
            sent_de = sent_de_list[sentence_idx].strip()
            sent = sent_en + " ||| " + sent_de
            output = word + " " + tar_word + " | " \
                     + "w_freq: " + str(sou_word_freq) + " - " + str(tar_word_freq) + " | " \
                     + "wiki_freq: " + str(sou_wiki_freq) + " - " + str(tar_wiki_freq) + " | " \
                     + "sentence_idx: " + str(sentence_idx) + " | " \
                     + "align_1: " + str(word_sou_idx) + "-" + str(word_tar_idx) + " | " \
                     + "align_2: " + str(sou_idx_2) + "-" + str(tar_idx_2) + " | " \
                     + "   " + sent + " \n"
            f_out.write(output + "\n")


def get_nums_for_ner_filter_sou(cand_sou, file_road):
    w_file = open(file_road, 'w', encoding='utf-8')
    sent_list_all = set()
    for ele in cand_sou:
        (_, _, sent_index, _, _, _, _, _, _, _, _, _, _, _) = ele
        sent_list_all.add(sent_index)
    w_file.write("total: " + str(len(sent_list_all))+"\n")
    w_file.close()
    return len(sent_list_all)


def save_cand_ner_sou_in_file(cand_sou, file_road):
    w_file = open(file_road, 'w', encoding='utf-8')
    for ele in cand_sou:
        (word, tar_word, sent_index, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, wiki_sou_count, wiki_tar_count, word_sou_count, word_tar_count, entity_sou, entity_tar) = ele
        output = word + " " + tar_word + " " \
                 + str(sent_index) + " " + str(align_idx) + " " \
                 + str(word_sou_idx) + " " + str(word_tar_idx) + " " \
                 + str(sou_idx_1) + " " + str(tar_idx_1) + " " \
                 + str(wiki_sou_count) + " " + str(wiki_tar_count) + " " \
                 + str(word_sou_count) + " " + str(word_tar_count) + "|||||" \
                 + str(entity_sou) + "|||" + str(entity_tar)
        w_file.write(output+"\n")
    w_file.close()


def get_cand_ner_sou_from_file(file_road):
    cand = []
    with open(file_road, 'r', encoding='utf-8') as cand_f:
        for line in cand_f:
            in_line = line.strip().split("|||||")
            in_line_1 = in_line[0].strip().split()
            in_line_2 = in_line[1].strip().split("|||")
            word = in_line_1[0]
            tar_word = in_line_1[1]
            sent_idx = int(in_line_1[2])
            align_idx = int(in_line_1[3])
            word_sou_idx = int(in_line_1[4])
            word_tar_idx = int(in_line_1[5])
            sou_idx_1 = int(in_line_1[6])
            tar_idx_1 = int(in_line_1[7])
            wiki_sou_count = int(in_line_1[8])
            wiki_tar_count = int(in_line_1[9])
            word_count = int(in_line_1[10])
            word_tar_count = int(in_line_1[11])
            entity_sou = in_line_2[0]
            entity_tar = in_line_2[1]
            ele = (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, wiki_sou_count, wiki_tar_count, word_count, word_tar_count, entity_sou, entity_tar)
            cand.append(ele)
    return cand


def get_nums_for_wiki_title_filter_sou(cand_sou, file_road):
    w_file = open(file_road, 'w', encoding='utf-8')
    sent_list_all = set()
    for ele in cand_sou:
        (_, _, sent_index, _, _, _, _, _, _, _, _, _, _, _) = ele
        sent_list_all.add(sent_index)
    w_file.write("total: " + str(len(sent_list_all)) + "\n")
    w_file.close()
    return len(sent_list_all)


def save_cand_check_wiki_title_filter_sou(cand_sou, file_road):
    w_file = open(file_road, 'w', encoding='utf-8')
    for ele in cand_sou:
        (word, tar_word, sent_index, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, wiki_sou_count,
         wiki_tar_count, word_sou_count, word_tar_count, entity_sou, entity_tar) = ele
        output = str(sent_index)
        w_file.write(output + "\n")
    w_file.close()


def save_sent_cand_sou_wiki_title(wiki_cand, sent_en_list, sent_de_list, file_out):
    with open(file_out, 'w', encoding='utf-8') as f_out:
        for cand in wiki_cand:
            (word, tar_word, sentence_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1,
             sou_wiki_freq, tar_wiki_freq, sou_word_freq, tar_word_freq, entity_sou, entity_tar) = cand
            sent_en = sent_en_list[sentence_idx].strip()
            sent_de = sent_de_list[sentence_idx].strip()
            sent = sent_en + " ||| " + sent_de
            output = word + " " + tar_word + " | " \
                     + "w_freq: " + str(sou_word_freq) + " - " + str(tar_word_freq) + " | " \
                     + "wiki_freq: " + str(sou_wiki_freq) + " - " + str(tar_wiki_freq) + " | " \
                     + "sentence_idx: " + str(sentence_idx) + " | " \
                     + "align_1: " + str(word_sou_idx) + "-" + str(word_tar_idx) + " | " \
                     + "align_2: " + str(sou_idx_1) + "-" + str(tar_idx_1) + " | " \
                     + "entity: " + entity_sou + " - " + entity_tar + " | " \
                     + "   " + sent + " \n"
            f_out.write(output + "\n")


def save_cand_wiki_title_sou_in_file(cand_sou, file_road):
    w_file = open(file_road, 'w', encoding='utf-8')
    for ele in cand_sou:
        (word, tar_word, sent_index, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, wiki_sou_count,
         wiki_tar_count, word_sou_count, word_tar_count, entity_sou, entity_tar) = ele
        output = word + " " + tar_word + " " \
                 + str(sent_index) + " " + str(align_idx) + " " \
                 + str(word_sou_idx) + " " + str(word_tar_idx) + " " \
                 + str(sou_idx_1) + " " + str(tar_idx_1) + " " \
                 + str(wiki_sou_count) + " " + str(wiki_tar_count) + " " \
                 + str(word_sou_count) + " " + str(word_tar_count) + "|||||" \
                 + str(entity_sou) + "|||" + str(entity_tar)
        w_file.write(output + "\n")
    w_file.close()
    
    
    


def save_sent_cand_sou_ner(ner_cand, sent_sou_list, sent_tar_list, file_out):
    with open(file_out, 'w', encoding='utf-8') as f_out:
        for cand in ner_cand:
            (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_2, tar_idx_2, sou_wiki_freq, tar_wiki_freq, sou_word_freq, tar_word_freq,ent_sou, ent_tar) = cand
            sent_sou = sent_sou_list[sent_idx].strip()
            sent_tar = sent_tar_list[sent_idx].strip()
            sent = sent_sou + " ||| " + sent_tar
            output = word + " " + tar_word + " | " \
                     + "w_freq: " + str(sou_word_freq) + " - " + str(tar_word_freq) + " | " \
                     + "wiki_freq: " + str(sou_wiki_freq) + " - " + str(tar_wiki_freq) + " | " \
                     + "sentence_idx: " +str(sent_idx) + " | " \
                     + "align_1: " + str(word_sou_idx) + "-" +str(word_tar_idx) + " | " \
                     + "align_2: " + str(sou_idx_2) + "-" + str(tar_idx_2) + " | " \
                     + "ner_entity: " + ent_sou + "-" + ent_tar + " | " \
                     + "   " + sent + "\n"
            f_out.write(output + "\n")


def save_cand_check_ner_filter_sou(cand_sou, file_road):
    w_file = open(file_road, 'w', encoding='utf-8')
    for ele in cand_sou:
        (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, word_count, word_tar_count, sou_count_in_file, tar_count_in_file, ent_sou, ent_tar) = ele
        output = word + " " + str(sent_idx) + " " +str(word_sou_idx)
        w_file.write(output + "\n")
    w_file.close()



def save_cand_for_word_process_sou(cand, file_road, threshold_num, min_distance, max_distance):
    w_file = open(file_road, 'w', encoding='utf-8')
    for th_num in range(threshold_num):
        cand_sep = cand[th_num]
        for dist in range(min_distance, max_distance + 1):
            cand_each_dis = cand_sep[dist]
            for (word, sent_index, word_pair_index, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1) in cand_each_dis:
                output = str(th_num+1) + " " + word + " " + str(sent_index) + " " + str(word_pair_index) \
                         + " " + str(word_sou_idx) + " " + str(word_tar_idx) \
                         + " " + str(sou_idx_1) + " " + str(tar_idx_1) + "\n"
                w_file.write(output)
    w_file.close()


def save_cand_for_word_process_tar(cand, file_road, threshold_num, min_distance, max_distance):
    w_file = open(file_road, 'w', encoding='utf-8')
    for th_num in range(threshold_num):
        cand_sep = cand[th_num]
        for dist in range(min_distance, max_distance + 1):
            cand_each_dis = cand_sep[dist]
            for (word, sent_index, word_pair_index, word_tar_idx, word_sou_idx, tar_idx_1, sou_idx_1) in cand_each_dis:
                output = str(th_num+1) + " " + word + " " + str(sent_index) + " " + str(word_pair_index) \
                         + " " + str(word_tar_idx) + " " + str(word_sou_idx) \
                         + " " + str(tar_idx_1) + " " + str(sou_idx_1) + "\n"
                w_file.write(output)
    w_file.close()


def get_nums_for_filter(cand, file_road, threshold_num):
    w_file = open(file_road, 'w', encoding='utf-8')
    sent_list_all = set()
    for th_num in range(threshold_num):
        cand_sep = cand[th_num]
        sent_list = set()
        sent_list.clear()
        for (_, sent_idx, _, _, _, _, _, _) in cand_sep:
            sent_list.add(sent_idx)
            sent_list_all.add(sent_idx)
        nums_cand_sep = len(sent_list)
        w_file.write("word frequency " + str(th_num + 1) + ": " + str(nums_cand_sep) + "\n")
    w_file.write("total: " + str(len(sent_list_all)) + "\n")
    w_file.close()


def save_cand_for_wiki_process_sou(cand, file_road, threshold_num, tar_word_res):
    w_file = open(file_road, 'w', encoding='utf-8')
    for th_num in range(threshold_num):
        cand_sep = cand[th_num]
        for (word, sent_index, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, tar_freq) in cand_sep:
            tar_word = tar_word_res[sent_index][word_tar_idx]
            output = str(th_num+1) + " " +str(tar_freq) + " " \
                     + word + " " + tar_word + " " \
                     + str(sent_index) + " " + str(align_idx) + " " \
                     + str(word_sou_idx) + " " + str(word_tar_idx) + " " \
                     + str(sou_idx_1) + " " + str(tar_idx_1) + "\n"
            w_file.write(output)
    w_file.close()

def save_cand_for_wiki_process_tar(cand, file_road, threshold_num, sou_word_res):
    w_file = open(file_road, 'w', encoding='utf-8')
    for th_num in range(threshold_num):
        cand_sep = cand[th_num]
        for (word, sent_index, align_idx, word_tar_idx, word_sou_idx, tar_idx_1, sou_idx_1, sou_freq) in cand_sep:
            sou_word = sou_word_res[sent_index][word_sou_idx]
            output = str(th_num+1) + " " +str(sou_freq) + " " \
                     + word + " " + sou_word + " " \
                     + str(sent_index) + " " + str(align_idx) + " " \
                     + str(word_tar_idx) + " " + str(word_sou_idx) + " " \
                     + str(tar_idx_1) + " " + str(sou_idx_1) + "\n"
            w_file.write(output)
    w_file.close()


def get_nums_for_filter(cand, file_road, threshold_num):
    w_file = open(file_road, 'w', encoding='utf-8')
    sent_list_all = set()
    for th_num in range(threshold_num):
        cand_sep = cand[th_num]
        sent_list = set()
        sent_list.clear()
        for (_, _, sent_idx, _, _, _, _, _, _, _, _, _) in cand_sep:
            sent_list.add(sent_idx)
            sent_list_all.add(sent_idx)
        nums_cand_sep = len(sent_list)
        w_file.write("word frequency " + str(th_num + 1) + ": " + str(nums_cand_sep) + "\n")
    w_file.write("total: " + str(len(sent_list_all)) + "\n")
    w_file.close()


def save_cand_for_ner_process_sou(cand, file_road, threshold_num):
    w_file = open(file_road, 'w', encoding='utf-8')
    for th_num in range(threshold_num):
        cand_sep = cand[th_num]
        for ele in cand_sep:
            (word, tar_word, sent_index, align_index, sou_idx_1, tar_idx_1, sou_idx_2, tar_idx_2,
             sou_word_freq, tar_word_freq, en_freq, de_freq) = ele
            output = word + " " + tar_word + " " + str(sent_index) + " " + str(align_index) + " " \
                     + str(sou_idx_1) + " " + str(tar_idx_1) + " " + str(sou_idx_2) + " " + str(tar_idx_2) + " " \
                     + str(sou_word_freq) + " " + str(tar_word_freq) + " " + str(en_freq) + " " + str(de_freq) + "\n"
            w_file.write(output)
    w_file.close()


def save_cand_for_ner_process_tar(cand, file_road, threshold_num):
    w_file = open(file_road, 'w', encoding='utf-8')
    for th_num in range(threshold_num):
        cand_sep = cand[th_num]
        for ele in cand_sep:
            (word, sou_word, sent_index, align_index, tar_idx_1, sou_idx_1, tar_idx_2, sou_idx_2,
             tar_word_freq, sou_word_freq, de_freq, en_freq) = ele
            output = word + " " + sou_word + " " + str(sent_index) + " " + str(align_index) + " " \
                     + str(tar_idx_1) + " " + str(sou_idx_1) + " " + str(tar_idx_2) + " " + str(sou_idx_2) + " " \
                     + str(tar_word_freq) + " " + str(sou_word_freq) + " " + str(de_freq) + " " + str(en_freq) + "\n"
            w_file.write(output)
    w_file.close()


def save_cand_for_check_sou(cand, file_road, threshold_num):
    w_file = open(file_road, 'w', encoding='utf-8')
    for th_num in range(threshold_num):
        cand_sep = cand[th_num]
        for ele in cand_sep:
            (word, tar_word, sent_index, align_index, sou_idx_1, tar_idx_1, sou_idx_2, tar_idx_2,
             sou_word_freq, tar_word_freq, en_freq, de_freq) = ele
            output = word + " " + " " + str(sent_index) + " " + str(sou_idx_1) + "\n"
            w_file.write(output)
    w_file.close()


def save_cand_for_check_tar(cand, file_road, threshold_num):
    w_file = open(file_road, 'w', encoding='utf-8')
    for th_num in range(threshold_num):
        cand_sep = cand[th_num]
        for ele in cand_sep:
            (word, sou_word, sent_index, align_index, tar_idx_1, sou_idx_1, tar_idx_2, sou_idx_2,
             tar_word_freq, sou_word_freq, de_freq, en_freq) = ele
            output = word + " " + str(sent_index) + " " + str(tar_idx_1) + "\n"
            w_file.write(output)
    w_file.close()


def save_cand_for_final_sou(cand, file_road, threshold_num):
    w_file = open(file_road, 'w', encoding='utf-8')
    for th_num in range(threshold_num):
        cand_sep = cand[th_num]
        for ele in cand_sep:
            (word, tar_word, sent_index, align_index, sou_idx_1, tar_idx_1, sou_idx_2, tar_idx_2,
             sou_word_freq, tar_word_freq, en_freq, de_freq) = ele
            output = word + " " + tar_word + " " + str(sent_index) + " " + str(align_index) + " " \
                     + str(sou_idx_1) + " " + str(tar_idx_1) + " " + str(sou_idx_2) + " " + str(tar_idx_2) + " " \
                     + str(sou_word_freq) + " " + str(tar_word_freq) + " " + str(en_freq) + " " + str(de_freq) + "\n"
            w_file.write(output)
    w_file.close()


def save_cand_for_final_tar(cand, file_road, threshold_num):
    w_file = open(file_road, 'w', encoding='utf-8')
    for th_num in range(threshold_num):
        cand_sep = cand[th_num]
        for ele in cand_sep:
            (word, sou_word, sent_index, align_index, tar_idx_1, sou_idx_1, tar_idx_2, sou_idx_2,
             tar_word_freq, sou_word_freq, de_freq, en_freq) = ele
            output = word + " " + sou_word + " " + str(sent_index) + " " + str(align_index) + " " \
                     + str(tar_idx_1) + " " + str(sou_idx_1) + " " + str(tar_idx_2) + " " + str(sou_idx_2) + " " \
                     + str(tar_word_freq) + " " + str(sou_word_freq) + " " + str(de_freq) + " " + str(en_freq) + "\n"
            w_file.write(output)
    w_file.close()


def get_f1_score(total_nums: list[int], total_pos_nums: list[int], find_nums: list[int], find_pos_nums: list[int]):
    res_f1 = []
    for total_n, total_pos_n, find_n, find_pos_n in zip(total_nums, total_pos_nums, find_nums, find_pos_nums):
        total_n_float = float(total_n)
        total_pos_n_float = float(total_pos_n)
        find_n_float = float(find_n)
        find_pos_n_float = float(find_pos_n)
        tp = find_pos_n_float
        fp = find_n_float - find_pos_n_float
        fn = total_pos_n_float - find_pos_n_float
        tn = total_n_float - find_n_float - fn
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1 = 2 * precision * recall/(precision + recall)
        res_f1.append(f1)
    return res_f1
    

def get_sum(nums_list:list[int]):
    return sum(nums_list)

