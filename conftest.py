import io
import os

import pytest

from robocop import Robocop


@pytest.fixture(scope="session")
def robocop_session():
    # kill ssltunnel
    # kill xpcshell
    # delete anrs
    # delete tombstones
    # stop process (app)
    # clear screenshots
    # clear logs
    # install robocop
    # setup local paths
    # build profile
    # start servers
    yield None
    # stop servers
    # stop application
    # pull logs/screenshots
    # remove profile/screenshots/logs/config


@pytest.fixture
def robocop_log(pytestconfig, tmpdir):
    log = str(tmpdir.join("robocop.log"))
    pytestconfig._robocop_log = log
    yield log


@pytest.fixture
def robocop(pytestconfig, robocop_session, robocop_log, fxa_account, monkeypatch):
    monkeypatch.setenv("FXA_EMAIL", fxa_account.email)
    monkeypatch.setenv("FXA_PASSWORD", fxa_account.password)
    app = pytestconfig.getoption("app")
    yield Robocop(app, robocop_log)


def pytest_addoption(parser):
    parser.addoption("--app", required=True, help="name of test app")


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    pytest_html = item.config.pluginmanager.getplugin("html")
    report.sections.append(("foo", "bar"))
    for log in ("Robocop",):
        attr = "_{}_log".format(log.lower())
        path = getattr(item.config, attr, None)
        if path is not None and os.path.exists(path):
            if pytest_html is not None:
                with io.open(path, "r", encoding="utf8") as f:
                    extra.append(pytest_html.extras.text(f.read(), log))
            report.sections.append((log, "Log: {}".format(path)))
    report.extra = extra
