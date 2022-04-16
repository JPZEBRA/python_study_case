# 趣味のPython学習　Project 01-02
# 連想記憶パイソンちゃん
# ばーじょん 0.1.1

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
     result = ""
     while len(likes)>0 :
         like = likes[:likes.find("/")]
         if len(like) <= 0 :
             like = likes
             likes = ""
         else :
             likes = likes[likes.find("/")+1:]
         query = mind_word_one(like)
         if result =="" :
             result = query
         else :
             result = result & query
     print(result)

while task:
    com = input("COMMAND : ")
    com = com.replace("／","/")
    cmd = com[:com.find("/")]
    words = com[com.find("/")+1:]
    if len(cmd)<=0 :
        cmd = com
    if cmd == MIND :
        mind_word(words)
    elif cmd == FIND :
        find_word(words)
    elif cmd == STORE :
        word = words[:words.find("/")]
        like = words[words.find("/")+1:]
        store_word(word,like)
    elif cmd == END :
        task = False