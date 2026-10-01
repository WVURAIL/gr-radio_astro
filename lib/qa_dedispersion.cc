/* SPDX-License-Identifier: GPL-3.0-or-later */
#include <gnuradio/blocks/vector_sink.h>
#include <gnuradio/blocks/vector_source.h>
#include <gnuradio/radio_astro/dedispersion.h>
#include <gnuradio/top_block.h>
#include <iostream>
#include <vector>

bool check(const std::vector<float>& input, const std::vector<float>& expected,
           int nt, float dm, int max_batch)
{
    auto tb = gr::make_top_block("dedispersion_regression");
    auto source = gr::blocks::vector_source_f::make(input, false, 2 * nt);
    auto block = gr::radio_astro::dedispersion::make(2, dm, 1000, 200, 1, nt);
    auto sink = gr::blocks::vector_sink_f::make(nt);
    tb->connect(source, 0, block, 0);
    tb->connect(block, 0, sink, 0);
    tb->run(max_batch);
    if (sink->data() != expected) {
        std::cerr << "Incorrect dedispersion for nt=" << nt << ", dm=" << dm
                  << ", batch=" << max_batch << std::endl;
        return false;
    }
    return true;
}

int main()
{
    for (int batch : {1, 2, 4}) {
        if (!check({1, 2, 3, 4, 10, 20, 30, 40}, {3, 7, 30, 70}, 2, 0, batch))
            return 1;
    }
    if (!check({0, 10, 0, 20, 0, 30}, {30, 10, 20}, 3, 1, 2))
        return 1;
    if (!check({0, 10, 0, 20, 0, 30}, {20, 30, 10}, 3, 8, 2))
        return 1;
    return 0;
}
