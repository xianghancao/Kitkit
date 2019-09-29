# coding=utf-8
import numpy as np
from .function_wrapper import *
from .decorator import *

@decorator
def add(x, y):
	# (x + y)
	return x + y


@decorator
def sub(x, y):
	# (x - y)
	return x - y


@decorator
def mul(x, y):
	# (x * y)
	return x * y


@decorator
def div(x, y):
	# (x/y)
	return x/y


@decorator
def abve(x, y):
	# (x/y)
	return x > y


@decorator
def below(x, y):
	# (x/y)
	return x < y


@decorator
def equal(x, y):
	# (x/y)
	return x == y

