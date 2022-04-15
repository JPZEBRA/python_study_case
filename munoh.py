# 趣味のPython学習　Project 01-01
# しりとりゲーム：人工無能パイソンちゃん
# ばーじょん 0.2

# 単語記憶
memory = []

# 設定
ME = "パイソンちゃん"
YOU = "あなた"

# パス
PASS_MAX = 3
pass_me  = 0
pass_you = 0

# しりとり
last_letter = ""

# 会話中
speaking = True
counter = 0

def speak(who,message) :
    print(who + " : " + message)
    return

def find_word(word) :
    for record in memory :
        if record[0]==word :
            return record[2]
    return -1

def count_word(word) :
    rcd = ""
    ct1 = 1
    ct2 = 1
    for record in memory :
        if record[0]==word :
            rcd = record
            ct1 = record[1] + 1
            ct2 = record[2] + 1
    if rcd!="" :
        memory.remove(rcd)
    memory.append((word,ct1,ct2))
    return

def reply_word(letter) : 
    for record in memory :
        if record[0][0] == letter and record[2] == 0 :
            if end_word(record[0]) == False or counter % 7 == 5 :
                return record[0]
    return ""

def end_word(word) :
    last_letter = word[-1]
    if last_letter == "ん" or last_letter == "ン" :
        return True
    return False

def list_up_words() :
    print("***** 覚えた言葉 *****")
    for record in memory :
        print(record[0] + " ( " + str(record[1]) + " ) " )
    return

def write_memory() :
    with open("munoh.dat", 'w' ,encoding="UTF-8") as file:
        for record in memory :
            file.write(record[0]+ "/" + str(record[1])+"\n")

def read_memory() :
    memory.clear()
    with open("munoh.dat",encoding="UTF-8") as file:
        for line, text in enumerate(file,1) :
            word = text[:text.find("/")]
            cnt = int(text[text.rfind("/")+1:])
            memory.append((word,cnt,0))

# メイン
read_memory()

while speaking :
    pass_me = 0
    pass_you = 0
    last_letter = ""
    speak(ME,"ねえ！しりとりしようよ？")
    speak(ME,"パス(PASS)は" + str(PASS_MAX) + "回まで！")
    speak(ME,"私は" + str(len(memory)) + "の言葉を覚えたよ！")
    speak(ME,"あなたからどうぞ？")
    game = True
    while game :
        # あなた
        while True :
            word = input(YOU+":")
            if(len(word)>0) :
                if word=="PASS" :
                    pass_you += 1
                    speak(ME,"あなたのパスは" + str(pass_you) + "回目です。")
                    if pass_you > PASS_MAX :
                        speak(ME,"あなたの負け！")
                        game = False
                    break
                else :
                    if find_word(word)>0 :
                        speak(ME,"それはもう出たの！")
                    else :
                        if last_letter != "" :
                            if word[0] != last_letter :
                                speak(ME,"それはつながらないの！")
                            else :
                                break
                        else :
                            break

        count_word(word)
        last_letter = word[-1]
        if end_word(word) :
            speak(ME,"あなたの負け！")
            game = False
            break
        # COMP
        counter += 1
        word = reply_word(last_letter)
        if word == "" :
            pass_me += 1
            speak(ME,"わたしのパスは" + str(pass_me) + "回目です。")
            if pass_me > PASS_MAX :
                speak(ME,"わたしの負け！")
                game = False
        else :
            print(ME,word)
            count_word(word)
            last_letter = word[-1]
            if end_word(word) :
                speak(ME,"あっ負けちゃった！")
                game = False
                break
    # 終了確認
    query = input("終わる？(Y)")
    if query == "Y" or query =="y" or query == "Ｙ" or query =="ｙ" :
        list_up_words()
        print("*************************************************")
        speak(ME,"またね！")
        word = input(" ANY KEY ")
        speaking = False
    # 発言回数クリア
    old_mem = memory.copy()
    memory = []
    for record in old_mem :
        memory.append((record[0],record[1],0))
    # SAVE
    write_memory()
