# coding=utf-8
import expr_generator
prob_engine = expr_generator.ExprGenerator()


def drawdown(y):
    return 'drawdown(%s)' %y


def drawdown_period(y):
    return 'drawdown_period(%s)' %y


def scale_one(x):
    return 'scale_one(%s)' %x


def equal_wgts(x):
    return 'equal_wgts(%s)' %x