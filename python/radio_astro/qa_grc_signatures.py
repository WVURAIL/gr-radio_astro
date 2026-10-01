# SPDX-License-Identifier: GPL-3.0-or-later
from pathlib import Path
from types import SimpleNamespace
import yaml
from mako.template import Template
from gnuradio import gr_unittest
from correlate import correlate


class qa_grc_signatures(gr_unittest.TestCase):
    def test_grc_constructor_and_port_shapes(self):
        path = Path(__file__).resolve().parents[2] / 'grc/radio_astro_correlate.block.yml'
        spec = yaml.safe_load(path.read_text())
        parameters = {'n_inputs': 2, 'vec_length': 4}
        render = lambda value: Template(value).render(**parameters)
        block = eval(render(spec['templates']['make']),
                     {'radio_astro': SimpleNamespace(correlate=correlate)})
        self.assertEqual(int(render(spec['inputs'][0]['multiplicity'])), 2)
        self.assertEqual(int(render(spec['inputs'][0]['vlen'])), 4)
        self.assertEqual(int(render(spec['outputs'][0]['vlen'])), 12)
        self.assertEqual(len(block.in_sig().port_types(2)), 2)
        self.assertEqual(block.out_sig().port_types(1)[0].itemsize, 12 * 8)

    def test_dedispersion_port_shapes(self):
        path = Path(__file__).resolve().parents[2] / 'grc/radio_astro_dedispersion.block.yml'
        spec = yaml.safe_load(path.read_text())
        parameters = {'vec_length': 2, 'nt': 3, 'dms': 1, 'f_obs': 1000,
                      'bw': 200, 't_int': 1}
        render = lambda value: Template(value).render(**parameters)
        arguments = eval(render(spec['templates']['make']),
                         {'radio_astro': SimpleNamespace(dedispersion=lambda *args: args)})
        self.assertEqual(arguments, (2, 1, 1000, 200, 1, 3))
        self.assertEqual(int(render(spec['inputs'][0]['vlen'])), 6)
        self.assertEqual(int(render(spec['outputs'][0]['vlen'])), 3)


if __name__ == '__main__':
    gr_unittest.run(qa_grc_signatures)
