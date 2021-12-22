from flask import Response, Request
import json
import re


def getParam(request: Request):
    if request.method == 'POST':
        if request.headers.get('content-type') == 'application/json':
            return request.json
        else:
            return request.form
    else:
        return request.args


def ajaxResponse(status, data=None, error=None, warning=None):
    ret = {"status": status}
    if data:
        ret["data"] = data
    if error:
        ret["error"] = error
    if warning:
        ret["warning"] = warning
    content = json.dumps(ret)
    return Response(content, 200, {"Content-Type": "application/json"})


def isAscii(inputStr):
    return bool(re.match(r"^[\x00-\xff]+$", inputStr))


def isAsciiPunc(inputStr):
    return bool(re.match(r"^[\x20-\x2f\x3a-\x40\x5b-\x60]+$", inputStr))


def isAsciiChar(char):
    return ord(char) <= 255


def isAsciiPuncChar(char):
    charCode = ord(char)
    if 0x20 <= charCode <= 0x2f or 0x3a <= charCode <= 0x40 or 0x5b <= charCode <= 0x60:
        return True
    else:
        return False


class CHARTYPE:
    ASCII = 0
    ASCII_PUNC = 1
    UNICODE = 2


def getCharType(char):
    if isAsciiChar(char):
        if isAsciiPuncChar(char):
            return CHARTYPE.ASCII_PUNC
        else:
            return CHARTYPE.ASCII
    else:
        return CHARTYPE.UNICODE


def replaceCJKPunc(string):
    table = {ord(f): ord(t) for f, t in zip(
        u'，。！？【】（）《》％＃＠＆·１２３４５６７８９０',
        u',.!?[]()  %#@& 1234567890')}
    return string.translate(table)


def splitAscii(string):
    if len(string) == 0:
        return string
    string = replaceCJKPunc(string)

    lastCharType = getCharType(string[0])
    segList = []
    startPos = 0
    endPos = 0
    buffer = []
    for char in string:
        if char == " ":
            if endPos > startPos:
                segList.append(string[startPos:endPos])
            startPos = endPos + 1
        else:
            currentCharType = getCharType(char)
            if lastCharType != currentCharType:
                if endPos > startPos:
                    segList.append(string[startPos:endPos])
                    startPos = endPos
                lastCharType = currentCharType
        endPos += 1

    if endPos > startPos:
        segList.append(string[startPos:])
    return segList
