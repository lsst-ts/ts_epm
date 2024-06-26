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
import math
import pathlib
import unittest
from unittest.mock import patch

from lsst.ts import epm, salobj
from lsst.ts.xml.component_info import ComponentInfo
from pysnmp.proto.rfc1902 import OctetString

TEST_DATA_DIR = pathlib.Path(__file__).parents[1].joinpath("tests", "data")
TEST_CONFIG_DIR = TEST_DATA_DIR / "config"
TEST_SNMP_DIR = TEST_DATA_DIR / "snmp"

DEVICE_TYPES = ["pdu", "scheiderPm5xxx", "xups"]


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

    async def validate_telemetry(self) -> None:
        component_info = ComponentInfo("EPM", "")

        for device_type in DEVICE_TYPES:
            topic_name = f"tel_{device_type}"
            topic = getattr(self.remote, topic_name)
            data = await self.assert_next_sample(topic)
            device_info = component_info.topics[topic_name]

            # TODO DM-45001 From XML 22.0 onward all EPM telemetry topics will
            #  have a systemDescription field so the if may be removed and the
            #  rest should be kept.
            if hasattr(data, "systemDescription"):
                system_description = getattr(data, "systemDescription")
                assert system_description == epm.SIMULATED_SYS_DESCR

            for array_field_name in device_info.array_fields:
                field_data = getattr(data, array_field_name)
                assert isinstance(field_data, list)
                array_field_length = device_info.array_fields[array_field_name]
                assert len(field_data) == array_field_length
                for i in range(array_field_length):
                    assert not math.isnan(field_data[i])

    async def test_snmp_data_clients(self) -> None:
        """Process telemetry generated by the `SnmpServerSimulator` class."""
        logging.info("test_snmp_data_clients")
        async with self.make_csc(
            initial_state=salobj.State.ENABLED,
            config_dir=TEST_CONFIG_DIR,
            simulation_mode=1,
        ):
            await self.validate_telemetry()

    async def test_snmp_data_clients_with_existing_data(self) -> None:
        """Process telemetry read from files.

        The files contain SNMP telemetry retrieved from real UPSs and PDUs.
        """
        # Read files with SNMP data.
        logging.info("test_snmp_data_clients_with_existing_data")
        self.snmp_data: dict[str, str] = {}
        for device_type in DEVICE_TYPES:
            filename = TEST_SNMP_DIR / f"{device_type}_output.txt"
            with open(filename) as f:
                lines = f.readlines()
            for line in lines:
                line = line.strip()
                items = line.split(":")
                self.snmp_data[items[0]] = ":".join(items[1:])

        # Patch functions so always the values read from file are returned.
        with (
            patch.object(
                epm.SnmpServerSimulator, "generate_integer", self.get_snmp_value
            ),
            patch.object(
                epm.SnmpServerSimulator, "generate_float", self.get_snmp_value
            ),
            patch.object(
                epm.SnmpServerSimulator, "generate_string", self.get_snmp_value
            ),
        ):
            async with self.make_csc(
                initial_state=salobj.State.ENABLED,
                config_dir=TEST_CONFIG_DIR,
                simulation_mode=1,
            ):
                await self.validate_telemetry()

    def get_snmp_value(self, oid: str) -> OctetString:
        """Get an SNMP value.

        All values eventually are transmitted as strings, so it is safe to use
        this method for all values read from file.

        Parameters
        ----------
        oid : `str`
            The OID to get an SNMP value for.

        Returns
        -------
        OctetString
            An SNMP OctetString object.
        """
        return OctetString(self.snmp_data[oid])
