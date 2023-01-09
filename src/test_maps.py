
from maps import *

import math
import cmath
from pytest import raises

from algaeset import C, R, Z, N
from properties import *


class TestMapping:

	def test_accepts_lambdas(self):
		assert Mapping(lambda x: x**2, [R], [R])

	def test_accepts_functions(self):
		def f(x):
			return x**2
		assert Mapping(f, [R], [R])

	def test_checks_domains(self):
		m = Mapping(lambda a, b, c: a, [R, Z, N], [R])
		assert m(1, 2, 3) == 1
		assert m(math.pi, -14, 12) == math.pi
		with raises(DomainError):
			assert m(12j, -14, 12)
		with raises(DomainError):
			assert m(math.pi, math.pi, 12)
		with raises(DomainError):
			assert m(math.pi, -14, -12)

	def test_checks_codomains(self):
		m = Mapping(lambda a: cmath.sqrt(a), [R], [R])
		assert m(9) == 3
		with raises(DomainError):
			assert m(-9) == 3j


class TestEndomorphism:

	def test_domain_codomain_equality(self):
		endo = Endomorphism(lambda _: 1, R)
		assert endo.domain == endo.range


class TestClosedOperation:

	def test_domain_codomain_equality(self):
		add = BinaryOperation(lambda a, b: a + b, R, R)
		assert add.domain == add.range

	def test_unclosed_operation_raises_domain_error(self):
		sqrt = BinaryOperation(lambda a, b: cmath.sqrt(a), R, R)
		assert sqrt(4, 1) == 2
		with raises(DomainError):
			assert sqrt(-9, 1) == 3j


class TestAssociativeOperation:

	def test_is_associative(self):
		add = AssociativeOperation(lambda a, b: a + b, R, R)
		assert add(1, 2) == 3
		assert add(4, 5) == 9

	def test_not_associative(self):
		sub = AssociativeOperation(lambda a, b: a - b, R, R)
		with raises(AssociativityError):
			assert sub(1, 2) == -1
			assert sub(12, 3) == 9


class TestCommutativeOperation:

	def test_is_commutative(self):
		add = CommutativeOperation(lambda a, b: a + b, R, R)
		assert add(1, 2) == 3

	def test_not_commutative(self):
		sub = CommutativeOperation(lambda a, b: a - b, R, R)
		with raises(CommutativityError):
			assert sub(5, 3) == 2


class TestAbelianOperation:
	
	def test_is_abelian(self):
		add = AbelianOperation(lambda a, b: a + b, R, R)
		assert add(1, 2) == 3

	def test_not_abelian(self):
		sub = AbelianOperation(lambda a, b: a - b, R, R)
		with raises(CommutativityError):
			assert sub(5, 3) == 2


class TestIndempotentOperation:

	def test_is_indempotent(self):
		same = IndempotentOperation(lambda a, b: a, R, R)
		assert same(1, 2) == 1
		assert same(4, 3) == 4

	def test_not_indempotent(self):
		not_same = IndempotentOperation(lambda a, b: (a + b)/3, R, R)
		with raises(IndempotencyError):
			assert not_same(1, 3)


class TestIdentityOperation:

	def test_has_identity(self):
		add = IdentityOperation(lambda a, b: a + b, R, R, identity=0)
		assert add(12, 13) == 25
		assert add(221, 2) == 223

	def test_lacks_identity(self):
		bad_add = IdentityOperation(lambda a, b: a + b, R, R, identity=1)
		with raises(IdentityError):
			assert bad_add(2, 3) == 5


class TestInvertibleOperation:

	def test_subclasses_IdentityOperation(self):
		add = InvertibleOperation(
			lambda a, b: a + b, 
			BinaryOperation(lambda a, b: a - b, R, R), 
			R, R, 0
		)
		assert isinstance(add, IdentityOperation)

	def test_is_invertible(self):
		add = InvertibleOperation(
			lambda a, b: a + b, 
			BinaryOperation(lambda a, b: a - b, R, R), 
			R, R, 0
		)
		assert add(12, 13) == 25
		assert add(3, 5) == 8

	def test_not_invertible(self):
		bad_add = InvertibleOperation(
			lambda a, b: a + b, 
			BinaryOperation(lambda a, b: a * b, R, R), 
			R, R, 0
		)
		with raises(InvertibilityError):
			assert bad_add(12, 13) == 25
			assert bad_add(3, 5) == 8

	def test_requires_valid_identity(self):
		bad_add = InvertibleOperation(
			lambda a, b: a + b, 
			BinaryOperation(lambda a, b: a - b, R, R), 
			R, R, 1
		)
		with raises(IdentityError):
			assert bad_add(12, 4) == 16

	def test_requires_valid_inverse_operation(self):
		bad_add = InvertibleOperation(
			lambda a, b: a + b, 
			BinaryOperation(lambda a, b: a + b, R, R), 
			R, R, 0
		)
		with raises(InvertibilityError):
			assert bad_add(12, 13) == 25


class TestGroupOperation:

	def test_subclasses_InvertibleOperation(self):
		add = GroupOperation(
			lambda a, b: a + b, 
			BinaryOperation(lambda a, b: a - b, R, R), 
			R, 0
		)
		assert isinstance(add, InvertibleOperation)

	def test_subclasses_IdentityOperation(self):
		add = GroupOperation(
			lambda a, b: a + b, 
			BinaryOperation(lambda a, b: a - b, R, R), 
			R, 0
		)
		assert isinstance(add, IdentityOperation)

	def test_subclasses_AssociativeOperation(self):
		add = GroupOperation(
			lambda a, b: a + b, 
			BinaryOperation(lambda a, b: a - b, R, R), 
			R, 0
		)
		assert isinstance(add, AssociativeOperation)

	def test_is_invertible(self):
		add = GroupOperation(
			lambda a, b: a + b, 
			BinaryOperation(lambda a, b: a - b, R, R), 
			R, 0
		)
		assert add(12, 13) == 25
		assert add(3, 5) == 8

	def test_not_invertible(self):
		add = GroupOperation(
			lambda a, b: a + b, 
			BinaryOperation(lambda a, b: a - b, R, R), 
			R, 0
		)
		with raises(InvertibilityError):
			assert add(12, 13) == 25
			assert add(3, 5) == 8

	def test_has_identity(self):
		add = GroupOperation(
			lambda a, b: a + b, 
			BinaryOperation(lambda a, b: a - b, R, R), 
			R, 0
		)
		assert add(12, 13) == 25
		assert add(221, 2) == 223

	def test_lacks_identity(self):
		bad_add = GroupOperation(
			lambda a, b: a + b, 
			BinaryOperation(lambda a, b: a - b, R, R), 
			R, 1
		)
		with raises(IdentityError):
			assert bad_add(2, 3) == 5

	def test_is_associative(self):
		add = GroupOperation(
			lambda a, b: a + b, 
			BinaryOperation(lambda a, b: a - b, R, R), 
			R, 0
		)
		assert add(1, 2) == 3
		assert add(4, 5) == 9

	def test_not_associative(self):
		sub = GroupOperation(
			lambda a, b: a - b, 
			BinaryOperation(lambda a, b: a + b, R, R), 
			R, 0
		)
		with raises(AssociativityError):
			assert sub(1, 2) == -1
			assert sub(12, 3) == 9
