from api import api_blue
from flask import Response, request
import utils
from extend.hangul_romanize import Transliter
from extend.hangul_romanize.rule import academic


class Hanja:
    def convertToRomaja(self, hanja):
        transliter = Transliter(academic)
        segList = utils.splitAscii(hanja)
        sentenceList = []
        for seg in segList:
            if seg == " ":
                sentenceList.append("-")
            elif utils.isAscii(seg):
                if utils.isAsciiPunc(seg):
                    sentenceList.append(seg)
                else:
                    sentenceList.append([seg])
            else:
                roma = transliter.translit(seg)
                sentenceList.append(roma.split(" "))
        return sentenceList

    @staticmethod
    @api_blue.route('/hanja/romaja/', methods=['GET', 'POST'])
    def hanja2roma():
        params = utils.getParam(request)
        sentence = params.get('sentence')
        if sentence:
            convertor = Hanja()
            data = convertor.convertToRomaja(sentence)
            return utils.ajaxResponse(1, data)
        else:
            return utils.ajaxResponse(-1, error="Param 'sentence' not set.")
