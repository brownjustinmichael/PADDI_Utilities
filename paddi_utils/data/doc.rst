:mod:`data` Module
******************

.. module:: paddi_utils.data

This module contains the means to read output data from a PADDI run. The basic use of this module is in the indexing methods of the :class:`.Diagnostic`, the :class:`.Dump`, the :class:`.Profile`, and the :class:`.Spectra` classes. We outline their construction and use here.

The most basic object here is the :class:`.Parameters` object, which reads and contains the parameters used for a particular run.::

	from paddi_utils.data import Parameters

	# Load the object from the file
	params = Parameters("location/of/parameter_file")

	# Parameters are stored as attributes
	params.max_degrees_of_x_fourier_modes


To access the attributes of a PADDI diagnostic file (e.g., "OUT01"), construct a :class:`.Diagnostic` object.::

	from paddi_utils.data import Diagnostic

	# Load the object from the file
	diagnostic = Diagnostic(["location/of/file1", "location/of/file2", ...])
	# ... or ...
	diagnostic = Diagnostic(glob.glob("location/of/files*"))

	# Index the Diagnostic object like a pandas dataframe
	diagnostic["flux_Chem"][100:]
	diagnostic.iloc[100:]["flux_Chem"]

.. toctree::
   :maxdepth: 2

:mod:`data.parameters` Module
-----------------------------
.. automodule:: paddi_utils.data.parameters
	:members:
	:special-members:
	:show-inheritance:

:mod:`data.diagnostic` Module
-----------------------------
.. automodule:: paddi_utils.data.diagnostic
	:members:
	:special-members:
	:show-inheritance:

:mod:`data.dump` Module
-----------------------
.. automodule:: paddi_utils.data.dump
	:members:
	:special-members:
	:show-inheritance:

:mod:`data.profile` Module
--------------------------
.. automodule:: paddi_utils.data.profile
	:members:
	:special-members:
	:show-inheritance:

:mod:`data.spectra` Module
--------------------------
.. automodule:: paddi_utils.data.spectra
	:members:
	:special-members:
	:show-inheritance: