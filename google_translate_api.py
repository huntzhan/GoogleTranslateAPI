# standrad packages
import unicodedata
from concurrent.futures import ThreadPoolExecutor

# third-part dependencies
import requests


_GOOGLE_TRANS_URL = 'http://translate.google.com/translate_a/t'
_RECONNECT_TIMES = 5
_TIMEOUT = 30

_MAX_LENGTH = 2000
_SENTENCES = 'sentences'
_SRC = 'src'
_TRANS = 'trans'


class _TranslateMinix(object):

    """
    Low-level method for HTTP communication with google translation service.
    """

    def _basic_request(self, src_lang, tgt_lang, src_text):
        """
        Description:
            POST request to translate.google.com. If connection failed,
            _basic_request would try to reconnect the server.
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

        reconnect_times = _RECONNECT_TIMES
        while True:
            try:
                # POST request
                response = requests.post(
                    _GOOGLE_TRANS_URL,
                    data={'q': src_text},
                    params=params,
                )
                break
            except Exception as e:
                if reconnect_times == 0:
                    # has already tried _RECONNECT_TIMES times, request failed.
                    # if so, just let it crash.
                    raise e
                else:
                    reconnect_times -= 1

        return response.json()

    def _merge_jsons(self, jsons):
        """
        Description:
            Receive JSON dictionaries returned by _basic_request. With the
            observation of JSON response of translate.google.com, we can see
            that:
                1. For single word translation, JSON dictionary contains more
                information compared to sentence translation.
                2. For multi-word sentence translation, there are three keys in
                JSON dictionary, 'sentences', 'server_time' and 'src'. The JSON
                dictionary returned by single word translation, on the other
                hand, has an extra key 'dict' whose value related to details
                of the meanings.
            Therefore, for jsons has the length greater than one, _merge_json
            would just merge the value of 'sentences' key in jsons. For the
            accuracy of language detectation, values of 'src' key in jsons
            would be analysed and stored as a dictionary, with language code as
            its key and the proportion as its value.
        Return Value:
            Dictionary contains unicode JSON data.
        """

        assert type(jsons) is list
        if len(jsons) == 1:
            # adjust src
            single_json = jsons[0]
            single_json[_SRC] = {single_json[_SRC]: 1.0}
            return single_json

        merged_json = {
            _SENTENCES: [],
            _SRC: {},
        }
        langs = merged_json[_SRC]
        lang_counter = 0
        for json in jsons:
            merged_json[_SENTENCES].extend(json[_SENTENCES])

            lang_code = json[_SRC]
            if lang_code in langs:
                langs[lang_code] += 1
            else:
                langs[lang_code] = 1
            lang_counter += 1
        # analyse src
        for lang_code, val in langs.items():
            langs[lang_code] = float(val) / lang_counter

        return merged_json

    def _request(self, src_lang, tgt_lang, src_texts):
        """
        Description:
            Receive src_texts, which should be a list of texts to be
            translated. _request method calls _basic_request method for http
            request, and assembles the JSON dictionary returned by
            _basic_request. For case that _basic_request needs to be called
            multiple times, concurrent.futures package is adopt for the usage
            of threads concurrency.
        Return Value:
            Dictionary contains unicode JSON data.
        """

        assert type(src_texts) is list

        executor = ThreadPoolExecutor(max_workers=len(src_texts))
        threads = []
        for src_text in src_texts:
            future = executor.submit(
                self._basic_request,
                src_lang,
                tgt_lang,
                src_text,
            )
            threads.append(future)

        # check whether all threads finished or not.
        for future in threads:
            if future.exception(_TIMEOUT) is None:
                continue
            else:
                # let it crash.
                raise future.exception()

        # now, all is well.
        # assemble JSON dictionary(s).
        merged_json = self._merge_jsons(
            [future.result() for future in threads],
        )
        return merged_json


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

        if unicodedata.category(character) == 'Po':
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
                    # (index + 1) means that the punctuation is included in the
                    # sentence(s) to be split. Reason of doing that is based on
                    # the observation of google TTS HTTP request header.
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

    def _translate(self, src_lang, tgt_lang, src_text):
        """
        Description:
            Split text and request for JSON dictionary.
        Return Value:
            Dictionary contains information about the result of translation.
        """

        # split text
        src_texts = self._split_text(src_text, _MAX_LENGTH)
        # request with concurrency
        return self._request(src_lang, tgt_lang, src_texts)

    def trans_details(self, src_lang, tgt_lang, src_text):
        """
        Description:
            trans_details is used to translate single word. Different from
            trans_sentence, trans_details would return a dictionary containing
            more related information.
        Return Value:
            Dictionary contains information about the result of translation.
        """

        return self._translate(src_lang, tgt_lang, src_text)

    def trans_sentence(self, src_lang, tgt_lang, src_text):
        """
        Description:
            trans_sentence returns result of (long) sentence translation.
        Return Value:
            String contains information about the result of translation.
        """

        json_result = self._translate(src_lang, tgt_lang, src_text)
        sentences = []
        for item in json_result[_SENTENCES]:
            sentences.append(item[_TRANS])
        return ''.join(sentences)

    def detect(self, src_text):
        """
        Description:
            Detect the language of given source text.
        Return Value:
            Dictionary contains language information.
        """

        json_result = self._translate('', '', src_text)
        return json_result[_SRC]


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