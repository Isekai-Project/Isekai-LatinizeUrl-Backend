from flask import request

import utils
from api import api_blue
from extend.kanji_to_romaji import kanji_to_romaji


class Kanji:
    def convertToRomaji(self, kanji):
        segList = utils.splitAscii(kanji)
        sentenceList = []
        for seg in segList:
            if utils.isAscii(seg):
                if utils.isAsciiPunc(seg):
                    sentenceList.append(seg)
                else:
                    sentenceList.append([seg])
            else:
                romaji = kanji_to_romaji(seg)
                sentenceList.append(romaji.split(" "))
        return sentenceList

    @staticmethod
    @api_blue.route('/kanji/romaji/', methods=['GET', 'POST'])
    def kanji2romaji():
        params = utils.getParam(request)
        sentence = params.get('sentence')
        if sentence:
            convertor = Kanji()
            data = convertor.convertToRomaji(sentence)
            return utils.ajaxResponse(1, data)
        else:
            return utils.ajaxResponse(-1, error="Param 'sentence' not set.")
