import easyvvuq as uq
import chaospy as cp
import os
import sys
import pytest
import logging
from pprint import pformat, pprint
from gauss.encoder_gauss import GaussEncoder
from gauss.decoder_gauss import GaussDecoder

__copyright__ = """

    Copyright 2018 Robin A. Richardson, David W. Wright

    This file is part of EasyVVUQ

    EasyVVUQ is free software: you can redistribute it and/or modify
    it under the terms of the Lesser GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    EasyVVUQ is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Lesser GNU General Public License for more details.

    You should have received a copy of the Lesser GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
__license__ = "LGPL"


# If cannonsim has not been built (to do so, run the Makefile in tests/cannonsim/src/)
# then skip this test
if not os.path.exists("tests/cannonsim/bin/cannonsim"):
    pytest.skip(
        "Skipping cannonsim test (cannonsim is not installed in tests/cannonsim/bin/)",
        allow_module_level=True)

cannonsim_path = os.path.realpath(os.path.expanduser("tests/cannonsim/bin/cannonsim"))

logging.basicConfig(level=logging.CRITICAL)


def test_cannonsim(tmpdir):
    # Define parameter space for the cannonsim app
    params = {
        "angle": {
            "type": "float",
            "min": 0.0,
            "max": 6.28,
            "default": 0.79},
        "air_resistance": {
            "type": "float",
            "min": 0.0,
            "max": 1.0,
            "default": 0.2},
        "height": {
            "type": "float",
            "min": 0.0,
            "max": 1000.0,
            "default": 1.0},
        "time_step": {
            "type": "float",
            "min": 0.0001,
            "max": 1.0,
            "default": 0.01},
        "gravity": {
            "type": "float",
            "min": 0.0,
            "max": 1000.0,
            "default": 9.8},
        "mass": {
            "type": "float",
            "min": 0.0001,
            "max": 1000.0,
            "default": 1.0},
        "velocity": {
            "type": "float",
            "min": 0.0,
            "max": 1000.0,
            "default": 10.0}}

    # Create an encoder and decoder for the cannonsim app
    encoder = uq.encoders.GenericEncoder(
        template_fname='tests/cannonsim/test_input/cannonsim.template',
        delimiter='#',
        target_filename='in.cannon')
    output_cols = ['Dist', 'lastvx', 'lastvy']
    decoder = uq.decoders.SimpleCSV(
        target_filename='output.csv', output_columns=output_cols, header=0)
    # Create a collation element for this campaign
    collater = uq.collate.AggregateByVariables(average=False)
    # Make a random sampler
    sweep = {
        "angle": [0.1, 0.2, 0.3],
        "height": [2.0, 10.0],
        "velocity": [10.0, 10.1, 10.2]
    }
    sampler = uq.sampling.BasicSweep(sweep=sweep)

    my_campaign = uq.Campaign(name='aggregate_by_var', work_dir=tmpdir)
    my_campaign.add_app(name="cannon_test",
                        params=params,
                        encoder=encoder,
                        decoder=decoder,
                        collater=collater)
    my_campaign.set_app("cannon_test")
    sampler = uq.sampling.BasicSweep(sweep=sweep)
    my_campaign.set_sampler(sampler)
    my_campaign.draw_samples()
    my_campaign.populate_runs_dir()

    actions = uq.actions.ExecuteLocal("tests/cannonsim/bin/cannonsim in.cannon output.csv")
    my_campaign.apply_for_each_run_dir(actions)
    my_campaign.collate()

    results = my_campaign.get_collation_result()
    assert 'Variable' in results.columns
    assert 'Value' in results.columns
    n_runs = sampler.count
    n_vars = len(output_cols)
    assert len(results) == n_runs * n_vars


if __name__ == "__main__":
    test_cannonsim('/tmp/')
