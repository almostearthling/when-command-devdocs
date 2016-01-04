==========
Test Suite
==========

As of version *0.7.0-beta.1* **When** has an automated test suite. The test
suite does not come packaged with the applet, since it wouldn't be useful
to install the test scripts on the user machine: instead, it's stored in its
dedicated repository_, see the specific ``README.md`` file for more details.

Whenever a new feature is added, that affects the *background* part of
**When** (i.e. the loop that checks conditions and possibly runs tasks),
specific tests should be added using the test suite "tools", that is:

* the configurable *items* export file
* the *ad hoc* configuration file
* the test functions in ``run.sh``.

It has to be noted that, at least for now, the test suite is only concerned
about *function* and not *performance*: since **When** is a rather lazy
applet, performance in terms of speed is not a top requirement.

.. _repository: https://github.com/almostearthling/when-command-testsuite.git
