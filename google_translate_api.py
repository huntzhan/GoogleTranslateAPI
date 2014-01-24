

class _BaseTranslator(object):
    pass


class TranslateService(_BaseTranslator):

    def __init__(self):
        pass

    def trans_word(self, src_lang, tgt_lang, src_text):
        pass

    def trans_sentence(self, src_lang, tgt_lang, src_text):
        pass

    def languages(self):
        pass

    def detect(self, src_text):
        pass


class TTSService(object):

    def __init__(self):
        pass

    def get_mpeg_binary(self, src_text):
        pass

    def speak(self, src_text):
        pass
