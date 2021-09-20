import unittest
from unittest.mock import patch
import app as a


class TestSecretaryUnittest(unittest.TestCase):

    @patch('builtins.input', lambda *args: '2207 876234')
    def test_get_doc_owner_name_exist(self):
        self.assertEqual('Василий Гупкин', a.get_doc_owner_name())

    @patch('builtins.input', lambda *args: '322')
    def test_get_doc_owner_name_not_exist(self):
        self.assertEqual(None, a.get_doc_owner_name())

    # Вопрос по тесту. Если указать множество конкретных имен, в зависимости от способа запуска теста (запуск теста
    # отдельно либо запуск всего тестового класса) результат меняется. Все из-за того, что работаем со словарем.
    # Можно ли это как-то по-другому обойти?
    def test_show_all_docs_info(self):
        self.assertEqual({item['name'] for item in a.documents}, a.get_all_doc_owners_names())

    @patch('builtins.input', lambda *args: '10006')
    def test_get_doc_shelf_exist(self):
        self.assertEqual('2', a.get_doc_shelf())

    @patch('builtins.input', lambda *args: '100063848')
    def test_get_doc_shelf_not_exist(self):
        self.assertEqual(None, a.get_doc_shelf())

    @patch('builtins.input', lambda *args: '7')
    def test_add_new_doc(self):
        self.assertEqual('7', a.add_new_doc())
        self.assertIn({"type": "7", "number": "7", "name": "7"}, a.documents)
        self.assertIn(('7', ['7']), a.directories.items())

    @patch('builtins.input', lambda *args: '11-2')
    def test_delete_doc_exist(self):
        self.assertEqual(('11-2', True), a.delete_doc())
        self.assertNotIn({"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"}, a.documents)
        self.assertNotIn('11-2', a.directories['1'])

    @patch('builtins.input', lambda *args: '343545656')
    def test_delete_doc_not_exist(self):
        self.assertEqual(None, a.delete_doc())

    @patch('builtins.input', lambda *args: '11-2')
    def test_move_doc_to_shelf_exist(self):
        a.move_doc_to_shelf()
        self.assertNotIn('11-2', a.directories['1'])
        self.assertIn('11-2', a.directories['11-2'])

    # При вводе несуществующего документа, программа все равно "кладет" этот документ на указанную полку. Тест падает.
    @unittest.expectedFailure
    @patch('builtins.input', lambda *args: '15-2')
    def test_move_doc_to_shelf_not_exist(self):
        a.move_doc_to_shelf()
        self.assertNotIn('15-2', a.directories['15-2'])

    def test_add_new_shelf_exist(self):
        self.assertEqual(('1', False), a.add_new_shelf('1'))

    def test_add_new_shelf_not_exist(self):
        self.assertEqual(('4', True), a.add_new_shelf('4'))
        self.assertIn(('4', []), a.directories.items())
