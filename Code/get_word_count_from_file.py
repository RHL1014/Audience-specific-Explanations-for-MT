from tqdm import tqdm


def get_word_list(input_file, nums_sent):
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


def get_word_count_dict(word_list_res, nums_sent):
    count_dict = {}
    print("get word count begin...\n")
    with tqdm(total=nums_sent) as pbar:
        for line in word_list_res:
            for word in line:
                if word in count_dict:
                    old_count = count_dict[word]
                    new_count = old_count + 1
                    count_dict[word] = new_count
                else:
                    count_dict[word] = 1
            pbar.update(1)
    print("get word count finish...\n")
    return count_dict


def get_word_count_dict_from_file(input_file, nums_sent):
    count_dict = {}
    print("get word count begin...\n")
    with open(input_file, 'r', encoding='utf-8') as word_file:
        with tqdm(total=nums_sent) as pbar:
            for sent in word_file:
                words = sent.strip().split()
                for word in words:
                    if word in count_dict:
                        old_count = count_dict[word]
                        new_count = old_count + 1
                        count_dict[word] = new_count
                    else:
                        count_dict[word] = 1
                pbar.update(1)
    print("get word count finish...\n")
    return count_dict


def save_word_count_to_file(word_count_dict, output_file):
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
    output_f = open(output_file, 'w', encoding='utf-8')
    for (word, count) in words_count_dict_sorted:
        output_one = word + " " + str(count) + "\n"
        output_f.write(output_one)
    output_f.close()
    print("save the dictionary finished!\n")
    

if __name__ == '__main__':
    road = "D:\\thesis_data\\cc_Matrix\\en_fr\\1\\sou\\"
    res_road = "D:\\thesis_data\\cc_Matrix\\en_fr\\1\\res\\"
    file_in = road + "fr_token_1000k_1.txt"
    file_out = res_road + "word_count\\fr_word_count.txt"
    nums_sent = 1000000
    word_count_dict = get_word_count_dict_from_file(file_in, nums_sent)
    save_word_count_to_file(word_count_dict, file_out)
    '''
    for idx in range(1, 6):
        sou_road = road + str(idx) + "/sou/"
        res_road = road + str(idx) + "/res/"
        nums_sent_total = 1000000
        file_in = sou_road + "en_token_1000k_" + str(idx) + ".txt"
        file_out = res_road + "word_count/" + "en_word_count.txt"
        word_count_dict = get_word_count_dict_from_file(file_in, nums_sent_total)
        save_word_count_to_file(word_count_dict, file_out)
        
        file_in = sou_road + "de_token_1000k_" + str(idx) + ".txt"
        file_out = res_road + "word_count/" + "de_word_count.txt"
        word_count_dict = get_word_count_dict_from_file(file_in, nums_sent_total)
        save_word_count_to_file(word_count_dict, file_out)
    '''
