"""
Demonstrates how to make a plot without ever importing matplotlib.pyplot.

Notes
-----
#.  Written by David C. Stauffer in April 2017.
"""

# %% Imports
import os

import numpy as np
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget

from dstauffman import close_all, get_images_dir

# %% Constants
plt = None


# %% Classes - _HoverButton
class _HoverButton(QPushButton):
    r"""Custom button that allows hovering and icons."""

    def __init__(self, *args, **kwargs):
        # initialize
        super().__init__(*args, **kwargs)
        # Enable mouse hover event tracking
        self.setMouseTracking(True)
        self.setStyleSheet("border: 0px;")
        # set icon
        for this_arg in args:
            if isinstance(this_arg, QIcon):
                self.setIcon(this_arg)
                self.setIconSize(QSize(24, 24))

    def enterEvent(self, event):
        # Draw border on hover
        self.setStyleSheet("border: 1px; border-style: solid;")  # pragma: no cover

    def leaveEvent(self, event):
        # Delete border after hover
        self.setStyleSheet("border: 0px;")  # pragma: no cover


# %% Classes - MyCustomToolbar
class MyCustomToolbar:
    r"""
    Defines a custom toolbar to use in any matplotlib plots.

    Examples
    --------
    >>> from dstauffman import MyCustomToolbar
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> fig = plt.figure()
    >>> fig.canvas.manager.set_window_title('Figure Title')
    >>> ax = fig.add_subplot(111)
    >>> x = np.arange(0, 10, 0.1)
    >>> y = np.sin(x)
    >>> _ = ax.plot(x, y)
    >>> fig.toolbar_custom_ = MyCustomToolbar(fig)

    Close plot
    >>> plt.close(fig)

    """

    def __init__(self, toolbar):
        r"""Initializes the custom toolbar."""
        # create buttons - Prev Plot
        icon = QIcon(os.path.join(get_images_dir(), "prev_plot.png"))
        self.btn_prev_plot = _HoverButton(icon, "")
        self.btn_prev_plot.setToolTip("Show the previous plot")
        fig.canvas.toolbar.addWidget(self.btn_prev_plot)
        self.btn_prev_plot.clicked.connect(self.prev_plot)
        # create buttons - Next Plot
        icon = QIcon(os.path.join(get_images_dir(), "next_plot.png"))
        self.btn_next_plot = _HoverButton(icon, "")
        self.btn_next_plot.setToolTip("Show the next plot")
        fig.canvas.toolbar.addWidget(self.btn_next_plot)
        self.btn_next_plot.clicked.connect(self.next_plot)
        # create buttons - Close all
        icon = QIcon(os.path.join(get_images_dir(), "close_all.png"))
        self.btn_close_all = _HoverButton(icon, "")
        self.btn_close_all.setToolTip("Close all the open plots")
        fig.canvas.toolbar.addWidget(self.btn_close_all)
        self.btn_close_all.clicked.connect(self._close_all)

    def _close_all(self, *args):
        r"""Closes all the currently open plots."""
        close_all()

    def next_plot(self, *args):
        r"""Brings up the next plot in the series."""
        # get all the figure numbers
        all_figs = plt.get_fignums()
        # get the active figure number
        this_fig = plt.gcf()
        # loop through all the figures
        for i in range(len(all_figs)):
            # find the active figure within the list
            if this_fig == all_figs[i]:
                # find the next figure, with allowances for rolling over the list
                if i < len(all_figs) - 1:
                    next_fig = all_figs[i + 1]
                else:
                    next_fig = all_figs[0]
        # set the appropriate active figure
        fig = plt.figure(next_fig)
        # make it the active window
        fig.canvas.manager.window.raise_()

    def prev_plot(self, *args):
        r"""Brings up the previous plot in the series."""
        # get all the figure numbers
        all_figs = plt.get_fignums()
        # get the active figure number
        this_fig = plt.gcf()
        # loop through all the figures
        for i in range(len(all_figs)):
            # find the active figure within the list
            if this_fig == all_figs[i]:
                # find the next figure, with allowances for rolling over the list
                if i > 0:
                    prev_fig = all_figs[i - 1]
                else:
                    prev_fig = all_figs[-1]
        # set the appropriate active figure
        fig = plt.figure(prev_fig)
        # make it the active window
        fig.canvas.manager.window.raise_()


# %% Script
if __name__ == "__main__":
    # data
    time = np.arange(0, 10)
    data = np.sin(time)
    this_title = "Sin vs. Time"

    # create GUI for figure
    frame = QMainWindow()
    gui_widget = QWidget(frame)
    frame.setCentralWidget(gui_widget)
    layout = QVBoxLayout(gui_widget)

    # create figure
    fig = Figure()
    fig.canvas = FigureCanvas(fig)
    fig.canvas.manager.set_window_title(this_title)
    fig.canvas.toolbar = NavigationToolbar(fig.canvas, frame)

    # add figure to GUI
    layout.addWidget(fig.canvas.toolbar)
    layout.addWidget(fig.canvas)

    # add an axis and plot the data
    ax = fig.add_subplot(111)
    ax.plot(time, data, ".-", label="Sin")

    # add labels and legends
    ax.set_xlabel("Time")
    ax.set_ylabel("Amp")
    ax.set_title(this_title)

    # show legend
    ax.legend()
    # show a grid
    ax.grid(True)

    # add a custom toolbar
    fig.toolbar_custom_ = MyCustomToolbar(fig.canvas.toolbar)

    # show the plot
    frame.show()
