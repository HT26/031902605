import sys

# 全局变量用来定位属于word中哪个敏感词
pos = 1

class senwordsget(object):
    """
    DFA算法
    """

    def __init__(self):
        """
        算法初始化
        """
        # 词库
        self.root = dict()
        # 无意义词库,在检测中需要跳过的
        self.skip_root = [' ', '&', '!', '！', '@', '#', '$', '￥', '*', '^', '%', '?', '？', '<', '>', "《", '》', '1', '2',
                          '3', '4', '5', '6', '7', '8', '9', '0', '{', '}', '[', ']', '|', ':', '"', '\'', ',', '_',
                          '+', '(', ')', '~', '`', '·', '（', '）', ';', '.', '/', '-', '——', '=', '…', '“', '”']
        self.word = []
        self.org = []

    def add_word(self, word):
        """
        添加词库
        :param word:
        :return:
        """
        global pos
        now_node = self.root
        word_count = len(word)
        for i in range(word_count):
            char_str = word[i]
            if char_str in now_node.keys():
                # 如果存在该key，直接赋值，用于下一个循环获取
                now_node = now_node.get(word[i])
            else:
                # 不存在则构建一个dict
                new_node = dict()

                if i == word_count - 1:  # 最后一个
                    new_node['is_end'] = pos
                else:  # 不是最后一个
                    new_node['is_end'] = 0

                now_node[char_str] = new_node
                now_node = new_node

    def check_match_word(self, txt, begin_index):
        """
        检查文字中是否包含匹配的字符
        :param txt:待检测的文本
        :param begin_index: 调用getSensitiveWord时输入的参数，获取词语的上边界index
        :return:如果存在，则返回匹配字符的长度和对应word中的位置,不存在返回0
        """
        flag = 0
        match_flag_length = 0  # 匹配字符的长度
        now_map = self.root
        tmp_flag = 0  # 包括特殊字符的敏感词的长度
        i = begin_index
        while i < len(txt):
            word = txt[i]
            # 检测是否是特殊字符"
            if word in self.skip_root and match_flag_length > 0:
                # 保证已经找到这个词的开头之后出现的特殊字符
                tmp_flag += 1
                i += 1
                continue
            # 获取指定key
            now_map = now_map.get(word)
            if now_map:  # 存在，则判断是否为最后一个
                # 找到相应key，匹配标识+1
                match_flag_length += 1
                # 如果为最后一个匹配规则，结束循环，返回匹配标识数
                if now_map.get("is_end"):
                    # 结束标志位
                    flag = now_map.get("is_end")
                    back_tmp_flag = 0
                    # 因为是最大匹配这里找到后还得继续检测
            else:  # 不存在，直接返回
                 break
            i += 1
        total_length = tmp_flag + match_flag_length
        if not flag:
            total_length = 0
        return total_length, flag

    def get_match_word(self, txt):
        """
        获取匹配到的词语
        :param txt:待检测的文本
        :return:文字中的相匹配词和对应到word的位置信息
        """
        matched_word_list = list()
        match_flag = []
        i = 0
        while i < len(txt):  # 0---11
            length, flag = self.check_match_word(txt, i)
            if length > 0:
                word = txt[i:i + length]
                matched_word_list.append(word)
                match_flag.append(flag)
                i = i + length - 1
            i += 1
        return matched_word_list, match_flag

    def input_path(self, word_path='', org_path=''):
        global pos
        if len(word_path) > 0 and len(org_path) > 0:
            io_error(word_path)
            io_error(org_path)
            self.word, self.org = get_word(word_path, org_path)
        for i in self.word:
            self.add_word(i)
            pos += 1

    def output_path(self, ans_path):
        out_ans = []
        total = 0
        for i in range(len(self.org)):
            result, flag = dfa.get_match_word(self.org[i])
            if len(result) > 0:
                for j in range(len(result)):
                    total += 1
                    out_ans.append("Line{}: <{}> {}\n".format(i + 1, self.word[flag[j] - 1], result[j]))
        with open(ans_path, 'w', encoding='utf-8') as f:
            f.write("Total: {}\n".format(total))
        with open(ans_path, 'a', encoding='utf-8') as f:
            f.writelines(out_ans)
        # return out_ans


def get_word(word_path, org_path):
    word = []
    org = []
    with open(word_path, 'r', encoding='UTF-8') as f:
        for i in f.readlines():
            word.append(i.strip('\n'))
    with open(org_path, 'r', encoding='UTF-8') as f:
        for i in f.readlines():
            org.append(i.strip('\n').strip('\u3000') + '$')
    return word, org


def io_error(file):
    try:
        fh = open(file, "r")
    except IOError:
        print("Error: 没有找到文件或读取文件失败")
        exit()
    else:
        fh.close()


if __name__ == "__main__":
    # start = time.time()
    if len(sys.argv) == 1:
        w_path = 'D_words.txt'
        o_path = 'WenZhang.txt'
        a_path = 'keywords.txt'
    elif len(sys.argv) == 4:
        w_path = sys.argv[1]
        o_path = sys.argv[2]
        a_path = sys.argv[3]
    else:
        print("输入路径有误！")
        exit()
    dfa = senwordsget()
    dfa.input_path(w_path, o_path)
    dfa.output_path(a_path)
    # end = time.time()
    # print(end - start)
