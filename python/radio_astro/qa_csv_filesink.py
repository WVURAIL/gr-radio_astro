#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 DSPIRA.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import datetime
from pathlib import Path
import tempfile
from unittest.mock import patch
import numpy as np
from gnuradio import gr_unittest
from csv_filesink import csv_filesink


class FixedClock:
    @staticmethod
    def now():
        return datetime.datetime(2026, 1, 1)


class qa_csv_filesink(gr_unittest.TestCase):
    def make_sink(self, directory, mode=0, scale=2, save='True'):
        return csv_filesink(2, 2e6, 100e6, str(directory) + '/', save,
                           mode, scale, '0', '90', 'test')

    def test_all_batch_rows_saved_without_overwriting(self):
        with tempfile.TemporaryDirectory() as directory:
            block = self.make_sink(directory)
            inputs = np.asarray([[1, 2], [3, 4], [5, 6]], dtype=np.float32)
            with patch('csv_filesink.datetime', FixedClock):
                self.assertEqual(block.work([inputs], []), 3)
                self.assertEqual(block.work([inputs[:1] + 6], []), 1)
            paths = list(Path(directory).glob('*_spectrum.csv'))
            self.assertEqual(len(paths), 4)
            saved = sorted(tuple(np.loadtxt(path, delimiter=',')[:, 1]) for path in paths)
            self.assertEqual(saved, [(1, 2), (3, 4), (5, 6), (7, 8)])

    def test_existing_capture_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            original = Path(directory) / '2026-01-01_00.00.00.0_test_0_90_spectrum.csv'
            original.write_text('previous capture')
            block = self.make_sink(directory)
            with patch('csv_filesink.datetime', FixedClock):
                block.work([np.asarray([[1, 2]], dtype=np.float32)], [])
            self.assertEqual(original.read_text(), 'previous capture')
            self.assertEqual(len(list(Path(directory).glob('*_spectrum.csv'))), 2)

    def test_long_mode_counts_every_input_row(self):
        with tempfile.TemporaryDirectory() as directory:
            block = self.make_sink(directory, mode=1, scale=2)
            with patch('csv_filesink.datetime', FixedClock):
                block.work([np.asarray([[1, 2], [3, 4], [5, 6]], dtype=np.float32)], [])
                block.work([np.asarray([[7, 8]], dtype=np.float32)], [])
            saved = sorted(tuple(np.loadtxt(path, delimiter=',')[:, 1])
                           for path in Path(directory).glob('*_spectrum.csv'))
            self.assertEqual(saved, [(3, 4), (7, 8)])

    def test_disabled_save_and_empty_batch(self):
        with tempfile.TemporaryDirectory() as directory:
            block = self.make_sink(directory, save='False')
            self.assertEqual(block.work([np.asarray([[1, 2]], dtype=np.float32)], []), 1)
            self.assertEqual(block.work([np.empty((0, 2), dtype=np.float32)], []), 0)
            self.assertEqual(list(Path(directory).iterdir()), [])


if __name__ == '__main__':
    gr_unittest.run(qa_csv_filesink)
