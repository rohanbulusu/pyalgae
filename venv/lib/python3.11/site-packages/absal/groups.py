
from algae.utils import typename
from algae.algaeset import AlgaeSet
from algae.maps import GroupOperation


class Group:

	def __init__(self, aset, binop):
		if not isinstance(binop, GroupOperation):
			raise TypeError(f'Expected a GroupOperation, not {typename(binop)}')
		if binop.domain != aset:
			raise ValueError(f'Expected binary operation\'s domain to be {aset}')
		self.aset = aset
		self.binop = binop

	def has_subgroup(self, candidate):
		if not isinstance(candidate, Group):
			raise TypeError(f'Expected Group, not {typename(candidate)}')
		return self.aset.has_proper_subset(candidate.aset)

	def is_subgroup(self, candidate):
		if not isinstance(candidate, Group):
			raise TypeError(f'Expected Group, not {typename(candidate)}')
		return self.aset.is_proper_subset(candidate.aset)

	@classmethod
	def Z_mod(cls, n):
		if not isinstance(n, int):
			raise TypeError(f'Z can only be partitioned by integer modulo')
		if not n > 0:
			raise ValueError(f'Z can only be partitioned by positive modulo')
		aset = AlgaeSet(*range(n))
		return cls(
			aset,
			GroupOperation(
				lambda a, b: (a + b) % n,
				lambda a, b: (a - b) if a >= b else (a - b) + n
				domain=aset,
				identity=0
			)
		)


class LieGroup(Group):

	def __init__(self, aset, binop):
		if not isinstance(aset, AlgaeSet):
			raise TypeError(f'Expected AlgaeSet, not {typename(aset)}')
		if aset.is_finite:
			raise ValueError(f'Expected infinite set, not {aset}')
		super().__init__(aset, binop)
		
