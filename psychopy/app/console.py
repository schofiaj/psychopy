#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the PsychoPy library
# Copyright (C) 2002-2018 Jonathan Peirce (C) 2019-2021 Open Science Tools Ltd.
# Distributed under the terms of the GNU General Public License (GPL).


"""Classes and functions for broadcasting standard streams from external
consoles/terminals within the PsychoPy GUI suite.
"""

# This module can be expanded to centralize management for all console related
# actions in the future.
#

import sys


class StdStreamDispatcher(object):
    """Class for broadcasting standard output to text boxes.

    This class serves to redirect and log standard streams within the PsychoPy
    GUI suite, usually from sub-processes (e.g., a running script) to display
    somewhere. An instance of this class is created on-startup and referenced by
    the main application instance. Only one instance of this class can be
    created per-session (singleton).

    Parameters
    ----------
    app : :class:`~psychopy.app._psychopyApp.PsychoPyApp`
        Reference to the application instance.

    """
    # Developer note: In the future we should be able to attach other listeners
    # dynamically. Right now they are hard-coded, being the runner output box
    # and coder output panel. This will allow changes being made on those
    # objects not requiring any changes here.
    #
    _instance = None
    _initialized = False
    _app = None  # reference to parent app

    def __init__(self, app):
        # only setup if previously not instanced
        if not self._initialized:
            self._app = app
        else:
            raise RuntimeError(
                "Cannot create a new `psychopy.app.console.StdOutManager` "
                "instance. Already initialized.")

        self._initialized = True

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(StdStreamDispatcher, cls).__new__(cls)

        return cls._instance

    @classmethod
    def getInstance(cls):
        """Get the (singleton) instance of the `StdStreamDispatcher` class.

        Getting a reference to the `StdOutManager` class outside of the scope of
        the user's scripts should be done through this class method.

        Returns
        -------
        StdStreamDispatcher or None
            Instance of the `Mouse` class created by the user.

        """
        return cls._instance

    @classmethod
    def initialized(cls):
        """Check if this class has been initialized.

        Returns
        -------
        bool
            `True` if the `StdStreamDispatcher` class has been already
            instanced.

        """
        return cls._initialized

    def write(self, text):
        """Send text standard output to all listeners (legacy). This method is
        used for compatibility for older code. This makes it so an instance of
        this object looks like a ...

        Parameters
        ----------
        text : str
            Text to broadcast to all standard output windows.

        """
        self.broadcast(text=text)

    def broadcast(self, text):
        """Send text standard output to all listeners.

        Parameters
        ----------
        text : str
            Text to broadcast to all standard output windows.

        """
        # do nothing is the app isn't fully realized
        if not self._app.appLoaded:
            return

        coder = self._app.coder
        if coder is not None:
            if hasattr(coder, 'consoleOutput'):
                pass   # write output to coder output window

        runner = self._app.runner
        if runner is not None:
            runner.write(text)

    def clear(self):
        """Clear all output windows."""
        # do nothing is the app isn't fully realized
        if not self._app.appLoaded:
            return

        coder = self._app.coder
        if coder is not None:
            if hasattr(coder, 'consoleOutput'):
                pass   # write output to coder output window

        runner = self._app.runner
        if runner is not None:
            runner.Clear()


if __name__ == "__main__":
    pass
