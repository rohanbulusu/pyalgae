
from utils import chain, typename, is_predicate


def get_restricted_type(_type, restriction):
	if not isinstance(_type, type):
		raise TypeError(f'Expected a class identifier, not an object')

	class RestrictedTypeMeta(type):
		def __instancecheck__(cls, instance):
			return isinstance(instance, _type) and restriction(instance)
		def __repr__(cls):
			return f'RestrictedType({_type.__name__} restricted by {restriction})'
		def __eq__(cls, other):
			return _type == other or super().__eq__(other)
		def __hash__(cls):
			return hash(repr(cls))

	class RestrictedType(metaclass=RestrictedTypeMeta):
		...

	return RestrictedType


class AlgaeSet:

	def __init__(self, *elements):
		if any(isinstance(e, type) for e in elements):
			raise TypeError(f'Expected objects, not types')
		self.types = []
		self.elements = list(set(elements))
		self.exclusions = []

	@classmethod
	def from_type(cls, _type):
		if not isinstance(_type, type):
			raise TypeError(f'Expected a class identifier, not an object')
		_obj = cls()
		_obj.types.append(_type)
		return _obj

	@property
	def is_infinite(self):
		return bool(self.types)

	@property
	def is_finite(self):
		return not self.is_infinite

	def __repr__(self):
		return f'AlgaeSet{tuple(chain(self.types, self.elements))}'

	def __eq__(self, other):
		if not isinstance(other, self.__class__):
			return False
		equal_types = set(self.types) == set(other.types)
		equal_elements = set(self.elements) == set(other.elements)
		equal_exclusions = set(self.exclusions) == set(other.exclusions)
		return equal_types and equal_elements and equal_exclusions

	def __contains__(self, candidate):
		captured_by_type = any(isinstance(candidate, t) for t in self.types)
		in_elements = candidate in self.elements
		in_exclusions = candidate in self.exclusions
		return (captured_by_type or in_elements) and not in_exclusions

	def add(self, element):
		if any(isinstance(element, t) for t in self.types):
			return
		if element in self.exclusions:
			self.exclusions.remove(element)
			return
		self.elements.append(element)

	def add_type(self, _type):
		if not isinstance(_type, type):
			raise TypeError(f'Expected a class identifier, not an object')
		self.types.append(_type)

	def remove(self, element):
		if element not in self:
			raise ValueError(f'{element} not in {self}')
		if element in self.exclusions:
			return
		if element in self.elements:
			self.elements.remove(element)
		self.exclusions.append(element)

	def remove_type(self, _type):
		if not isinstance(_type, type):
			raise TypeError(f'Expected a class identifier, not an object')
		self.types.remove(_type)

	def __or__(self, other):
		if not isinstance(other, AlgaeSet):
			raise TypeError(f'Expected AlgaeSet, not {typename(other)}')
		if self.is_infinite and other.is_finite:
			if all(any(isinstance(e, t) for t in self.types) for e in other.elements):
				return self
			union = self.__class__(*other.elements)
			union.types = self.types
			return union
		if other.is_infinite and self.is_finite:
			if all(any(isinstance(e, t) for t in other.types) for e in self.elements):
				return other
			union = self.__class__(*self.elements)
			union.types = other.types
			return union
		union = self.__class__(*list(chain(self.elements, other.elements)))
		union.types = list(chain(self.types, other.types))
		union.exclusions = list(chain(self.exclusions, other.exclusions))
		return union

	def __and__(self, other):
		if not isinstance(other, AlgaeSet):
			raise TypeError(f'Expected AlgaeSet, not {typename(other)}')
		intersection = self.__class__(*[
			e for e in self.elements if e in other.elements
		])
		intersection.types = [
			t for t in self.types if t in other.types
		]
		intersection.exclusions = [
			t for t in self.exclusions if t in other.exclusions
		]
		return intersection

	def such_that(self, restriction):
		if not is_predicate(restriction):
			raise TypeError(f'Expected restriction to be a valid predicate')
		restricted_elements = [e for e in self.elements if restriction(e)]
		_obj = self.__class__(*restricted_elements)
		_obj.types = [get_restricted_type(t, restriction) for t in self.types]
		return _obj

	def has_subset(self, other):
		if not isinstance(other, AlgaeSet):
			raise TypeError(f'Expected AlgaeSet, not {typename(other)}')
		if self == other:
			return True
		if self.is_finite and other.is_finite:
			elements_are_contained = all(
				o in self for o in other.elements
			) 
			exclusions_are_respected = all(
				s in other for s in self.exclusions
			)
			return elements_are_contained and exclusions_are_respected
		if self.is_infinite and other.is_finite:
			elements_are_contained = all(
				any(isinstance(o, t) for t in self.types) for o in other.elements
			)
			exclusions_are_respected = not any(
				o in self.exclusions for o in other.elements
			)
			return elements_are_contained and exclusions_are_respected
		if self.is_infinite and other.is_infinite:
			types_are_contained = all(
				t in self.types for t in other.types
			)
			elements_are_contained = all(
				(o in self.elements or any(isinstance(o, t) for t in self.types)) 
				for o in other.elements
			)
			exclusions_are_respected = not any(
				o in self.exclusions for o in other.elements
			)
			return types_are_contained and elements_are_contained and exclusions_are_respected
		return False

	def is_subset(self, other):
		return other.has_subset(self)

	def has_proper_subset(self, other):
		if not isinstance(other, AlgaeSet):
			raise TypeError(f'Expected AlgaeSet, not {typename(other)}')
		if self == other:
			return False
		return self.has_subset(other)

	def is_proper_subset(self, other):
		if not isinstance(other, AlgaeSet):
			raise TypeError(f'Expected AlgaeSet, not {typename(other)}')
		if self == other:
			return False
		return self.is_subset(other)


C = AlgaeSet.from_type(int) | AlgaeSet.from_type(float) | AlgaeSet.from_type(complex)
R = C.such_that(lambda e: e.imag == 0 if isinstance(e, complex) else True)
Z = R.such_that(lambda e: e % 1 == 0)
N = Z.such_that(lambda e: e >= 0)

