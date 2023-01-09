
import inspect
from collections.abc import Iterable


def typename(_obj):
	return _obj.__class__.__name__

def chain(*iterators):
	if not all(isinstance(i, Iterable) for i in iterators):
		raise TypeError(f'Expected iterable, not {typename(i)}')
	for i in iterators:
		yield from i

def num_kwargs(_func):
	if not callable(_func):
		raise TypeError(f'Expected callable, not {typename(_func)}')
	return str(inspect.signature(_func)).count('=')

def num_args(_func):
	if not callable(_func):
		raise TypeError(f'Expected callable, not {typename(_func)}')
	return len(inspect.signature(_func).parameters) - num_kwargs(_func)

def is_predicate(candidate):
	if not callable(candidate):
		return False
	return len(inspect.signature(candidate).parameters)


