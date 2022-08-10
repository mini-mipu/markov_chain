#https://github.com/ckiplab/ckip-transformers
from ckip_transformers.nlp import CkipWordSegmenter
import random
import pandas as pd
ws_driver  = CkipWordSegmenter(model="bert-base")
ws_driver = CkipWordSegmenter(device=0)

# text = [
#    "老師就像一隻隻辛苦忙碌的蜜蜂，每天忙著授予知識的花粉給他們心中那些美麗、天真又可愛的花朵。",
#    "總是在學生身旁默默扶持著，雖然老師們上課有時輕鬆，有時嚴厲，最終心願還是希望自己心愛的學生能快樂學習，順利完成學業。",
#    "求學多年，我所遇到的老師均對我有莫大影響。",
#    "每位老師都在我心中佔有一席地位，他們都是我心目中的恩師。",
#    "所以，如果我能當一天老師，我一定要讓學生永遠記得我。",
#    "在充滿神奇奧妙的自然課上，使學生們對自然產生興趣是最重要的，帶領學生走出悶熱的教室，徜徉於大自然中，呼吸新鮮空氣，沉澱煩雜的心靈。",
#    "讓學生們忘卻暗綠色的黑板，眼中盡是翠綠花草樹木，心中便不再覺得上課是單調、乏味的。",
#    "帶領學生們探觸世界中的一草一木，走在大自然中，偶爾停下來，觀察小溪邊的蘚苔植物，一面告訴他們葉片背面的孢子囊堆是繁殖下一代的生命之源，也藉機教他們如何使用顯微鏡等儀器觀察，讓他們了解萬物靜觀皆自得。",
#    "看著學生們開朗的笑容、專注聆聽的表情，彷彿身邊多了一群可愛又頑皮的小天使，雖然常惹出許多麻煩卻又不失天真的本性。",
#    "看著他們認真得學習，與他們一同討論、研究，並獲得學生的喜愛、認同及尊重。",
#    "我想，這就是如果我能當一天的老師最希望做的事。",
#    "老師，是一件辛苦又偉大的事業，苦思對學生們最有幫助的教學方式想必都是老師們每天都要操心的問題，畢竟每位老師都希望自己的愛徒們能走向光明燦爛的人生，所以如果我能當一天的老師，我希望可以親自帶領學生們體驗輕鬆、快樂的戶外教學。"
# ]

def read_file(path):
	text = []
	with open(path,'r',encoding='utf-8') as f:
		while True:
			line = f.readline().strip()
			if not line: break
			line = line.split('^')
			if line[6] != 'R': continue
			text.append(line[0]+'。')
	return text


text = read_file('errData_M1.txt')
# Run pipeline
ws  = ws_driver(text)


def make_chain(text):
	index = 1
	chain = {}
	for t in text:
		for word in t[index:]:
			key = t[index-1]
			if key in chain:
				if word not in chain[key]: chain[key].append(word)
			else:
				chain[key] = [word]
			index+=1
		index = 1
	return chain

mk_chain = make_chain(ws)
wf = open('errData_M1_mkchain.txt','w',encoding='utf-8')
for i in mk_chain.keys():
	wf.write(i+str(mk_chain.get(i))+'\n')
wf.close()

def create_sentence(chain, length, firstwordsz = None):
	start = random.choice(list(chain.keys()) if firstwordsz is None else firstwordsz)
	wordsz = [start]
	# while len(wordsz) < length:
	while True:
		start = random.choice(chain.get(start,list(chain.keys())))
		wordsz.append(start)
		if start == '。': break
	return "".join(wordsz)

for i in range(10):
	newsentence = create_sentence(mk_chain, 9, None)
	print(newsentence)