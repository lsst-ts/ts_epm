.. py:currentmodule:: lsst.ts.epm

.. _lsst.ts.epm-version_history:

###############
Version History
###############

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
