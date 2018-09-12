import logging
import time

from mozdevice import ADBAndroid


logging.getLogger(__name__).addHandler(logging.NullHandler())


class Robocop(object):
    device = ADBAndroid()
    logger = logging.getLogger()

    def __init__(self, app, log):
        self.app = app
        self.log = log

    def run(self, identifier):
        # build browser environment
        # setup robotium config
        # setup remote profile
        # build browser args
        cmd = [
            "am",
            "instrument",
            "-e quit_and_finish 1",
            "-e deviceroot {}".format(self.device.test_root),
            "-e class org.mozilla.gecko.tests.{}".format(identifier),
            "org.mozilla.roboexample.test/org.mozilla.gecko.FennecInstrumentationTestRunner",
        ]
        self.device.clear_logcat()
        self.logger.info("Running: {}".format(" ".join(cmd)))
        self.device.shell(" ".join(cmd))

        # wait for process to end
        top = self.app
        while top == self.app:
            time.sleep(0.5)
            top = self.device.get_top_activity(timeout=60)

        log = "\n".join(self.device.get_logcat())
        with open(self.log, "w") as f:
            f.writelines(log)
        assert "Failed: 0" in log
