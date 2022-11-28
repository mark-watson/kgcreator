import spacy
from os import system
system("python -m spacy download en_core_web_sm")

from click.testing import CliRunner
from kgcreator.cli import cli


def test_version():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert result.output.startswith("cli, version ")
