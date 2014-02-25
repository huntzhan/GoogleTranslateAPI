# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

import random
import unittest

from concurrent.futures import ThreadPoolExecutor
import google_translate_api as api


class _BaseRequestMinixTest(unittest.TestCase):

    def setUp(self):
        self._minix = api._BaseRequestMinix()

    def test_request_reconnect(self):

        def raise_exception(retry_times):
            counter = {0: retry_times}

            def wrapper():
                if counter[0] == 0:
                    return
                else:
                    counter[0] -= 1
                    raise Exception
            return wrapper

        for retry_times in range(1, api._RECONNECT_TIMES + 1):
            callback = raise_exception(retry_times)
            self._minix._request_with_reconnect(callback)

        with self.assertRaises(Exception):
            callback = raise_exception(api._RECONNECT_TIMES + 1)
            self._minix._request_with_reconnect(callback)

    def test_check_threads(self):
        def good_func():
            return

        def bad_func():
            raise Exception

        size = random.randint(1, 1000)

        with ThreadPoolExecutor(max_workers=size) as executor:
            threads = []
            for i in range(size - 1):
                future = executor.submit(good_func)
            # append bad func
            future = executor.submit(bad_func)
            threads.insert(
                random.randint(0, size - 1),
                future,
            )
            with self.assertRaises(Exception):
                self._minix._check_threads(threads)


class _SplitTextMinixTest(unittest.TestCase):

    def setUp(self):
        self._minix = api._SplitTextMinix()

    def test_find_split_point(self):
        text = "This is a sentence. This is another sentence."

        # boundary case, end equals to len(text) - 1.
        modify_flag, end = self._minix._find_split_point(text, 0, len(text),
                                                         'Po')
        self.assertEqual(end, len(text))

        # boundary case, end equals to len(text)
        with self.assertRaises(Exception):
            self._minix._find_split_point(text, 0, len(text) + 1, 'Po')

        # assert to find first period.
        modify_flag, end = self._minix._find_split_point(text,
                                                         0,
                                                         len(text) - 1,
                                                         'Po')
        self.assertEqual(end, text.find('.') + 1)

    def test_split_text(self):
        sentence = " This is a sentence."

        # boundary case, max_length equals to the length of sentence.
        split_text = self._minix._split_text(sentence * 2, len(sentence))
        self.assertEqual(split_text, [sentence, sentence])

        # boundary case, max_length equals to the length of sentence minus one,
        # which means both sentences would be split in the middle.
        split_text = self._minix._split_text(sentence * 2, len(sentence) - 1)
        result = [
            " This is a ",
            "sentence.",
            " This is a ",
            "sentence.",
        ]
        self.assertEqual(split_text, result)

        # boundary case, last character is a unicode separater.
        split_text = self._minix._split_text(sentence + ' ', len(sentence))
        self.assertEqual(split_text, [sentence, ' '])

        # max_length greater than length of text.
        split_text = self._minix._split_text(sentence, len(sentence) * 10)
        self.assertEqual(split_text, [sentence])


class _TranslateMinixTest(unittest.TestCase):

    def setUp(self):
        self._minix = api._TranslateMinix()

    def test_basic_request(self):

        # en to zh-CN
        result = self._minix._basic_request('en', 'zh-CN', 'test')
        self.assertIn('dict', result)
        self.assertIn(api.SENTENCES, result)
        self.assertIn(api.SRC, result)

        # zh-CN to en
        result = self._minix._basic_request('zh-CN', 'en', '测试')
        self.assertIn(api.SENTENCES, result)
        self.assertIn(api.SRC, result)

    def test_merge_jsons(self):

        json_1st = {
            api.SENTENCES: [{api.TRANS: 'whatever'}],
            api.SRC: 'en',
        }
        json_2nd = {
            api.SENTENCES: [{api.TRANS: 'whatever else'}],
            api.SRC: 'zh-CN',
        }

        # for 1st
        json = self._minix._merge_jsons([json_1st])
        expect_json = {
            api.SENTENCES: [{api.TRANS: 'whatever'}],
            api.SRC: {'en': 1.0},
        }
        self.assertEqual(json, expect_json)

        # merge 1st and 2nd
        json = self._minix._merge_jsons([json_1st, json_2nd])
        expect_merge_json = {
            api.SENTENCES: [{api.TRANS: 'whatever'},
                            {api.TRANS: 'whatever else'}],
            api.SRC: {'en': 0.5, 'zh-CN': 0.5},
        }
        self.assertEqual(json, expect_merge_json)


class TranslateServiceTest(unittest.TestCase):

    def setUp(self):
        self.translator = api.TranslateService()

    def test_trans_details(self):

        # en to zh-CN
        result = self.translator.trans_details(
            'en',
            'zh-CN',
            'test',
        )
        self.assertIn(api.SENTENCES, result)
        self.assertIn(api.SRC, result)
        sentence = result[api.SENTENCES][0]
        self.assertIn(api.TRANS, sentence)

        # zh-CN to en
        result = self.translator.trans_details(
            'zh-CN',
            'en',
            '测试',
        )
        self.assertIn(api.SENTENCES, result)
        self.assertIn(api.SRC, result)
        sentence = result[api.SENTENCES][0]
        self.assertIn(api.TRANS, sentence)

    def test_trans_sentence(self):

        result = self.translator.trans_sentence(
            'en',
            'zh-CN',
            'hello world.',
        )
        self.assertEqual(result, '你好世界。')

    def test_detect(self):

        # en
        result = self.translator.detect('test')
        self.assertEqual(result, {'en': 1.0})

        # zh-CN
        result = self.translator.detect('测试')
        self.assertEqual(result, {'zh-CN': 1.0})

    # def test_print_json(self):
    #     from pprint import pprint
    #     result = self.translator.trans_details(
    #         'en',
    #         'zh-CN',
    #         'test',
    #     )
    #     pprint(result)

    #     result = self.translator.trans_details(
    #         'en',
    #         'zh-CN',
    #         'hello world.',
    #     )
    #     pprint(result)


if __name__ == '__main__':
    unittest.main()
