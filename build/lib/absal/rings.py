
from algae.utils import AlgaeSet
from algae.properties import left_ideal_closure, right_ideal_closure, ideal_closure
import algae.maps as maps

from magma import Semigroup, Monoid
from groups import Group


class Ring:

	def __init__(self, aset, addition, multiplication):
		if not isinstance(aset, AlgaeSet):
			raise TypeError(f'Expected AlgaeSet, not {aset}')
		if not isinstance(addition, maps.GroupOperation):
			raise TypeError(f'Expected GroupOperation, not {typename(addition)}')
		if not isinstance(multiplication, maps.ClosedAssociativeOperation):
			raise TypeError(f'Expected ClosedAssociativeOperation, not {typename(multiplication)}')
		if addition.domain != aset:
			raise ValueError(f'Expected addition\'s domain to be {aset}')
		if multiplication.domain != aset:
			raise ValueError(f'Expected multiplication\'s domain to be {aset}')
		self.aset = aset
		self.addition = addition
		self.additive_group = Group(aset, addition)
		self.multiplication = multiplication
		self.multiplicative_semigroup = Semigroup(aset, multiplication)
		self.is_infinite = aset.is_infinite
		self.is_finite = aset.is_finite

	@classmethod
	def from_group(cls, addition_group, multiplication):
		if not isinstance(multiplication, maps.ClosedAssociativeOperation):
			raise TypeError(f'Expected ClosedAssociativeOperation, not {typename(multiplication)}')
		return cls(
			addition_group.aset,
			addition_group.binop,
			multiplication
		)

	def add(self, a, b):
		return self.addition(a, b)

	def mul(self, a, b):
		return self.multiplication(a, b)


class UnitalRing(Ring):

	def __init__(self, aset, addition, multiplication):
		if not isinstance(multiplication, maps.ClosedAssociativeIdentityOperation):
			raise TypeError(f'Expected ClosedAssociativeIdentityOperation, not {typename(multiplication)}')
		self.multiplicative_monoid = Monoid(aset, multiplication)
		super().__init__(aset, addition, multiplication)


class DivisionRing(UnitalRing):

	def __init__(self, aset, addition, multiplication):
		if not isinstance(multiplication, maps.GroupOperation):
			raise TypeError(f'Expected GroupOperation, not {typename(multiplication)}')
		super().__init__(aset, addition, multiplication)


class Field(DivisionRing):

	def __init__(self, aset, addition, multiplication):
		if not isinstance(multiplication, maps.AbelianGroupOperation):
			raise TypeError(f'Expected AbelianGroupOperation, not {typename(multiplication)}')
		super().__init__(aset, addition, subtraction)


class RightIdeal:

	def __init__(self, ring, aset):
		if not isinstance(ring, Ring):
			raise TypeError(f'Expected Ring, not {typename(ring)}')
		if not isinstance(aset, AlgaeSet):
			raise TypeError(f'Expected AlgaeSet, not {typename(aset)}')
		if not ring.additive_group.has_subgroup(Group(aset, ring.addition)):
			raise ValueError(f'AlgaeSet {aset} does not satisfy ideal addition axiom')
		ring.multiplication = right_ideal_closure(ring.aset, aset)(ring.multiplication)
		self.ring = ring
		self.aset = aset


class LeftIdeal:

	def __init__(self, ring, aset):
		if not isinstance(ring, Ring):
			raise TypeError(f'Expected Ring, not {typename(ring)}')
		if not isinstance(aset, AlgaeSet):
			raise TypeError(f'Expected AlgaeSet, not {typename(aset)}')
		if not ring.additive_group.has_subgroup(Group(aset, ring.addition)):
			raise ValueError(f'AlgaeSet {aset} does not satisfy ideal addition axiom')
		ring.multiplication = left_ideal_closure(ring.aset, aset)(ring.multiplication)
		self.ring = ring
		self.aset = aset


class Ideal(RightIdeal, LeftIdeal):

	def __init__(self, ring, aset):
		ring.multiplication = left_ideal_closure(ring.aset, aset)(ring.multiplication)
		super().__init__(ring, aset)


