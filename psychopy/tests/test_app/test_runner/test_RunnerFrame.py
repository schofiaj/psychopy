import pytest
import os
import time
from psychopy import prefs
import wx
from psychopy.app import psychopyApp


class Test_RunnerFrame:
    """
    This test opens Runner, and several processes.
    """
    def setup(self):
        self.tempFile = os.path.join(
            prefs.paths['tests'], 'data', 'test001EntryImporting.psyexp')

    def _getRunnerView(self, app):
        runner = app.newRunnerFrame()
        runner.clearTasks()
        return runner

    @pytest.mark.usefixtures("get_app")
    def test_RunnerFrame(self, get_app):
        app = get_app
        app.showRunner()

    @pytest.mark.usefixtures("get_app")
    def test_addFile(self, get_app):
        runner = self._getRunnerView(get_app)
        runner.addTask(fileName=self.tempFile)
        assert runner.panel.expCtrl.FindItem(-1, self.tempFile)

    @pytest.mark.usefixtures("get_app")
    def test_runLocal(self, get_app):
        """Run a local experiment file. Tests the `Job` module and expands
        coverage.
        """
        runner = self._getRunnerView(get_app)
        runner.Raise()

        # get panel with controls
        runnerPanel = runner.panel

        # add task
        runner.addTask(fileName=self.tempFile)
        runner.panel.expCtrl.Select(0)  # select only item

        # ---
        # Run a Builder experiment locally without interruption, check if the
        # UI is correctly updated.
        # ---

        # check button states before running the file
        assert runnerPanel.runBtn.Enabled, (
            "Incorrect button state for `Runner.panel.runBtn` at start of "
            "experiment.")
        assert not runnerPanel.stopBtn.Enabled, (
            "Incorrect button state for `Runner.panel.stopBtn` at start of "
            "experiment.")

        # issue a button click event to run the file
        wx.PostEvent(
            runnerPanel.runBtn.GetEventHandler(),
            wx.PyCommandEvent(wx.EVT_BUTTON.typeId,
                              runnerPanel.runBtn.GetId())
        )

        # wait until the the subprocess wakes up
        while runnerPanel.scriptProcess is None:
            time.sleep(0.01)
            wx.Yield()

        # check button states during experiment
        assert not runnerPanel.runBtn.Enabled, (
            "Incorrect button state for `Runner.panel.runBtn` during "
            "experiment.")
        assert runnerPanel.stopBtn.Enabled, (
            "Incorrect button state for `Runner.panel.stopBtn` during "
            "experiment.")

        # wait until the subprocess ends
        while runnerPanel.scriptProcess is not None:
            time.sleep(0.01)
            wx.Yield()

        # check button states after running the file, make sure they are
        # correctly restored
        assert runnerPanel.runBtn.Enabled, (
            "Incorrect button state for `Runner.panel.runBtn` at end of "
            "experiment.")
        assert not runnerPanel.stopBtn.Enabled, (
            "Incorrect button state for `Runner.panel.stopBtn` at end of "
            "experiment.")

        # ---
        # Run a Builder experiment locally, but interrupt it to see how well
        # the UI can handle that.
        # ---

        runner.panel.expCtrl.Select(0)

        # again, start the process using the run event
        wx.PostEvent(
            runnerPanel.runBtn.GetEventHandler(),
            wx.PyCommandEvent(wx.EVT_BUTTON.typeId,
                              runnerPanel.runBtn.GetId())
        )

        # wait until the the subprocess wakes up
        while runnerPanel.scriptProcess is None:
            time.sleep(0.01)
            wx.Yield()

        # kill the process a bit through it
        wx.PostEvent(
            runnerPanel.stopBtn.GetEventHandler(),
            wx.PyCommandEvent(wx.EVT_BUTTON.typeId,
                              runnerPanel.stopBtn.GetId())
        )

        # wait until the subprocess ends
        while runnerPanel.scriptProcess is not None:
            time.sleep(0.01)
            wx.Yield()

        # check button states after running the file, make sure they are
        # correctly restored
        assert runnerPanel.runBtn.Enabled, (
            "Incorrect button state for `Runner.panel.runBtn` at end of "
            "experiment.")
        assert not runnerPanel.stopBtn.Enabled, (
            "Incorrect button state for `Runner.panel.stopBtn` at end of "
            "experiment.")

        runner.clearTasks()  # clear task list

    @pytest.mark.usefixtures("get_app")
    def test_removeTask(self, get_app):
        runner = self._getRunnerView(get_app)
        runner.removeTask(runner.panel.currentSelection)
        assert runner.panel.expCtrl.FindItem(-1, self.tempFile) == -1

    @pytest.mark.usefixtures("get_app")
    def test_clearItems(self, get_app):
        runner = self._getRunnerView(get_app)
        runner.addTask(fileName=self.tempFile)
        runner.clearTasks()
        assert runner.panel.expCtrl.FindItem(-1, self.tempFile) == -1
