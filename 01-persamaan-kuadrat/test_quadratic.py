import unittest
from io import StringIO
from unittest.mock import patch

from quadratic import main, solve_quadratic


class TestSolveQuadratic(unittest.TestCase):
    def test_not_quadratic_when_a_is_zero(self):
        self.assertEqual(solve_quadratic(0, 2, 1), ("bukan_persamaan_kuadrat", None))

    def test_two_distinct_real_roots(self):
        kind, roots = solve_quadratic(1, 0, -4)
        self.assertEqual(kind, "dua_akar_real")
        self.assertEqual(roots, (2.0, -2.0))

    def test_repeated_real_root(self):
        kind, roots = solve_quadratic(1, -2, 1)
        self.assertEqual(kind, "akar_real_kembar")
        self.assertEqual(roots, (1.0,))

    def test_complex_roots(self):
        kind, roots = solve_quadratic(1, 2, 5)
        self.assertEqual(kind, "dua_akar_kompleks")
        self.assertEqual(roots, (complex(-1, 2), complex(-1, -2)))


class TestInteractiveLoop(unittest.TestCase):
    def test_multiple_iterations_and_stop(self):
        # Iterasi 1: a=0, lanjut; iterasi 2: akar real berbeda, lanjut;
        # iterasi 3: akar kembar, lanjut; iterasi 4: akar kompleks, berhenti.
        values = iter([
            "0", "2", "1", "Y",
            "1", "0", "-4", "Y",
            "1", "-2", "1", "Y",
            "1", "2", "5", "N",
        ])
        output = StringIO()
        with patch("builtins.input", side_effect=lambda _: next(values)):
            with patch("sys.stdout", new=output):
                main()

        rendered = output.getvalue()
        self.assertIn("Bukan persamaan kuadrat", rendered)
        self.assertIn("dua akar real", rendered)
        self.assertIn("akar real kembar", rendered)
        self.assertIn("dua akar kompleks", rendered)
        self.assertIn("Program selesai.", rendered)
        self.assertEqual(rendered.count("PROGRAM PERSAMAAN KUADRAT"), 4)


if __name__ == "__main__":
    unittest.main()
