
import inspect


def typename(_obj):
	return _obj.__class__.__name__


def num_args(_func):
	if not callable(_func):
		raise TypeError(f'Expected Callable, not {typename(_func)}')
	parameters = inspect.signature(_func).parameters.values()
	return len(parameters)
