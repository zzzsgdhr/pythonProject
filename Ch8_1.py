import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual(‘test’.upper(), ‘TEST’)    # 判断两个值是否相等

    def test_isupper(self):
        self.assertTrue(‘TEST’.isupper())          # 判断值是否为 True
        self.assertFalse(‘Test’.isupper())         # 判断值是否为 False
