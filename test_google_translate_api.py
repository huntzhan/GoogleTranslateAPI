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
            counter = retry_times
            def wrapper():
                nonlocal counter
                if counter == 0:
                    return
                else:
                    counter -= 1
                    raise Exception
            return wrapper

        for retry_times in range(1, api._RECONNECT_TIMES+1):
            callback = raise_exception(retry_times)
            self._minix._request_with_reconnect(callback)

        with self.assertRaises(Exception):
            callback = raise_exception(api._RECONNECT_TIMES+1)
            self._minix._request_with_reconnect(callback)

    def test_check_threads(self):
        def good_func():
            return

        def bad_func():
            raise Exception

        size = random.randint(1, 1000)

        with ThreadPoolExecutor(max_workers=size) as executor:
            threads = []
            for i in range(size-1):
                future = executor.submit(good_func)
            # append bad func
            future = executor.submit(bad_func)
            threads.insert(
                random.randint(0, size-1),
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
        end = self._minix._find_split_point(text, 0, len(text), 'Po')
        self.assertEqual(end, len(text))

        # boundary case, end equals to len(text)
        with self.assertRaises(Exception):
            self._minix._find_split_point(text, 0, len(text)+1, 'Po')

        # assert to find first period.
        end = self._minix._find_split_point(text, 0, len(text)-1, 'Po')
        self.assertEqual(end, text.find('.')+1)

    def test_split_text(self):
        sentence = " This is a sentence."

        # boundary case, max_length equals to the length of sentence.
        split_text = self._minix._split_text(sentence*2, len(sentence))
        self.assertEqual(split_text, [sentence, sentence])

        # boundary case, max_length equals to the length of sentence minus one,
        # which means the first sentence would be split in the middle.
        split_text = self._minix._split_text(sentence*2, len(sentence)-1)
        result = [
            " This is a ",
            "sentence.",
            sentence,
        ]
        self.assertEqual(split_text, result)


if __name__ == '__main__':
    unittest.main()
