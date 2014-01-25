# standrad packages
import unicodedata
import concurrent.futures

# third-part dependencies
import requests


_GOOGLE_TRANS_URL = 'http://translate.google.com/translate_a/t'


class _TranslateMinix(object):

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
        }

        response = requests.post(
            _GOOGLE_TRANS_URL,
            data={'q': src_text},
            params=params,
        )
        return response.json()


class _SplitTextMinix(object):
    """
    Split Unicode Text.
    """

    def _check_punctuation(self, character):
        """
        Description:
            Accept a character and judge whether it is a unicode punctuation or
            not.
        Return Value:
            True for unicode punctuation and False for everything else.
        """
        if unicodedata.category(character).startswith('P'):
            return True
        else:
            return False

    def _split_text(self, text, max_length):
        """
        Description:
            Receive unicode text, split it based on max_length(maximum
            number of characters). Unicode punctuations are the 'split points'
            of text. If there's no punctuations for split, max_length is adopt
            for splitting text.
        Return Value:
            List cotains split text.
        """
        split_text = []
        start = 0
        end = max_length
        while end < len(text):
            for index in reversed(range(start, end)):
                if self._check_punctuation(text[index]):
                    end = index + 1
                    break
            split_text.append(text[start: end])
            start = end
            end = start + max_length
        split_text.append(text[start:])
        return split_text


class TranslateService(_TranslateMinix, _SplitTextMinix):

    def __init__(self):
        pass

    def trans_details(self, src_lang, tgt_lang, src_text):
        """
        Description:
            trans_details is used to translate single word. Different from
            trans_sentence, trans_details would return a dictionary containing
            more related information.
        Return Value:
            Dictionary contains information about the result of translation.
        """
        # assure size
        return self._request(src_lang, tgt_lang, src_text)

    def trans_sentence(self, src_lang, tgt_lang, src_text):
        """
        Description:
            trans_sentence returns result of (long) sentence translation.
        Return Value:
            String contains information about the result of translation.
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
