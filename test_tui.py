import sys
from unittest.mock import patch
from pathlib import Path
from pdfninja.tui import run_tui

# crie um pdf falso
test_pdf = Path("/tmp/test_single_file.pdf")
test_pdf.touch()

class MockPath:
    def ask(self):
        return str(test_pdf)

class MockSelect:
    def ask(self):
        return "Sair"

def mock_questionary_path(*args, **kwargs):
    return MockPath()

def mock_questionary_select(*args, **kwargs):
    return MockSelect()

with patch("questionary.path", mock_questionary_path):
    with patch("questionary.select", mock_questionary_select):
        try:
            run_tui()
        except SystemExit:
            print("Saiu normalmente.")
