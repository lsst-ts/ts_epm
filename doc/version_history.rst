.. py:currentmodule:: lsst.ts.epm

.. _lsst.ts.epm-version_history:

###############
Version History
###############

v0.3.2
======
* Pin pyasn1 to 0.6.0 in conda recipe.

v0.3.1
======
* Pin pysnmp to 4.4.12 in conda recipe.

v0.3.0
======

* Remove backward compatibility with XML 21.0.

Requires:

* ts_salobj 7
* ts_idl 4.7.1
* IDL file for EPM from ts_xml 22
* ts_ess_csc
* ts_ess_common
* ts_tcpip
* ts_utils

v0.2.0
======

* Run the blocking `execute_next_cmd` command in an asyncio loop.
* Reduce frequently occurring warning log messages to debug.

Requires:

* ts_salobj 7
* ts_idl 4.7.1
* IDL file for EPM from ts_xml 21
* ts_ess_csc
* ts_ess_common
* ts_tcpip
* ts_utils

v0.1.3
======

* Support configurable SNMP community.
* Removed unused location configuration item.
* Add more TelemetryItem values.
* Add support for XML 22.0 array fields.

Requires:

* ts_salobj 7
* ts_idl 4.7.1
* IDL file for EPM from ts_xml 21
* ts_ess_csc
* ts_ess_common
* ts_tcpip
* ts_utils

v0.1.2
======

* Improve reading of MIB files.
* Improve simulating and processing of telemetry.

Requires:

* ts_salobj 7
* ts_idl 4.7.1
* IDL file for EPM from ts_xml 21
* ts_ess_csc
* ts_ess_common
* ts_tcpip
* ts_utils

v0.1.1
======

* Reading telemetry from Schneider UPS-es now works.
* Add temporary handling of list items.

Requires:

* ts_salobj 7
* ts_idl 4.7.1
* IDL file for EPM from ts_xml 21
* ts_ess_csc
* ts_ess_common
* ts_tcpip
* ts_utils

v0.1.0
======

First release of the Electrical Power Manager CSC.

* A basic EPM CSC.
* A DataClient that retrieves telemetry via SNMP and that sends SAL telemetry messages.

Requires:

* ts_salobj 7
* ts_idl 4.7.1
* IDL file for EPM from ts_xml 21
* ts_ess_csc
* ts_ess_common
* ts_tcpip
* ts_utils
