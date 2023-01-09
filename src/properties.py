
import functools
import itertools

from utils import typename, num_args


class DomainError(ValueError):
	...


class PropertyError(TypeError):
	...


class ClosureError(PropertyError):
	...


class AssociativityError(PropertyError):
	...


class CommutativityError(PropertyError):
	...


class IndempotencyError(PropertyError):
	...


class InvertibilityError(PropertyError):
	...


class IdentityError(PropertyError):
	...

def associative(_op):
	# TODO: ensure that _op must be a bound method
	if num_args(_op) < 3:
		raise ValueError(f'Expected bound method to take at least two arguments')
	input_cache = []
	@functools.wraps(_op)
	def operation(_obj, left, right):
		input_cache.append(left)
		input_cache.append(right)
		if len(input_cache) >= 3:
			for a, b, c in itertools.permutations(input_cache, 3):
				if not _op(_obj, _op(_obj, a, b), c) == _op(_obj, a, _op(_obj, b, c)):
					raise AssociativityError(f'Operation {_op} is not associative')
		return _op(_obj, left, right)
	return operation

def commutative(_op):
	# TODO: ensure that _op must be a bound method
	if num_args(_op) < 3:
		raise ValueError(f'Expected bound method to take at least two arguments')
	input_cache = []
	@functools.wraps(_op)
	def operation(_obj, left, right):
		input_cache.append(left)
		input_cache.append(right)
		for a, b in itertools.permutations(input_cache, 2):
			if not _op(_obj, a, b) == _op(_obj, b, a):
				raise CommutativityError(f'Operation {_op} is not commutative')
		return _op(_obj, left, right)
	return operation

def indempotent(_op):
	# TODO: ensure that _op must be a bound method
	if num_args(_op) < 3:
		raise ValueError(f'Expected bound method to take at least two arguments')
	input_cache = []
	@functools.wraps(_op)
	def operation(_obj, left, right):
		input_cache.append(left)
		input_cache.append(right)
		for e in input_cache:
			if not _op(_obj, e, e) == e:
				raise IndempotencyError(f'Operation {_op} is not indempotent')
		return _op(_obj, left, right)
	return operation

def identity(candidate):
	def decorator(_op):
		if num_args(_op) != 2:
			raise ValueError(f'Expected bound method to take at least two arguments')
		input_cache = []
		@functools.wraps(_op)
		def operation(self, other):
			input_cache.append(self)
			input_cache.append(other)
			for e in input_cache:
				if _op(candidate, e) != e:
					raise IdentityError(f'Operation {_op} does not have right identity {candidate}')
				if _op(e, candidate) != e:
					raise IdentityError(f'Operation {_op} does not have left identity {candidate}')
			return _op(self, other)
		return operation
	return decorator

def invertible(identity, _inv_op):
	if num_args(_inv_op) != 2:
		raise ValueError(f'Expected invertible operation to have at least two arguments')
	@functools.wraps(_inv_op)
	def decorator(_op):
		if num_args(_op) != 2:
			raise ValueError(f'Expected invertible operation to have at least two arguments')
		input_cache = []
		@functools.wraps(_op)
		def operation(self, other):
			input_cache.append(self)
			input_cache.append(other)
			if len(input_cache) >= 3:
				for a, b, c in itertools.permutations(input_cache, 3):
					if a != _inv_op(c, b):
						raise InvertiblityError(f'Operation {_op} is not right invertible via {_inv_op}')
					if b != _inv_op(c, a):
						raise InvertibilityError(f'Operation {_op} is not left invertible via {_inv_op}')
			for e in input_cache:
				if identity != _inv_op(e, e):
					raise IdentityError(f'Operation {_op} with inverse operation {_inv_op} does not have identity {identity}')
			return _op(self, other)
		return operation
	return decorator

def right_ideal_closure(ring_aset, ideal_aset):
	def decorator(_ring_op):
		if num_args(_op) < 3:
			raise ValueError(f'Expected bound method to take at least two arguments')
		input_cache = []
		@functools.wraps(_ring_op)
		def operation(self, other):
			input_cache.append(self)
			input_cache.append(other)
			for a, b in itertools.permutations(input_cache, 2):
				if not (a in ideal_aset or b in ideal_aset):
					continue
				if a in ideal_aset and b not in ideal_aset:
					if not _ring_op(a, b):
						raise ClosureError(f'Right ideal defined over {ideal_aset} does not satisfy the closure axiom')
				if b in ideal_aset and a not in ideal_aset:
					if not _ring_op(b, a):
						raise ClosureError(f'Right ideal defined over {ideal_aset} does not satisfy the closure axiom')
			return _ring_op(self, other)
		return operation
	return decorator

def left_ideal_closure(ring_aset, ideal_aset):
	def decorator(_ring_op):
		if num_args(_op) < 3:
			raise ValueError(f'Expected bound method to take at least two arguments')
		input_cache = []
		@functools.wraps(_ring_op)
		def operation(self, other):
			input_cache.append(self)
			input_cache.append(other)
			for a, b in itertools.permutations(input_cache, 2):
				if not (a in ideal_aset or b in ideal_aset):
					continue
				if a in ideal_aset and b not in ideal_aset:
					if not _ring_op(b, a):
						raise ClosureError(f'Left ideal defined over {ideal_aset} does not satisfy the closure axiom')
				if b in ideal_aset and a not in ideal_aset:
					if not _ring_op(a, b):
						raise ClosureError(f'Left ideal defined over {ideal_aset} does not satisfy the closure axiom')
			return _ring_op(self, other)
		return operation
	return decorator

def ideal_closure(ring_aset, ideal_aset):
	def decorator(_ring_op):
		if num_args(_op) < 3:
			raise ValueError(f'Expected bound method to take at least two arguments')
		input_cache = []
		@functools.wraps(_ring_op)
		def operation(self, other):
			input_cache.append(self)
			input_cache.append(other)
			for a, b in itertools.permutations(input_cache, 2):
				if not (a in ideal_aset or b in ideal_aset):
					continue
				if a in ideal_aset and b not in ideal_aset:
					if not _ring_op(b, a):
						raise ClosureError(f'Ideal defined over {ideal_aset} does not satisfy the closure axiom')
					if not _ring_op(a, b):
						raise ClosureError(f'Right ideal defined over {ideal_aset} does not satisfy the closure axiom')
				if b in ideal_aset and a not in ideal_aset:
					if not _ring_op(a, b):
						raise ClosureError(f'Ideal defined over {ideal_aset} does not satisfy the closure axiom')
					if not _ring_op(b, a):
						raise ClosureError(f'Right ideal defined over {ideal_aset} does not satisfy the closure axiom')
			return _ring_op(self, other)
		return operation
	return decorator




