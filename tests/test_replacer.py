from unittest import TestCase
import replacer


class TestReplacer(TestCase):

    def test_replace(self):
        test_cases = [['Слово', 'Слово'], ['Строка', 'Строка™'],
                      ['Начало строки', 'Начало™ строки™'],
                      ['Текст для тестирования', 'Текст для тестирования'],
                      ['Сейчас на фоне уязвимости Logjam все в индустрии в '
                       'очередной раз обсуждают проблемы и особенности TLS.',
                       'Сейчас™ на фоне уязвимости Logjam™ все в индустрии в '
                       'очередной раз обсуждают проблемы и особенности TLS.'],
                      ['Строка для тестов, проверка запятой.',
                       'Строка™ для тестов™, проверка запятой.']]
        for test_string, expected in test_cases:
            self.assertEqual(replacer.replace(test_string), expected)
