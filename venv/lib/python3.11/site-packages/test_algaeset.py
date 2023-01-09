
from pytest import fixture, raises

from .algaeset import *

@fixture
def C():
    return AlgaeSet.from_type(complex) | AlgaeSet.from_type(int) | AlgaeSet.from_type(float)

@fixture
def Im(C):
    return C.such_that(lambda e: e.imag == 0 if isinstance(e, complex) else False)

@fixture
def R(C):
    return C.such_that(lambda e: e.real == 0 if isinstance(e, complex) else True)

@fixture
def Z(R):
    return R.such_that(lambda e: e % 1 == 0)


class TestAlgaeSet:

    def test_finite_set_membership(self):
        s = AlgaeSet(1, 2, 3)
        assert 1 in s
        assert 2 in s
        assert 3 in s

    def test_complex_membership(self, C):
        assert 1 + 2j in C
        assert -1 + 2j in C
        assert 1 - 2j in C
        assert -1 - 2j in C
        assert 1.0 + 2.0j in C
        assert -1.0 + 2.0j in C
        assert 1.0 - 2.0j in C
        assert -1.0 - 2.0j in C

    def test_reals_membership(self, R):
        assert 1 in R
        assert 1.0 in R
        assert 0 in R
        assert -1.0 in R
        assert -1 in R

    def test_reals_non_membership(self, R):
        assert 1 + 2j not in R
        assert [1, 2, 3] not in R

    def test_integer_membership(self, Z):
        assert 1 in Z
        assert 0 in Z
        assert -1 in Z

    def test_infinite_set_equality(self):
        assert AlgaeSet.from_type(float) == AlgaeSet.from_type(float)

    def test_finite_set_equality(self): 
        assert AlgaeSet(1, 2, 3) == AlgaeSet(1, 2, 3)
        assert AlgaeSet(1, 2, 3) == AlgaeSet(3, 2, 1)
        assert AlgaeSet(1, 2, 3) == AlgaeSet(2, 1, 3)
        assert AlgaeSet(1, 2, 3) == AlgaeSet(2, 3, 1)
        assert AlgaeSet(1, 2, 3) == AlgaeSet(2, 2, 1, 1, 3, 3)

    def test_infinite_infinite_union(self, C):
        f_i = AlgaeSet.from_type(float) | AlgaeSet.from_type(int)
        i_f = AlgaeSet.from_type(int) | AlgaeSet.from_type(float)
        assert f_i == i_f
        assert i_f == f_i
        assert C | AlgaeSet.from_type(complex) == C
        assert AlgaeSet.from_type(complex) | C == C

    def test_infinite_finite_union(self, R):
        assert R | AlgaeSet(1.0, 2.0, 4.0) == R
        assert AlgaeSet(1.0, 2.0, 4.0) | R == R
        assert AlgaeSet(1j, 2j, 3j) | R == R | AlgaeSet(1j, 2j, 3j)

    def test_finite_finite_union(self):
        assert AlgaeSet(1, 2) | AlgaeSet(1, 2, 3) == AlgaeSet(1, 2, 3)
        assert AlgaeSet(1, 2, 3) | AlgaeSet(1, 2) == AlgaeSet(1, 2, 3)
        assert AlgaeSet(1, 1, 2, 2) | AlgaeSet(1, 2) == AlgaeSet(1, 2)
        assert AlgaeSet(1, 2) | AlgaeSet(1, 1, 2, 2) == AlgaeSet(1, 2)

    def test_finite_subset_of_finite_set(self):
        assert AlgaeSet(1, 2).is_subset(AlgaeSet(1, 2, 3, 4))
        assert AlgaeSet(1, 2, 3, 4).has_subset(AlgaeSet(1, 2))

    def test_infinite_subset_of_finite_set(self, R):
        assert not R.is_subset(AlgaeSet(1, 2, 3))

    def test_finite_subset_of_infinite_set(self, R):
        assert AlgaeSet(1, 2, 3).is_subset(R)
        assert AlgaeSet(1.0).is_subset(R)

        assert R.has_subset(AlgaeSet(1, 2, 3))
        assert R.has_subset(AlgaeSet(1.0))

    def test_infinite_subset_of_infinite_set(self, C, R, Z):
        assert R.is_subset(C)
        assert (R | AlgaeSet(1j, 2j, 3j)).is_subset(C)
        assert (AlgaeSet(1j, 2j, 3j) | R).is_subset(C)
        assert Z.is_subset(C)
        assert (Z | AlgaeSet(1.4, 2.4, 3.5)).is_subset(C)
        assert (AlgaeSet(1.4, 2.4, 3.5) | Z).is_subset(C)

        assert C.has_subset(R)
        assert C.has_subset(R | AlgaeSet(1j, 2j, 3j))
        assert C.has_subset(Z)
        assert C.has_subset(Z | AlgaeSet(1.4, 2.4, 3.5))

    def test_subset_check_admits_improper_subsets(self, R):
        assert AlgaeSet(1, 2, 3).is_subset(AlgaeSet(1, 2, 3))
        assert AlgaeSet(1, 2, 3).has_subset(AlgaeSet(1, 2, 3))
        assert R.is_subset(R)
        assert R.has_subset(R)
