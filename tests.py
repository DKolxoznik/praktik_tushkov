import unittest
import os
from database import TemplateDB


class TestFormTemplates(unittest.TestCase):
    test_db_path = 'test_db.json'

    def setUp(self):
        # Удаляем старый файл, если существует
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

        self.db = TemplateDB(self.test_db_path)
        self.db.initialize_db()

    def tearDown(self):
        self.db.close()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_template_matching(self):
        # Тест полного совпадения
        fields = {'f_name1': 'test@example.com', 'f_name2': '01.01.2023'}
        self.assertEqual(self.db.find_template(fields), "Проба")

        # Тест с дополнительными полями
        fields = {'f_name1': 'test@example.com', 'f_name2': '01.01.2023', 'extra': 'field'}
        self.assertEqual(self.db.find_template(fields), "Проба")

        # Тест отсутствия шаблона
        fields = {'unknown': 'value'}
        self.assertIsNone(self.db.find_template(fields))

        # Тест частичного совпадения
        fields = {'f_name1': 'test@example.com'}
        self.assertIsNone(self.db.find_template(fields))

    def test_field_validation(self):
        from validators import determine_field_type

        self.assertEqual(determine_field_type('01.01.2023'), 'date')
        self.assertEqual(determine_field_type('2023-01-01'), 'date')
        self.assertEqual(determine_field_type('+7 123 456 78 90'), 'phone')
        self.assertEqual(determine_field_type('test@example.com'), 'email')
        self.assertEqual(determine_field_type('plain text'), 'text')


if __name__ == '__main__':
    unittest.main()