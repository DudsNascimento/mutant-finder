import unittest

import mutant_service
from unittest.mock import patch, Mock

class TestMutantService(unittest.TestCase):

    HUMAN_DNA_STATICTICS_MUTANT_COUNT = 1
    HUMAN_DNA_STATICTICS_HUMAN_COUNT = 2
    HUMAN_DNA_STATICTICS_RATIO = 0.5

    @patch('mutant_repository.get_human_dna_statistics')
    def test_get_human_dna_statistics(self, get_human_dna_statistics_call):
        get_human_dna_statistics_call.return_value = {
            "count_mutant_dna": self.HUMAN_DNA_STATICTICS_MUTANT_COUNT,
            "count_human_dna": self.HUMAN_DNA_STATICTICS_HUMAN_COUNT,
            "ratio": self.HUMAN_DNA_STATICTICS_RATIO
        }
        
        result = mutant_service.get_human_dna_statistics()

        self.assertEqual(result, {
            "count_mutant_dna": self.HUMAN_DNA_STATICTICS_MUTANT_COUNT,
            "count_human_dna": self.HUMAN_DNA_STATICTICS_HUMAN_COUNT,
            "ratio": self.HUMAN_DNA_STATICTICS_RATIO
        })
        self.assertEqual(get_human_dna_statistics_call.call_count, 1)

    @patch('mutant_repository.get_human_dna')
    @patch('mutant_repository.save_human_dna_and_update_human_dna_statistics')
    def test_process_human_dna_1(self, save_human_dna_and_update_human_dna_statistics_call, get_human_dna_call):
        get_human_dna_call.return_value = None
        save_human_dna_and_update_human_dna_statistics_call.return_value = None
        
        result = mutant_service.process_human_dna([
            'ATCT',
            'TACA',
            'AAGA',
            'CTCA'
        ], 4)

        self.assertEqual(result, False)
        self.assertEqual(get_human_dna_call.call_count, 1)
        self.assertEqual(save_human_dna_and_update_human_dna_statistics_call.call_count, 1)
        save_human_dna_and_update_human_dna_statistics_call.assert_called_with(4,
            'ATCT,TACA,AAGA,CTCA',
            False)

    @patch('mutant_repository.get_human_dna')
    @patch('mutant_repository.save_human_dna_and_update_human_dna_statistics')
    def test_process_human_dna_2(self, save_human_dna_and_update_human_dna_statistics_call, get_human_dna_call):
        get_human_dna_call.return_value = None
        save_human_dna_and_update_human_dna_statistics_call.return_value = None
        
        result = mutant_service.process_human_dna([
            'TTCA',
            'TACA',
            'AAAA',
            'CTCA'
        ], 4)

        self.assertEqual(result, True)
        self.assertEqual(get_human_dna_call.call_count, 1)
        self.assertEqual(save_human_dna_and_update_human_dna_statistics_call.call_count, 1)
        save_human_dna_and_update_human_dna_statistics_call.assert_called_with(4,
            'TTCA,TACA,AAAA,CTCA',
            True)

    @patch('mutant_repository.get_human_dna')
    @patch('mutant_repository.save_human_dna_and_update_human_dna_statistics')
    def test_process_human_dna_3(self, save_human_dna_and_update_human_dna_statistics_call, get_human_dna_call):
        get_human_dna_call.return_value = None
        save_human_dna_and_update_human_dna_statistics_call.return_value = None
        
        result = mutant_service.process_human_dna([
            'ATCA',
            'TACA',
            'ATAA',
            'CTCA'
        ], 4)

        self.assertEqual(result, True)
        self.assertEqual(get_human_dna_call.call_count, 1)
        self.assertEqual(save_human_dna_and_update_human_dna_statistics_call.call_count, 1)
        save_human_dna_and_update_human_dna_statistics_call.assert_called_with(4,
            'ATCA,TACA,ATAA,CTCA',
            True)

    @patch('mutant_repository.get_human_dna')
    @patch('mutant_repository.save_human_dna_and_update_human_dna_statistics')
    def test_process_human_dna_4(self, save_human_dna_and_update_human_dna_statistics_call, get_human_dna_call):
        get_human_dna_call.return_value = None
        save_human_dna_and_update_human_dna_statistics_call.return_value = None
        
        result = mutant_service.process_human_dna([
            'ATCA',
            'TAAA',
            'AAAT',
            'ATCA'
        ], 4)

        self.assertEqual(result, True)
        self.assertEqual(get_human_dna_call.call_count, 1)
        self.assertEqual(save_human_dna_and_update_human_dna_statistics_call.call_count, 1)
        save_human_dna_and_update_human_dna_statistics_call.assert_called_with(4,
            'ATCA,TAAA,AAAT,ATCA',
            True)

    @patch('mutant_repository.get_human_dna')
    @patch('mutant_repository.save_human_dna_and_update_human_dna_statistics')
    def test_process_human_dna_4_again(self, save_human_dna_and_update_human_dna_statistics_call, get_human_dna_call):
        get_human_dna_call.return_value = {
            "is_mutant": True
        }
        
        result = mutant_service.process_human_dna([
            'ATCA',
            'TAAA',
            'AAAT',
            'ATCA'
        ], 4)

        self.assertEqual(result, True)
        self.assertEqual(get_human_dna_call.call_count, 1)
        self.assertEqual(save_human_dna_and_update_human_dna_statistics_call.call_count, 0)
