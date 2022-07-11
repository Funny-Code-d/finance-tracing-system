# import pytest


class Calculator:
  #empty constructor
  def __init__(self):
    pass
  #add method - given two numbers, return the addition
  def add(self, x1, x2):
    return x1 + x2
  #multiply method - given two numbers, return the 
  #multiplication of the two
  def multiply(self, x1, x2):
    return x1 * x2
  #subtract method - given two numbers, return the value
  #of first value minus the second
  def subtract(self, x1, x2):
    return x1 - x2
  #divide method - given two numbers, return the value
  #of first value divided by the second
  def divide(self, x1, x2):
    if x2 != 0:
      return x1/x2





# @pytest.mark.dependency(depends=["test_subtract"])
# def test_add():
#     calculator = Calculator()
#     assert calculator.add(4,7) == 11
# @pytest.mark.dependency(depends=["test_multiply"])
# def test_subtract():
#     calculator = Calculator()
#     assert calculator.subtract(10,5) == 5
# @pytest.mark.dependency(depends=["test_divide"])
# def test_multiply():
#     calculator = Calculator()
#     assert calculator.multiply(3,7) == 21
# @pytest.mark.dependency()
# def test_divide():
#     calculator = Calculator()
#     assert calculator.divide(10,2) == 5

import pytest

@pytest.mark.order2
def test_foo():
    assert True

@pytest.mark.order1
def test_bar():
    assert True