import uuid
import unittest

import mutant_repository
from unittest.mock import patch, Mock

class TestMutantRepository(unittest.TestCase):

    HUMAN_DNA_ID = uuid.UUID('06335e84-2872-4914-8c5d-3ed07d2a2f16').hex
    HUMAN_DNA_IS_MUTANT = True
    HUMAN_DNA_STATICTICS_MUTANT_COUNT = 1
    HUMAN_DNA_STATICTICS_HUMAN_COUNT = 2
    HUMAN_DNA_STATICTICS_RATIO = 0.5

    @patch('utils.database_utils.connect_to_database')
    def test_save_human_dna_and_update_human_dna_statistics_when_human(self, connect_to_database_call):
        connection_mock = Mock()
        connect_to_database_call.return_value = connection_mock
        cursor_mock = connection_mock.cursor.return_value
        cursor_mock.execute.return_value = None
        cursor_mock.fetchone.return_value = [self.HUMAN_DNA_ID]
        
        result = mutant_repository.save_human_dna_and_update_human_dna_statistics(
            4, ["ATCG,ATCG,ATCG,ATCG"], False)

        self.assertEqual(result, self.HUMAN_DNA_ID)
        self.assertEqual(cursor_mock.execute.call_count, 2)
        cursor_mock.execute.assert_called_with(
            " UPDATE human_dna_statistics SET " +
            "    count_human_dna = count_human_dna + 1, " +
            "    ratio = CAST(CAST(count_mutant_dna AS DECIMAL(5,4)) / CAST((count_human_dna + 1) AS DECIMAL(5,4)) AS DECIMAL(5,4)); "
        )

    @patch('utils.database_utils.connect_to_database')
    def test_save_human_dna_and_update_human_dna_statistics_when_mutant(self, connect_to_database_call):
        connection_mock = Mock()
        connect_to_database_call.return_value = connection_mock
        cursor_mock = connection_mock.cursor.return_value
        cursor_mock.execute.return_value = None
        cursor_mock.fetchone.return_value = [self.HUMAN_DNA_ID]
        
        result = mutant_repository.save_human_dna_and_update_human_dna_statistics(
            4, ["ATCG,AACG,ATAG,ATCA"], True)

        self.assertEqual(result, self.HUMAN_DNA_ID)
        self.assertEqual(cursor_mock.execute.call_count, 2)
        cursor_mock.execute.assert_called_with(
            " UPDATE human_dna_statistics SET " +
            "    count_mutant_dna = count_mutant_dna + 1, " +
            "    count_human_dna = count_human_dna + 1, " +
            "    ratio = CAST(CAST(count_mutant_dna + 1 AS DECIMAL(5,4)) / CAST((count_human_dna + 1) AS DECIMAL(5,4)) AS DECIMAL(5,4)); "
        )

    @patch('utils.database_utils.connect_to_database')
    def test_get_human_dna(self, connect_to_database_call):
        connection_mock = Mock()
        connect_to_database_call.return_value = connection_mock
        cursor_mock = connection_mock.cursor.return_value
        cursor_mock.execute.return_value = None
        cursor_mock.fetchone.return_value = [
            self.HUMAN_DNA_IS_MUTANT,
        ]
        
        result = mutant_repository.get_human_dna("ATCG,AACG,ATAG,ATCA")

        self.assertEqual(result, {
            "is_mutant": self.HUMAN_DNA_IS_MUTANT
        })
        self.assertEqual(cursor_mock.execute.call_count, 1)

    @patch('utils.database_utils.connect_to_database')
    def test_get_human_dna_statistics(self, connect_to_database_call):
        connection_mock = Mock()
        connect_to_database_call.return_value = connection_mock
        cursor_mock = connection_mock.cursor.return_value
        cursor_mock.execute.return_value = None
        cursor_mock.fetchone.return_value = [
            self.HUMAN_DNA_STATICTICS_MUTANT_COUNT,
            self.HUMAN_DNA_STATICTICS_HUMAN_COUNT,
            self.HUMAN_DNA_STATICTICS_RATIO
        ]
        
        result = mutant_repository.get_human_dna_statistics()

        self.assertEqual(result, {
            "count_mutant_dna": self.HUMAN_DNA_STATICTICS_MUTANT_COUNT,
            "count_human_dna": self.HUMAN_DNA_STATICTICS_HUMAN_COUNT,
            "ratio": self.HUMAN_DNA_STATICTICS_RATIO
        })
        self.assertEqual(cursor_mock.execute.call_count, 1)
