# 趣味のPython学習　Project 01-02
# 連想記憶パイソンちゃん
# ばーじょん 0.1.2

# 連想記憶
memory = []

task = True

# コマンド
STORE = "記憶"
FIND  = "確認"
MIND  = "連想"
END   = "終了"

def safe_word(word) :
    word = word.replace("/","")
    word = word.replace(",","")
    return word

def store_word(word,like) :
    for record in memory :
        if record[0] == like :
            record[1].add(word)
            return
    memory.append([like,{word}])

def find_word(word) :
    for record in memory :
        if word in record[1] :
            print(record[0], end=" ")
    print("\n")

def mind_word_one(like) :
    void = set()
    for record in memory :
        if record[0] == like :
            return record[1]
    return void

def mind_word(likes) :
    void = set()
    result = ""
    like = ""
    while len(likes)>0 :
        if likes.find(":") > 0 :
            like = likes[:likes.find(":")]
            likes = likes[likes.find(":")+1:]
        else :
            like = likes
            likes = ""
        query = mind_word_one(like)
        if result =="" :
            result = query
        else :
            result = result & query
    if result == void :
        print("{}")
    else :
        print(result)

def write_memory() :
    with open("kioku.dat", 'w' ,encoding="UTF-8") as file:
        for record in memory :
            for like in record[1] :
                file.write(record[0]+ ":" + like + "\n")

def read_memory() :
    memory.clear()
    with open("kioku.dat",encoding="UTF-8") as file:
        for line, text in enumerate(file,1) :
            like = text[:text.find(":")]
            word = text[text.rfind(":")+1:-1]
            store_word(word,like)

# MAIN

read_memory()

print("*****連想記憶*****")
print("* パイソンちゃん *")
print("******************")
print(STORE + ":名詞：形容詞")
print(FIND  + ":名詞")
print(MIND  + ":形容詞:形容詞...")
print(END)

while task:
    com = input("COMMAND : ")
    com = com.replace("：",":")
    if com.find(":") > 0 :
        cmd = com[:com.find(":")]
        words = com[com.find(":")+1:]
    else :
        cmd = com
        words = ""
    if cmd == MIND :
        mind_word(words)
    elif cmd == FIND :
        find_word(words)
    elif cmd == STORE :
        if words.find(":") > 0 :
            word = words[:words.find(":")]
            like = words[words.find(":")+1:]
            store_word(word,like)
    elif cmd == END :
        task = False

write_memory()