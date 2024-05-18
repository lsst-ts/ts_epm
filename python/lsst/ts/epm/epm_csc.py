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

__all__ = ["EpmCsc", "run_epm"]

import asyncio

from lsst.ts import salobj
from lsst.ts.ess.csc import EssCsc

from . import __version__
from .config_schema import CONFIG_SCHEMA


def run_epm() -> None:
    asyncio.run(EpmCsc.amain(index=True))


class EpmCsc(EssCsc):
    """Upper level Commandable SAL Component for the Electrical Power Manager.

    Parameters
    ----------
    index : `int`
        The index of the CSC.
    config_dir : `str`
        The configuration directory.
    initial_state : `salobj.State`
        The initial state of the CSC.
    simulation_mode : `int`
        Simulation mode (1) or not (0).
    override : `str`, optional
        Configuration override file to apply if ``initial_state`` is
        `State.DISABLED` or `State.ENABLED`.
    """

    version = __version__

    def __init__(
        self,
        index: int,
        config_dir: str | None = None,
        initial_state: salobj.State = salobj.State.STANDBY,
        simulation_mode: int = 0,
        override: str = "",
    ) -> None:

        super().__init__(
            name="EPM",
            index=index,
            config_schema=CONFIG_SCHEMA,
            config_dir=config_dir,
            initial_state=initial_state,
            simulation_mode=simulation_mode,
            override=override,
        )

        # TODO DM-44354 Add a new SNMP DataClient that gets the telemetry and
        #  sends the SAL messages.

    @staticmethod
    def get_config_pkg() -> str:
        return "ts_config_ocs"
