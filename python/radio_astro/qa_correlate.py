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

import numpy as np
from gnuradio import gr, gr_unittest, blocks
from correlate import correlate


class qa_correlate(gr_unittest.TestCase):
    def test_distinct_rows_in_flowgraph(self):
        block = correlate(2, 2)
        first = blocks.vector_source_c([1+1j, 2, 3, 4j], False, 2)
        second = blocks.vector_source_c([2, 1j, 5j, 2], False, 2)
        sink = blocks.vector_sink_c(6)
        tb = gr.top_block()
        tb.connect(first, (block, 0))
        tb.connect(second, (block, 1))
        tb.connect(block, sink)
        tb.run()
        expected = [2, 4, 2+2j, -2j, 4, 1, 9, 16, -15j, 8j, 25, 4]
        self.assertComplexTuplesAlmostEqual(expected, sink.data())

    def test_output_capacity(self):
        block = correlate(2, 2)
        inputs = [np.asarray([[1, 2], [9, 9]], dtype=np.complex64),
                  np.asarray([[3, 4], [9, 9]], dtype=np.complex64)]
        output = np.zeros((1, 6), dtype=np.complex64)
        self.assertEqual(block.work(inputs, [output]), 1)
        np.testing.assert_array_equal(output, [[1, 4, 3, 8, 9, 16]])



if __name__ == '__main__':
    gr_unittest.run(qa_correlate)
