from unittest import TestCase
import dynclipy

class TestR2Py(TestCase):
    def test_data(self):
        data = dynclipy.ro.r("""
        list(
            matrix = matrix(runif(100), nrow = 10, ncol = 10),
            sparse_matrix = Matrix::sparseMatrix(i = sample(100), j = sample(100), x = runif(100)),
            nested_list = list(
                atom = 1,
                unnamed_list = list(
                    1, 2, 3
                ),
                named_list = list(
                    a = "1",
                    b = 2,
                    c = TRUE
                )
            )
        )
        """)

        self.assertTrue(dynclipy.check_conversion_rpy2py(data))