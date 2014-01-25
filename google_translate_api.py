# standrad packages
import concurrent.futures

# third-part dependencies
import requests


_GOOGLE_TRANS_URL = 'http://translate.google.com/translate_a/t'


class _BaseTranslator(object):

    """
    Low-level method for HTTP communication with google translation service.
    """

    def _request(self, src_lang, tgt_lang, src_text):
        """
        Description:
            GET request to translate.google.com.
        Return Value:
            Dictionary contains unicode JSON data.
        """

        params = {
            'client': 'z',
            'sl': src_lang,
            'tl': tgt_lang,
            'ie': 'UTF-8',
            'oe': 'UTF-8',
            'text': src_text,
        }

        response = requests.get(_GOOGLE_TRANS_URL, params=params)
        return response.json()


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
        return self._request(src_lang, tgt_lang, src_text)

    def trans_sentence(self, src_lang, tgt_lang, src_text):
        """
        Description:
            trans_sentence returns result of (long) sentence translation.
        Return Value:
            Dictionary contains information about the result of translation.
        """
        # split text
        # query with concurrency
        # assemble results
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
        # for long sentence, simples and query.
        # for short sentence
        return self._request('', '', src_text)['src']


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
