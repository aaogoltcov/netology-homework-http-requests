import json
import unittest
from translator import file_translate


class TranslatorTestUnit(unittest.TestCase):

    def setUp(self):
        self.text_for_translation = 'привет'
        self.file_name = 'Hello.txt'
        with open(self.file_name, 'w') as file:
            file.write(self.text_for_translation)
        self.new_file_name, self.response = file_translate(self.file_name)

        try:
            self.translate_result_code = self.response.json()['code']
            self.translate_result_text = self.response.json()['text'][1]
        except (TypeError, json.decoder.JSONDecodeError, IndexError):
            self.translate_result_code = self.response.status_code
            self.translate_result_text = 'error'

    @unittest.expectedFailure
    def test_raise_except_code(self):
        self.fail_code = 404
        self.assertEqual(self.response.status_code, self.fail_code)

    def test_translate_result_code(self):
        self.assertEqual(self.translate_result_code, 200)

    def test_translate_result_text(self):
        self.assertEqual(self.translate_result_text, 'привет')

# if __name__ == '__main__':
#     unittest.main()
