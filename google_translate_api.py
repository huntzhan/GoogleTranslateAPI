# standrad packages
import concurrent.futures

# third-part dependencies
import requests


class _BaseTranslator(object):

    """
    Low-level method for HTTP communication with google translation service.
    """
    pass


class TranslateService(_BaseTranslator):

    def __init__(self):
        pass

    def trans_word(self, src_lang, tgt_lang, src_text):
        """
        Description:
            trans_word is used to translate single word. Different from
            trans_sentence, trans_word would return a dictionary containing
            more specific information.
        Return Value:
            Dictionary contains information about the result of translation.
        """
        pass

    def trans_sentence(self, src_lang, tgt_lang, src_text):
        """
        Description:
            trans_sentence returns result of (long) sentence translation.
        Return Value:
            Dictionary contains information about the result of translation.
        """
        pass

    def languages(self):
        """
        Description:
            Get supported language.
        Return Value:
            List contains avaliable language codes.
        """
        pass

    def detect(self, src_text):
        """
        Description:
            Detect the language of given source text.
        Return Value:
            String corresponding to the language code of given source text.
        """
        pass


class TTSService(object):

    def __init__(self):
        pass

    def get_mpeg_binary(self, src_text):
        """
        Description:
            Get MPEG binary data of given source text, as the result of Google
            TTS service.
        Return Value:
            MPEG Binary data.
        """
        pass

    def speak(self, src_text):
        """
        Description:
            Instead of getting binary data, speak method just 'speak out' the
            given source text.
        Return Value:
            None
        """
        pass
