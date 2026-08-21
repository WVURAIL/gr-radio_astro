#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 Kevin Bandura.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, gr_unittest
# from gnuradio import blocks
from gnuradio.radio_astro import running_norm_std

class qa_running_norm_std(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_instance(self):
        # One vector of 1024 floats, keeping 8 of them for the running standard
        # deviation. intype is one of complex/float/int, as declared in
        # grc/radio_astro_running_norm_std.block.yml.
        instance = running_norm_std(float, 1024, 8)
        self.assertEqual(instance.vec_length, 1024)
        self.assertEqual(instance.running_length, 8)
        self.assertEqual(instance.data_history.shape, (8, 1024))

    def test_instance_rejects_unknown_type(self):
        # The constructor raises for anything that is not complex, float or int.
        self.assertRaises(Exception, running_norm_std, str, 1024, 8)

    def test_001_descriptive_test_name(self):
        # set up fg
        self.tb.run()
        # check data


if __name__ == '__main__':
    gr_unittest.run(qa_running_norm_std)
