import argparse
import matplotlib.pyplot as plt

class PlotArgumentParser(argparse.ArgumentParser):
	"""
	A default argument parser for plotting utilities. This behaves much like the :class:`argparse.ArgumentParser` class. The basic use of this class is as follows::

		import matplotlib.pyplot as plt

		from paddi_utils.plots import PlotArgumentParser
		from paddi_utils.data import OutputType

		parser = PlotArgumentParser()
		parser.add_argument(...)

		args = parser.parse_args()

		data = OutputType(args.files)

		plt.plot(data["x"], data["y"])

		parser.exit(fig)

	This will output to the file specified at the command line for "--output". If no argument is given, it will bring up the matplotlib GUI. The command line argument "--style" will search your matplotlib style files for one of the same name.
	"""

	def __init__(self):
		super(PlotArgumentParser, self).__init__()

		# Add the basic arguments of the plot
		self.add_argument("files", nargs="*", default=tuple())
		self.add_argument("--output", default=None)
		self.add_argument("--style", default=None)

	def save(self, fig):
		# Read the command line arguments
		args = self.parse_args()

		# Load the matplotlib style if provided
		if args.style is not None:
			plt.style.use(args.style)

		# Output either to file or to the GUI
		plt.tight_layout()
		if args.output is None:
		    plt.show()
		else:
		    fig.savefig(args.output)