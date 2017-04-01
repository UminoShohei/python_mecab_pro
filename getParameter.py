import urllib
import requests
import MeCab
import re
from flask import Flask,request,json
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route('/post', methods=['POST'])
def post():
    getText = request.json['data']
    print(getText)
    response = getInfo(getText)
    print(response)
    return response


def getInfo(text):
    mecab = MeCab.Tagger ('/usr/lib/mecab/dic/mecab-ipadic-neologd')
    dict = []
    mecab.parse('')#文字列がGCされるのを防ぐ
    node = mecab.parseToNode(text)
    while node:
        mecab2 = MeCab.Tagger ('/usr/lib/mecab/dic/mecab-ipadic-neologd')
        #単語を取得
        word = node.surface
        #品詞を取得
        pos = node.feature.split(",")[1]
        if pos == "固有名詞":
            # print('{0} , {1}'.format(word, pos))
            r = requests.get('http://ja.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&titles='+word)
            json_response = json.loads(r.text)
            # jsonstring = json.dumps(json_response, ensure_ascii=False)
            pages = json_response['query']['pages']
            for key,value in pages.items():
                page = value
            p = re.compile(r"<[^>]*?>")
            title = page['title']
            title = p.sub("", title)
            info = page['extract']
            info = p.sub("", info)
            item  = {"title": title, "info": info}
            dict.append(item)
        #次の単語に進める
        node = node.next

    dictionary = {"result": dict}
    response = createJson(dictionary)
    return response


def createJson(dictionary):
    responseJson = json.dumps(dictionary, ensure_ascii=False)
    return responseJson
        
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

