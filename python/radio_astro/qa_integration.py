#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Kevin Bandura.
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

import numpy as np
from gnuradio import gr, gr_unittest, blocks
from integration import integration


class qa_integration(gr_unittest.TestCase):
    def test_exact_window_and_batch(self):
        for inputs, expected in [([[1, 2], [3, 4]], [[2, 3]]),
                                 ([[1, 2], [3, 4], [5, 6], [7, 8]], [[2, 3], [6, 7]])]:
            block = integration(2, 2)
            output = np.full((len(expected), 2), -999, dtype=np.float32)
            produced = block.work([np.asarray(inputs, dtype=np.float32)], [output])
            self.assertEqual(produced, len(expected))
            np.testing.assert_array_equal(output, expected)

    def test_output_capacity_limits_consumption(self):
        block = integration(2, 2)
        output = np.full((1, 2), -999, dtype=np.float32)
        produced = block.work([np.asarray([[1, 2], [3, 4], [5, 6], [7, 8]],
                                         dtype=np.float32)], [output])
        self.assertEqual(produced, 1)
        np.testing.assert_array_equal(output, [[2, 3]])

    def test_changed_decimation_in_flowgraph(self):
        block = integration(2, 2)
        block.set_n_integrations(3)
        self.assertEqual(block.fixed_rate_noutput_to_ninput(2), 6)
        source = blocks.vector_source_f([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], False, 2)
        sink = blocks.vector_sink_f(2)
        tb = gr.top_block()
        tb.connect(source, block, sink)
        tb.run()
        self.assertFloatTuplesAlmostEqual((3, 4, 9, 10), sink.data())

    def test_invalid_integration_count(self):
        with self.assertRaises(ValueError):
            integration(2, 0)
        block = integration(2, 2)
        with self.assertRaises(ValueError):
            block.set_n_integrations(-1)
        self.assertEqual(block.fixed_rate_noutput_to_ninput(1), 2)


if __name__ == '__main__':
    gr_unittest.run(qa_integration)
