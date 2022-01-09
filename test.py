from deep_translator import GoogleTranslator
from deep_translator import PonsTranslator

to_translate = "Sevgili kardeşim, seni çok seviyorum!"
translated = PonsTranslator(source='english',
target='german').translate(text, to_translate)

print(translated)

