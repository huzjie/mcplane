from mcplane._version import __version__, __spec_version__


def test_version_is_set():
    assert __version__ == "1.0.0"


def test_spec_version():
    assert __spec_version__ == "2026-07-28"
