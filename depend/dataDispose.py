import re
import os
from translate import Translator
import threading
import enchant
import random

thread_list1: list = []
key: int = 0
write_path: str = r""
open_path: str = r""


def start() -> None:
    """
    启动模块
    :return 无返回值:
    """
    while True:
        choose: str = input("加密【1】破译【2】结束【0】： ")
        global key
        if choose == "0":
            return None
        elif choose == "1":
            bridge_str = produceCiphertext()
            if open_path == "" and bridge_str is not None:
                result_str = decode(key, bridge_str)
                print(f"密文为: {result_str}")
                print(f"密钥为: 右移{key}位")
            elif bridge_str is not None:
                writeOutput(key, None, open_path, write_path)
        elif choose == "2":
            bridge_str = dataAccept()
            if bridge_str is not None:
                list_str: list[str]
                key_list: list[int]
                list_str, key_list = decodeBase(bridge_str)
                if not list_str:
                    print("特征文本无法确认是通过凯撒加密后得到的密文。")
                else:
                    key = key_list[0]
                    choice = input("是否翻译成汉语？ 是【1】否【0】：")
                    if choice == "1":
                        if len(list_str) > 1:
                            for tr_cir1 in range(len(list_str)):
                                list_str[tr_cir1] = decode(key, list_str[tr_cir1])
                            treadDispose(list_str)
                            print("特征文本结果有歧义。 ")
                            for result_error in thread_list1:
                                print(result_error)
                        else:
                            if open_path != "":
                                writeChinese(key, None, open_path, write_path)
                            else:
                                writeChinese(key, bridge_str)
                    else:
                        if len(list_str) > 1:
                            for tr_cir1 in range(len(list_str)):
                                list_str[tr_cir1] = decode(key, list_str[tr_cir1])
                            print("特征文本结果有歧义。 ")
                            for result_error in list_str:
                                print(result_error)
                        else:
                            if open_path != "":
                                writeOutput(key, None, open_path, write_path)
                            else:
                                writeOutput(key, bridge_str)
        keep = input("是否继续【1】否【0】：")
        if keep == "0":
            return None
        else:
            print("---"*20)


def dataAccept() -> str | None:
    """
    数据接收
    :return: text_inner
    """
    text_accept = input("请输入需要破译的文本/需要破译文本的路径/结束【0】：")
    if text_accept == "0":
        return None
    if text_accept.find(".txt") != -1:
        global open_path
        if os.path.exists(text_accept):
            open_path = text_accept
        else:
            print("该路径下无该目标文件。 请重新输入")
            return produceCiphertext()
        global write_path
        write_path = input("请输入需要保存文本的绝对路径【不输入密文文本路径】：")
        try:
            with open(write_path, "w", encoding="utf-8"):
                pass
        except FileNotFoundError:
            print("该路径无效。")
            return dataAccept()
        except PermissionError:
            print("该路径程序无权访问。")
            return dataAccept()
        with open(text_accept, "r", encoding="utf-8") as f_check:
            text_ = f_check.read()
            if re.search(r"[\u4e00-\u9fa5]", text_):
                print("该文本包含中文，请重新输入")
                return dataAccept()
        with open(text_accept, "r", encoding="utf-8") as f_get:
            try:
                text_inner = f_get.readline()
                while text_inner:
                    return text_inner
                print("该文本为空。 请重新输入")
                return dataAccept()
            except FileNotFoundError:
                print("该路径下无该文本/该文本无法访问。 请重新输入")
                return dataAccept()
    else:
        text_inner = text_accept
        if re.search(r"[\u4e00-\u9fa5]", text_inner):
            print("该文本包含中文，请重新输入")
            return dataAccept()
        elif text_inner == "":
            print("该文本为空。 请重新输入")
            return dataAccept()
        else:
            return text_inner


def produceCiphertext() -> str | None:
    text_ori = input("请输入需要加密的文本/需要加密文本的路径/结束【0】：")
    if text_ori == "0":
        return None
    global key
    try:
        key = int(input("请输入加密的密钥【1-25】随机【0】："))
    except ValueError:
        print("请输入合法密钥。")
        return produceCiphertext()
    if key == 0:
        key = random.randint(1, 25)
    elif key > 25 or key < 1:
        print("请输入合法密钥。")
        return produceCiphertext()
    if text_ori == "0":
        return None
    if text_ori.find(".txt") != -1:
        global open_path
        if os.path.exists(text_ori):
            open_path = text_ori
        else:
            print("该路径下无该目标文件。 请重新输入")
            return produceCiphertext()
        global write_path
        write_path = input("请输入需要保存文本的绝对路径【不要输入明文文本路径】：")
        try:
            with open(write_path, "w", encoding="utf-8"):
                pass
        except FileNotFoundError:
            print("该路径无效。")
            return produceCiphertext()
        except PermissionError:
            print("该路径程序无权访问。")
            return produceCiphertext()
        with open(text_ori, "r", encoding="utf-8") as f_pc:
            text_ = f_pc.read()
            if re.search(r"[\u4e00-\u9fa5]", text_):
                print("该文本包含中文，请重新输入")
                return produceCiphertext()
        with open(text_ori, "r", encoding="utf-8") as f_get_pc:
            try:
                text_inner = f_get_pc.readline()
                print(text_inner)
                while text_inner:
                    return text_inner
                print("该文本为空。 请重新输入")
                return produceCiphertext()
            except FileNotFoundError:
                print("该路径下无该文本/该文本无法访问。 请重新输入")
                return produceCiphertext()
    else:
        text_inner = text_ori
        if re.search(r"[\u4e00-\u9fa5]", text_inner):
            print("该文本包含中文，请重新输入")
            return produceCiphertext()
        elif text_inner == "":
            print("该文本为空。 请重新输入")
            return produceCiphertext()
        else:
            return text_inner


def treadDispose(text_list: list) -> None:
    """
    多线程处理
    :param text_list:
    :return: None
    """
    lock1 = threading.Lock()
    lock2 = threading.Lock()
    for sign in range(len(text_list)):
        if key != 0:
            break
        if 0 <= sign < 5:
            thread_1 = threading.Thread(target=translationToChinese, args=(text_list[sign], lock1))
            thread_1.start()
        else:
            thread_2 = threading.Thread(target=translationToChinese, args=(text_list[sign], lock2))
            thread_2.start()


def transALine(target_str: str) -> str | None:
    if re.search(r"[\u4e00-\u9fa5]", target_str):
        return print("文本含有汉字无法翻译")
    else:
        translator = Translator(to_lang="zh")
        tr = translator.translate(target_str)
        return tr


def translationToChinese(text_temp: str, lock) -> None:
    """
    数据翻译
    :return None: 无返回值。 结果全部写入thread_list1
    """
    lock.acquire()
    translator = Translator(to_lang="zh")
    tr = translator.translate(text_temp)
    if re.search(r"[A-Za-z]", tr):
        lock.release()
    else:
        global thread_list1
        thread_list1.append(tr)
        lock.release()


def writeChinese(key_result: int, text_w: str = None, path_open: str = None, path_write: str = None) -> None:
    """
    数据写入成汉语
    :param key_result: 破译后的密钥。
    :param path_open: 密文所在的文件路径地址。
    :param path_write: 密文破译后明文所写入的文件路径地址。
    :param text_w: 破译后的文本。
    :return None: 无返回值
    """
    if path_open is None:
        index_tr: int = 0
        tr: list = []
        print("破译结果:", end="")
        translator = Translator(to_lang="zh")
        line_out = decode(key_result, text_w)
        if re.search(r"[.]", line_out):
            for sentence in line_out.strip().split("."):
                if sentence == "":
                    continue
                tr.append(translator.translate(sentence))
                print(tr[index_tr], end="。")
                index_tr += 1
            print(" ")
        else:
            tr_: str = translator.translate(line_out)
            print(tr_, end="\n")
        print(line_out)
    else:
        sen_txt: int = 0
        len_txt: int = 0
        with open(path_write, "a", encoding="utf-8") as w:
            with open(path_open, "r", encoding="utf-8") as f_:
                for line_ in f_:
                    line_ = decode(key_result, line_)
                    for sentence in line_.strip().split("."):
                        if sentence == "":
                            continue
                        tr_ = transALine(sentence)
                        w.write(f"{tr_}。")
                        sen_txt += 1
                        print("已写入第{}句".format(sen_txt))
                    w.write("\n")
                    len_txt += 1
                    print("--已写入第{}段--".format(len_txt))
    print(f"密钥为: 右移{key_result}位")


def writeOutput(key_result: int, text_w: str = None, path_open: str = None, path_write: str = None) -> None:
    """
    数据写入成英语
    :param key_result: 破译后的密钥。
    :param path_open: 密文所在的文件路径地址。
    :param path_write: 密文破译后明文所写入的文件路径地址。
    :param text_w: 破译后的文本。
    :return None: 无法返回值
    """
    if path_open is None:
        result_text = decode(key_result, text_w)
        print("破译结果:", result_text)
    else:
        len_text: int = 0
        with open(path_write, "a", encoding="utf-8") as w:
            with open(path_open, "r", encoding="utf-8") as f_wo:
                for line_w in f_wo:
                    line_w = decode(key_result, line_w)
                    w.write(line_w)
                    len_text += 1
    print(f"密钥为: 右移{key_result}位")


def decodeBase(original_text: str) -> tuple[list[str], list[int]] | None:
    """
    通过特征文本提取密钥。
    :param original_text: 需要破译的密文未处理的特征文本。
    :return tuple[list[str], list[int]] | None: 返回值类型为-> 存有明文 文本 及 密钥 的元组 | 没有返回值？
    """
    original_text = original_text.strip()
    mid_text_ = re.sub(r"[\W\s]+", " ", original_text)
    new_text_ = re.match(r"\b(\w+\s?){1,4}\b", mid_text_)
    if new_text_ is None:
        print("无破译文本")
        return None
    else:
        check_word = enchant.Dict("en_US")
        str_ = new_text_.group()
        str_list: list[str] = []
        key_list: list[int] = []
        for mov_key in range(1, 26):
            str_temp: str = ""
            str_word = ""
            for j in str_:
                if j.isalpha():
                    if 'A' <= j <= "Z" and chr(ord(j) + mov_key) > 'Z':
                        str_temp += chr(ord(j) + mov_key - 26)
                        str_word += chr(ord(j) + mov_key - 26)
                    elif 'a' <= j <= "z" and chr(ord(j) + mov_key) > 'z':
                        str_temp += chr(ord(j) + mov_key - 26)
                        str_word += chr(ord(j) + mov_key - 26)
                    else:
                        str_temp += chr(ord(j) + mov_key)
                        str_word += chr(ord(j) + mov_key)
                else:
                    str_temp += j
                    if check_word.check(str_word):
                        str_word = ""
                    else:
                        str_temp = ""
                        break

            if str_temp != "":
                str_list.append(str_temp)
                key_list.append(mov_key)
        return str_list, key_list


def decode(target_key: int, target_text: str) -> str:
    """
    通过密钥位移文本。
    :param target_key: 密钥。
    :param target_text: 文本。
    :return str: 结果文本。
    """
    str_temp = ""
    for j in target_text:
        if j.isalpha():
            if 'A' <= j <= "Z" and chr(ord(j) + target_key) > 'Z':
                str_temp += chr(ord(j) + target_key - 26)
            elif 'a' <= j <= "z" and chr(ord(j) + target_key) > 'z':
                str_temp += chr(ord(j) + target_key - 26)
            else:
                str_temp += chr(ord(j) + target_key)
        else:
            str_temp += j
    return str_temp


if __name__ == '__main__':
    start()
