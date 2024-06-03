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
import types
import unittest
from unittest.mock import AsyncMock

from lsst.ts import epm


class SnmpDataClientTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_snmp(self) -> None:
        log = logging.getLogger()
        for device_type in ["pdu", "scheiderPm5xxx", "xups"]:
            tel_topic = AsyncMock()
            tel_topic.DataType = types.SimpleNamespace()
            topics = types.SimpleNamespace(**{f"tel_{device_type}": tel_topic})
            config = types.SimpleNamespace(
                host="localhost",
                port=161,
                max_read_timeouts=5,
                device_name="TestDevice",
                device_type=device_type,
                poll_interval=0.1,
                location="UnitTest",
            )
            snmp_data_client = epm.SnmpDataClient(
                config=config, topics=topics, log=log, simulation_mode=1
            )
            await snmp_data_client.setup_reading()
            assert snmp_data_client.system_description == epm.SIMULATED_SYS_DESCR

            await snmp_data_client.read_data()
            tel_topic = getattr(topics, f"tel_{config.device_type}")
            tel_topic.set_write.assert_called_once()
