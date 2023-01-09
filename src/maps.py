
from collections.abc import Sequence

from utils import typename, num_kwargs, num_args
from algaeset import AlgaeSet
from properties import DomainError, commutative, associative, indempotent, identity, invertible


class Mapping:

	def __init__(self, mapping, domains, codomains):
		if not callable(mapping):
			raise TypeError(f'Expected callable, not {typename(mapping)}')
		if num_kwargs(mapping):
			raise ValueError(f'Did not expect mapping to have kwarg parameters')
		if not isinstance(domains, Sequence):
			raise TypeError(f'Expected sequence, not {typename(domains)}')
		if not all(isinstance(d, AlgaeSet) for d in domains):
			raise TypeError(f'Expected all domains to be AlgaeSets')
		if not isinstance(codomains, Sequence):
			raise TypeError(f'Expected sequence, not {typename(domains)}')
		if not all(isinstance(c, AlgaeSet) for c in codomains):
			raise TypeError(f'Expected all codomains to be AlgaeSets')
		if num_args(mapping) > len(domains):
			raise ValueError(f'Must specify input domain for every mapping input')
		if num_args(mapping) < len(domains):
			raise ValueError(f'Cannot specify more input domains than there are mapping inputs')
		
		self.mapping = mapping
		self.domains = domains
		self.codomains = codomains
		self.input_dim = len(self.domains)
		self.output_dim = len(self.codomains)

	def __call__(self, *args):
		if len(args) != self.input_dim:
			raise ValueError(f'Expected {self.input_dim} arguments, got {len(args)} arguments')
		
		# check input types
		for arg, domain in zip(args, self.domains):
			if arg not in domain:
				raise DomainError(f'Expected argument {arg} to be in {domain}')
		
		# check output types
		output = self.mapping(*args)
		if self.output_dim == 1:
			if isinstance(output, Sequence) and len(output) != 1:
				raise DomainError(f'Expected output to be strictly one-dimensional')
			if output not in self.domains[0]:
				raise DomainError(f'Expected output {output} to be in {self.domains[0]}')
			return output
		if len(output) != self.output_dim:
			raise DomainError(f'Expected output to be strictly {self.output_dim}-dimensional')
		for result, codomain in zip(output, self.codomains):
			if result not in codomain:
				raise DomainError(f'Expected output {result} to be in {codomain}')
		return output


class Endomorphism(Mapping):

	def __init__(self, mapping, domain):
		super().__init__(mapping, [domain], [domain])
		self.domain = domain
		self.range = domain

	def __call__(self, a):
		return super().__call__(a)


class BinaryOperation(Mapping):

	def __init__(self, mapping, domain, codomain):
		super().__init__(mapping, [domain, domain], [codomain])
		self.domain = domain
		self.range = codomain

	def __call__(self, a, b):
		return super().__call__(a, b)


class ClosedOperation(BinaryOperation):

	def __init__(self, mapping, domain):
		super().__init__(mapping, domain, domain)


class CommutativeOperation(BinaryOperation):

	@commutative
	def __call__(self, a, b):
		return super().__call__(a, b)


class ClosedCommutativeOperation(CommutativeOperation):

	def __init__(self, mapping, domain):
		super().__init__(mapping, domain, domain)


class AbelianOperation(CommutativeOperation):
	...


class ClosedAbelianOperation(ClosedCommutativeOperation):
	...


class AssociativeOperation(BinaryOperation):

	@associative
	def __call__(self, a, b):
		return super().__call__(a, b)


class ClosedAssociativeOperation(AssociativeOperation):

	def __init__(self, mapping, domain):
		super().__init__(mapping, domain, domain)


class IndempotentOperation(BinaryOperation):

	@indempotent
	def __call__(self, a, b):
		return super().__call__(a, b)


class ClosedIndempotentOperation(IndempotentOperation):

	def __init__(self, mapping, domain):
		super().__init__(mapping, domain, domain)


class IdentityOperation(BinaryOperation):

	def __init__(self, mapping, domain, codomain, identity):
		super().__init__(mapping, domain, codomain)
		if identity not in domain:
			raise ValueError(f'Expected identity {identity} to be in domain {domain}')
		if identity not in codomain:
			raise ValueError(f'Expected identity {identity} to be in codomain {codomain}')
		self.identity = identity
		self.__call__ = lambda self, a, b: identity(self.identity)(super().__call__)(a, b)


class ClosedIdentityOperation(IdentityOperation):

	def __init__(self, mapping, domain, identity):
		super().__init__(mapping, domain, domain, identity)


class AssociativeIdentityOperation(IdentityOperation, AssociativeOperation):

	def __init__(self, mapping, domain, codomain, identity):
		super().__init__(mapping, domain, codomain, identity)


class ClosedAssociativeIdentityOperation(AssociativeIdentityOperation):

	def __init__(self, mapping, domain, identity):
		super().__init__(mapping, domain, domain, identity)


class InvertibleOperation(IdentityOperation):

	def __init__(self, mapping, inverse_mapping, domain, codomain, identity):
		super().__init__(mapping, domain, codomain, identity)
		if not isinstance(inverse_mapping, BinaryOperation):
			raise TypeError(f'Expected BinaryOperation, not {typename(inverse_mapping)}')
		if inverse_mapping.domain != codomain:
			raise ValueError(f'Expected domain of {inverse_mapping} to be the codomain of {mapping}')
		if inverse_mapping.range != domain:
			raise ValueError(f'Expected domain of {inverse_mapping} to be the domain of {mapping}')
		self.inverse_mapping = inverse_mapping
		self.__call__ = lambda self, a, b: invertible(self.identity, self.inverse_mapping)(super().__call__)(a, b)


class ClosedInvertibleOperation(InvertibleOperation):

	def __init__(self, mapping, inverse_mapping, domain, identity):
		super().__init__(mapping, inverse_mapping, domain, domain, identity)


class GroupOperation(ClosedInvertibleOperation):

	@associative
	def __call__(self, a, b):
		return super().__call__(a, b)

class AbelianGroupOperation(GroupOperation, ClosedAbelianOperation):

	@commutative
	def __call__(self, a, b):
		return super().__call__(a, b)
