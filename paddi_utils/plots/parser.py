import argparse
import matplotlib.pyplot as plt

class PlotArgumentParser(argparse.ArgumentParser):
	"""A default argument parser for plotting utilities"""

	def __init__(self):
		super(PlotArgumentParser, self).__init__()

		self.add_argument("files", nargs="*", default=None)
		self.add_argument("--output", default=None)
		self.add_argument("--format", default="paper")

		self.args = self.parse_args()

	def exit(self, fig):
		plt.style.use(self.args.format)

		plt.tight_layout()
		if self.args.output is None:
		    plt.show()
		else:
		    fig.savefig(args.output)