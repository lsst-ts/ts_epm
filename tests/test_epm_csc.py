# This file is part of ts_epm.
#
# Developed for the Vera Rubin Observatory Telescope and Site Systems.
# This product includes software developed by the Vera Rubin Observatory
# Project (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import pathlib
import unittest

from lsst.ts import epm, salobj

TEST_CONFIG_DIR = pathlib.Path(__file__).parents[1].joinpath("tests", "data", "config")


class CscTestCase(salobj.BaseCscTestCase, unittest.IsolatedAsyncioTestCase):
    def basic_make_csc(
        self,
        initial_state: salobj.State | int,
        config_dir: str | pathlib.Path | None,
        index: int = 1,
        simulation_mode: int = 1,
        override: str = "",
    ) -> salobj.BaseCsc:
        logging.info("basic_make_csc")
        epm_csc = epm.EpmCsc(
            initial_state=initial_state,
            config_dir=config_dir,
            simulation_mode=simulation_mode,
            index=index,
            override=override,
        )
        return epm_csc

    async def test_standard_state_transitions(self) -> None:
        logging.info("test_standard_state_transitions")
        async with self.make_csc(
            initial_state=salobj.State.STANDBY,
            config_dir=TEST_CONFIG_DIR,
            simulation_mode=1,
        ):
            await self.check_standard_state_transitions(enabled_commands=())

    async def test_version(self) -> None:
        logging.info("test_version")
        async with self.make_csc(
            initial_state=salobj.State.STANDBY,
            config_dir=None,
            simulation_mode=1,
        ):
            await self.assert_next_sample(
                self.remote.evt_softwareVersions,
                cscVersion=epm.__version__,
                subsystemVersions="",
            )

    async def test_bin_script(self) -> None:
        logging.info("test_bin_script")
        await self.check_bin_script(name="EPM", index=1, exe_name="run_epm")

    async def test_snmp_data_clients(self) -> None:
        async with self.make_csc(
            initial_state=salobj.State.ENABLED,
            config_dir=TEST_CONFIG_DIR,
            simulation_mode=1,
        ):
            data = await self.assert_next_sample(self.remote.tel_pdu)
            assert isinstance(data.powerOutletStatus, list)
            await self.assert_next_sample(
                self.remote.tel_scheiderPm5xxx,
                systemDescription=epm.SIMULATED_SYS_DESCR,
            )
            await self.assert_next_sample(
                self.remote.tel_xups,
                systemDescription=epm.SIMULATED_SYS_DESCR,
            )
