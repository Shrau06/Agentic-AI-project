import ast
import unittest
from pathlib import Path


class StockPageSyntaxTest(unittest.TestCase):
    def test_stock_page_has_valid_python_syntax(self):
        source = Path("modules/stock_page.py").read_text(encoding="utf-8")
        ast.parse(source)


if __name__ == "__main__":
    unittest.main() 
