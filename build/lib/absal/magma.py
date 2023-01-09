
from algae.utils import typename
from algae.algaeset import AlgaeSet
import algae.maps as maps


class Magma:

	def __init__(self, aset, binop):
		if not isinstance(aset, AlgaeSet):
			raise TypeError(f'Expected an AlgaeSet, not {typename(aset)}')
		if binop.domain != binop.range:
			raise TypeError(f'Expected a closed operation, not {typename(binop)}')
		if binop.domain != aset:
			raise ValueError(f'Expected binary operation to be closed over {aset}, not {binop.domain}')
		self.aset = aset
		self.binop = binop

	def __contains__(self, candidate):
		return candidate in self.aset

	def __call__(self, a, b):
		return self.binop(a, b)


class Semigroup(Magma):

	def __init__(self, aset, binop):
		if not isinstance(binop, maps.ClosedAssociativeOperation):
			raise TypeError(f'Expected a ClosedAssociativeOperation, not {typename(binop)}')
		super().__init__(aset, binop)


class UnitalMagma(Magma):

	def __init__(self, aset, binop):
		if not isinstance(binop, maps.ClosedIdentityOperation):
			raise TypeError(f'Expected a ClosedIdentityOperation, not {typename(binop)}')
		super().__init__(aset, binop)


class Monoid(UnitalMagma):

	def __init__(self, aset, binop):
		if not isinstance(binop, maps.ClosedAssociativeIdentityOperation):
			raise TypeError(f'Expected a ClosedAssociativeIdentityOperation, not {typename(binop)}')
		super().__init__(aset, binop)
