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

if __name__ == '__main__':
    unittest.main()
