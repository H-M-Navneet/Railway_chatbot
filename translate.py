import googletrans
from googletrans import Translator

#print(googletrans.LANGUAGES)

t1 = "how are you"
t2 = "आप कैसे हैं"
t3 = "ನೀವು ಹೇಗಿದ್ದೀರಿ"

trans = Translator()

print(trans.detect(t1))
print(trans.detect(t2))
print(trans.detect(t3).lang)

print("translated from Hindi : ",trans.translate(t2))
print("translated from Kannada : ",trans.translate(t3))

trans_res = trans.translate(t2)
trans_text = trans_res.text
print(trans_text)

