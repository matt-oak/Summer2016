#OpenTopo Downloader Unit Tests

from OpenTopoDL import *
from unittest import TestCase
from mock import patch
import unittest
import sys

class TestOpenTopoDL(unittest.TestCase):

	def test_invalid_dataset_number(self):
		sys.argv = ['OpenTopoDL.py', 'l', '999']
		self.assertRaises(IndexError, lambda: execfile('OpenTopoDL.py'))

	def test_invalid_dataset_type(self):
		sys.argv = ['OpenTopoDL.py', 'x', '2']
		self.assertRaises(Exception, lambda: execfile('OpenTopoDL.py'))

	def test_lidar_request(self):
		with patch('__builtin__.raw_input', return_value = 'l') as _raw_input:
			self.assertEqual(lidar_vs_raster(), 'PC_Bulk')
			_raw_input.assert_called_once_with('Download [L]idar Point Cloud or [R]aster data: ')

	def test_raster_request(self):
		with patch('__builtin__.raw_input', return_value = 'R') as _raw_input:
			self.assertEqual(lidar_vs_raster(), 'Raster')
			_raw_input.assert_called_once_with('Download [L]idar Point Cloud or [R]aster data: ')


def main():
    unittest.main()

if __name__ == '__main__':
    main()
