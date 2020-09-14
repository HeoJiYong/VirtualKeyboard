'''
한글조합
수정날짜 2020.05.22 16:11
제작 : hjy
버전 : 1.0
'''


class HangulCombination:
    def __init__(self):
        self.firstKoreanList = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ','ㅅ',
                                'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
        self.secondKoreanList = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ',
                                 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ',
                                 'ㅣ']
        self.thirdKoreanList = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ',
                                'ㄻ','ㄼ', 'ㄽ', 'ㄾ', 'ㄿ','ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
                                'ㅆ','ㅇ','ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
        #겹자음
        self.overlapConsonants={'ㄱ':[['ㅅ'],['ㄳ']],
                            'ㄴ':[['ㅈ','ㅎ'],['ㄵ','ㄶ']],
                            'ㄹ':[['ㄱ','ㅁ','ㅂ','ㅅ','ㅌ','ㅍ','ㅎ'],['ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ']],
                            'ㅂ':[['ㅅ'],['ㅄ']]}
        #겹모음
        self.overlapVowels ={"ㅗ":[['ㅏ','ㅐ','ㅣ'],['ㅘ','ㅙ','ㅚ']],
                             "ㅜ":[['ㅓ','ㅔ','ㅣ'],['ㅝ','ㅞ','ㅟ']],
                             "ㅡ":[['ㅣ'],['ㅢ']]}
        '''각 성 별 베이스코드'''
        self.firstNum=0x1100    #초성 기본코드
        self.secondNum=0x1161   #중성 기본코드
        self.thirdNum=0x11A7    #종성 기본코드
        self.base=0xAC00        #글자 기본코드

        self.firstKoreanUnicode = [i for i in range(self.firstNum,self.firstNum+19)]
        self.secondKoreanUnicode = [i for i in range(self.secondNum,self.secondNum+21)]
        self.thirdKoreanUnicode = [i for i in range(self.thirdNum,self.thirdNum+28)]
        pass

    '''[기존문장] 과 [입력된 글자] 를 자연스럽게 이어주는 함수.(이 함수가 인터페이스 역할)'''
    def smoothString(self,sentence, inputWord):
        print("sentence : ",type(sentence),", inputWord : ",type(inputWord))
        msg = sentence
        if len(sentence) > 0:
            msg = msg[:-1]
            #msg = sentence.rstrip(sentence[-1])
            msg += self.addString(sentence[-1], inputWord)
        else:
            msg += msg+inputWord
        return msg
        pass

    '''초성 중성 종성 -> 글자로 조합한다 (인자는 unicode, 반환은 char(=str))'''
    def unicodesToWord(self,first,second,third):
        firstIdx = 0
        secondIdx = 0
        thirdIdx=0
        firstIdx = self.firstKoreanUnicode.index(first)
        secondIdx = self.secondKoreanUnicode.index(second)
        thirdIdx = self.thirdKoreanUnicode.index(third)

        word = (firstIdx*21*28) + (secondIdx*28) + (thirdIdx) + self.base
        return chr(word)
        pass

    '''글자 하나를 초성 중성 종성 으로 분리해 unicode 3개로 반환'''
    def wordToUnicodes(self,word):
        unicode = ord(word) - self.base
        #first = ((unicode-(unicode%28)/28)/21) + self.firstNum
        #second = ((unicode-(unicode%28)/28)%21) + self.secondNum
        #third = (unicode%28)+ self.thirdNum
        first = (unicode/28)/21
        second = (unicode/28)%21
        third = (unicode%28)

        first = self.firstKoreanUnicode[int(first)]
        second = self.secondKoreanUnicode[int(second)]
        third = self.thirdKoreanUnicode[int(third)]
        return int(first), int(second), int(third)
        pass

    '''각 유니코드를 각 문자로 바꿔준다.'''
    def unicodesToChars(self,first,second,third):
        #해당 함수는 '가'(0xAC00) 이상의 글자가 들어올때만 호출한다.
        #유니코드에 해당하는 유니코드 리스트의 인덱스를 구한다
        #그 인덱스에 맞는 글자 리스트의 값을 반환한다. -> 결론적으로 char 형식의 문자가 반환

        firstUnicodeIdx = self.firstKoreanUnicode.index(first)
        secondUnicodeIdx = self.secondKoreanUnicode.index(second)
        thirdUnicodeIdx = self.thirdKoreanUnicode.index(third)

        firstWord = self.firstKoreanList[firstUnicodeIdx]
        secondWord = self.secondKoreanList[secondUnicodeIdx]
        thirdWord = self.thirdKoreanList[thirdUnicodeIdx]

        return firstWord,secondWord,thirdWord
        pass

    '''받은 겹자음을 부모,자식으로 반환한다 ㄵ -> ㄴ,ㅈ 로 반환'''
    def getOverlapFamily(self,overlapWord):
        for a in self.overlapConsonants.keys():
            for i in range(0,len(self.overlapConsonants[a][1])):
                if self.overlapConsonants[a][1][i] == overlapWord:
                    print("a : ",a,", Consonants : ",self.overlapConsonants[a][0][i])
                    return a, self.overlapConsonants[a][0][i]
        pass

    '''해당 글자의 인덱스를 반환, word=글자, parm=초성 중성 종성'''
    def getKoreanIndex(self,word,parm):
        #parm 1:초성, 2:중성, 3:종성
        if parm == 1:
            return self.firstKoreanList.index(word)
        elif parm ==2:
            return self.secondKoreanList.index(word)
        elif parm ==3:
            return self.thirdKoreanList.index(word)
        else:
            print("[getKoreanIndex] Error : not define parm value")
        pass

    '''해당 글자가 겹자음(모음)의 부모인지'''
    def isOverlapFamily(self,parent,child,parm):
        #1:자음, 2:모음
        if parm == 1:
            if parent in self.overlapConsonants.keys():
                if child in self.overlapConsonants[parent][0]:
                    return True
            else:
                return False

        elif parm == 2:
            if parent in self.overlapVowels.keys():
                if child in self.overlapVowels[parent][0]:
                    return True
            else:
                return False
        else:
            print("[isOverlapFamily] Error : not define parm value")
        pass

    '''글자 두개의 겹자음(모음) 을 만들어 char로 반환'''
    def getOverlapKorean(self,parent,child,parm):
        #1:자음, 2:모음
        if parm == 1:
            index = self.overlapConsonants[parent][0].index(child)
            return self.overlapConsonants[parent][1][index]
        elif parm == 2:
            index = self.overlapVowels[parent][0].index(child)
            return self.overlapVowels[parent][1][index]
            pass
        else:
            print("[getOverlapUnicode] Error : not define parm value")
        pass
    
    '''문자의 유니코드를 반환'''
    def charToUnicode(self,word,parm):
        if parm==1:
            idx = self.firstKoreanList.index(word)
            return self.firstKoreanUnicode[idx]
        elif parm==2:
            idx = self.secondKoreanList.index(word)
            return self.secondKoreanUnicode[idx]
        elif parm ==3:
            idx = self.thirdKoreanList.index(word)
            return self.thirdKoreanUnicode[idx]
        else:
            print("[chrToUnicode] Error : not define parm value")
        pass
    
    '''뒷글자, 입력글자의 비교,판단 등의 실질적인 조작 담당(함수 호출 등)'''
    def addString(self,lastWord,inputWord):
        print("last Word : ",lastWord, ", inputWord : ",inputWord)
        firstUnicode = 0
        secondUnicode = 0
        thirdUnicode = 0
        #print(lastWord, inputWord)
        #글자가 '가' 보다 클 때
        try:
            if ord(lastWord) >= self.base:
                firstUnicode,secondUnicode,thirdUnicode = self.wordToUnicodes(lastWord)
                firstWord, secondWord, thirdWord = self.unicodesToChars(firstUnicode,secondUnicode,thirdUnicode)

                #종성이 없을때 (받침이 없는 글자일 때)
                if thirdUnicode == self.thirdNum:
                    #다음글자가 중성일때
                    if inputWord in self.secondKoreanList:
                        #secondWord 가 겹모음 부모일때 (ㅘ 에서 ㅗ)
                        if self.isOverlapFamily(secondWord,inputWord,2):
                            secondWord = self.getOverlapKorean(secondWord,inputWord,2)
                            secondUnicode = self.charToUnicode(secondWord,2)
                            return self.unicodesToWord(firstUnicode,secondUnicode,self.thirdNum)
                        else:
                            return lastWord+inputWord
                        pass

                    #다음글자가 초성일때
                    elif inputWord in self.firstKoreanList:
                        #종성으로 쓸 수 없다면
                        if inputWord not in self.thirdKoreanList:
                            return lastWord + inputWord
                        else:
                            thirdWord = self.charToUnicode(inputWord,3)
                            return self.unicodesToWord(firstUnicode,secondUnicode,thirdWord)
                    else:
                        return lastWord + inputWord
                    pass

                #종성(받침) 이 있을때3
                else:
                    #다음글자가 중성일 때
                    if inputWord in self.secondKoreanList:
                        #이전문자의 받침이 초성이면
                        if thirdWord in self.firstKoreanList:
                            inputUnicode = self.charToUnicode(inputWord,2)
                            thirdUnicode = self.charToUnicode(thirdWord,1)
                            return self.unicodesToWord(firstUnicode,secondUnicode,self.thirdNum) + self.unicodesToWord(thirdUnicode,inputUnicode,self.thirdNum)

                        #이전문자의 받침이 겹자음이면
                        elif thirdWord in self.thirdKoreanList:
                            parent, child = self.getOverlapFamily(thirdWord)
                            childUnicode = self.charToUnicode(child,1)
                            parentUnicode = self.charToUnicode(parent,3)
                            inputUnicode = self.charToUnicode(inputWord,2)
                            return self.unicodesToWord(firstUnicode,secondUnicode,parentUnicode) + self.unicodesToWord(childUnicode,inputUnicode,self.thirdNum)

                        pass

                    #다음글자가 초성일 때
                    elif inputWord in self.firstKoreanList:
                        #이전문자의 받침이 초성이면
                        if thirdWord in self.firstKoreanList:
                            #이전문자의 받침과 다음문자가 겹자음이 가능하다면
                            if self.isOverlapFamily(thirdWord,inputWord,1):
                                #parent, child = self.getOverlapFamily(thirdWord)
                                overlapWord = self.getOverlapKorean(thirdWord,inputWord,1)
                                overlapWordUnicode = self.charToUnicode(overlapWord,3)
                                return self.unicodesToWord(firstUnicode,secondUnicode,overlapWordUnicode)
                            else:
                                return lastWord + inputWord
                        else:
                            return lastWord + inputWord
                    else:
                        return lastWord + inputWord
                    return lastWord + inputWord
                pass

            #else : '가' 보다 작을 때 (글자라고 볼 수 없는, 의미를 가지지 못하는)
            else:
                #이전 글자가 중성이면 ('ㅗ'... )
                if lastWord in self.secondKoreanList:
                    #다음 글자가 중성이면 ('ㅣ')
                    if inputWord in self.secondKoreanList:
                        #이전글자, 다음글자가 겹모음이 가능하다면
                        if self.isOverlapFamily(lastWord,inputWord,2):
                            return self.getOverlapKorean(lastWord,inputWord,2)
                        pass
                    else:
                        return lastWord+inputWord
                    pass

                #이전 글자가 초성이면 ('ㄱ'...)
                elif lastWord in self.firstKoreanList:
                    #다음 글자가 중성이면
                    if inputWord in self.secondKoreanList:
                        firstUnicode = self.charToUnicode(lastWord,1)
                        secondUnicode = self.charToUnicode(inputWord,2)
                        return self.unicodesToWord(firstUnicode,secondUnicode,self.thirdNum)

                    #다음 글자가 초성이면
                    elif inputWord in self.firstKoreanList:
                        #이전글자의 초성 과 다음글자의 초성이 겹자음이 가능하면
                        if self.isOverlapFamily(lastWord,inputWord,1):
                            word = self.getOverlapKorean(lastWord,inputWord,1)
                            return word
                        else:
                            return lastWord + inputWord
                        pass
                    else:
                        return lastWord + inputWord
                    pass
                #이전문자가 겹자음이면
                else:
                    #다음 글자가 중성('ㅗ') 이면
                    if inputWord in self.secondKoreanList:
                        parent , child = self.getOverlapFamily(lastWord)
                        child = self.charToUnicode(child,1)
                        inputWordUnicode = self.charToUnicode(inputWord,2)
                        return parent + self.unicodesToWord(child,inputWordUnicode,self.thirdNum)
                    else:
                        return lastWord + inputWord
                pass
            pass
        except Exception as e:
            print("Exception : ",e)
            return lastWord + inputWord

def main():
    test = HangulCombination()
    msg = ""
    while True:
        a = input()
        msg = test.smoothString(msg,a)
        print(msg)
        pass
    pass

if __name__ =="__main__":
    main()
