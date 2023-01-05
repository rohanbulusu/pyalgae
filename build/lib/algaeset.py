
from collections.abc import Sequence

from utils import typename, num_args


class AlgaeSet:

	def __init__(self, predicate):
		if not callable(predicate):
			raise TypeError(f'Expected Callable, not {typename(predicate)}')
		if num_args(predicate) != 1:
			raise ValueError(f'Predicate must be a single-argument function')
		self.predicate = predicate
		self.added_elemnts = []
		self.removed_elements = []

	@classmethod
	def from_sequence(sequence):
		if not isinstance(sequence, Sequence):
			raise TypeError(f'Expected Sequence, not {typename(sequence)}')
		return self.__class__(
			lambda e: e in sequence
		)

	def has(self, element):
		passes_predicate = self.predicate(element)
		was_added = element in self.added_elements
		was_removed = element in self.removed_elements
		return (passes_predicate or was_added) and not was_removed

	def add(self, element):
		self.added_elements.append(element)

	def remove(self, element):
		self.removed_elements.append(element)

	def __and__(self, other):
		if not isinstance(other, self.__class__):
			raise TypeError(f'Expected {typename(self)}, not {typename(other)}')
		return self.__class__(
			lambda e: self.has(e) and other.has(e)
		)

	def __or__(self, other):
		if not isinstance(other, self.__class__):
			raise TypeError(f'Expected {typename(self)}, not {typename(other)}')
		return self.__class__(
			lambda e: self.has(e) or other.has(e)
		)


