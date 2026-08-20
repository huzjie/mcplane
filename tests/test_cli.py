from mcplane.cli.main import build_parser, _cmd_version


def test_parser_has_commands():
    parser = build_parser()
    assert "version" in parser._subparsers._group_actions[0].choices


def test_version_runs(capsys):
    _cmd_version(None)
    out = capsys.readouterr().out
    assert "mcplane" in out
