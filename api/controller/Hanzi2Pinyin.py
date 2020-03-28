from api import api_blue
from flask import Response, request
import os.path as path
import jieba
import jieba.posseg as pseg
from pypinyin import pinyin, Style
import utils

jieba.initialize()
userDict = path.dirname(path.dirname(path.dirname(__file__))) + "/data/userDict.txt"
if(path.exists(userDict)):
    jieba.load_userdict(userDict)

class Hanzi2Pinyin:
    def filteJiebaTag(self, segList):
        ret = []
        for word, flag in segList:
            if(flag[0] == "u" and (word == "得" or word == "地")):
                ret.append("的")
            else:
                ret.append(word)
        return ret

    def parse(self, sentence):
        sentence = utils.replaceCJKPunc(sentence).replace(' ', '-')
        segList = self.filteJiebaTag(pseg.cut(sentence))
        sentenceList = []
        pinyinGroup = []
        for seg in segList:
            if(utils.isAscii(seg)):
                if(utils.isAsciiPunc(seg)):
                    if(len(pinyinGroup) > 0):
                        sentenceList.append(pinyinGroup)
                        pinyinGroup = []
                    sentenceList.append(seg)
                else:
                    if(len(pinyinGroup) > 0):
                        sentenceList.append(pinyinGroup)
                        pinyinGroup = []
                    sentenceList.append([seg])
            else:
                sentencePinyin = []
                for one in pinyin(seg, style=Style.NORMAL):
                    sentencePinyin.append(one[0])
                pinyinGroup.append(sentencePinyin)
        if(len(pinyinGroup) > 0):
            sentenceList.append(pinyinGroup)

        return sentenceList

    @staticmethod
    @api_blue.route('/asciiurl/hanzi2pinyin', methods=['GET', 'POST'])
    def hanzi2pinyin():
        params = utils.getParam(request)
        sentence = params.get('sentence')
        if(sentence):
            parser = Hanzi2Pinyin()
            data = parser.parse(sentence)
            return utils.ajaxResponse(1, data)
        else:
            return utils.ajaxResponse(-1, error="Param 'sentence' not set.")