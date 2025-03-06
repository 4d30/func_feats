#!/bin/env python

import itertools as its
import functools as fts
import operator as op
import statistics as sts
from array import array
import math

from scipy import stats

import func_feats.compose as compose

from func_feats.sampen import sampen  as __sampen


def __helper(function, signal):
    if hasattr(signal, '__len__'):
        if isinstance(signal[0], float):
            return function(signal)
        else:
            value = map(function, signal)
            value = array('d', value)
            return value
    elif isinstance(signal, float):
        return signal
    else:
        breakpoint()


#def sampen(signal: array) -> float:
#    def _sampen(signal):
#        return __sampen(signal)
#    sampen = __helper(_sampen, signal)
#    return sampen


def take(signal):
    if isinstance(signal, float):
        take_one_ = signal
        return take_one_
    else:
        take_one_ = iter(signal)
        take_one_ = next(take_one_, float('nan'))
        return take_one_

        


def lag(signal):
    def _lag(signal):
        if not signal:
            return float('nan')
        maxvalue = max(signal)
        if maxvalue not in signal:
            return float('nan')
        middle = len(signal)//2
        maxindex = signal.index(maxvalue)
        lg = maxindex - middle
        lg = float(lg)
        return lg
    lg = __helper(_lag, signal)
    return lg


def mav(signal):
    """ Calculates the mean absolute value

    Used to be the AOM, but when we divide by time
    it becomes the MAV

    Keyword arguments:
    signal -- a timeseries signal
    """
    def _mav(signal):
        if len(signal) == 0:
            return float('nan')
        val = map(math.fabs, signal)
        dt = 1/100
        val = map(op.mul, val, its.repeat(dt))
        val = sum(val)/(len(signal)*dt)
        val = float(val)
        val = val/len(signal)
        return val
    val = __helper(_mav, signal)
    return val


def mad(signal: array) -> float:
    def _mad(signal):
        "median absolute deviation"
        signal_median = median(signal)
        if signal_median != signal_median:
            return float('nan')
        deviation_from_median  = map(op.sub, signal, its.repeat(signal_median))
        deviation_from_median = tuple(deviation_from_median)
        abs_dev_from_med  = map(abs, deviation_from_median)
        abs_dev_from_med = tuple(abs_dev_from_med)
        mad = sts.median(abs_dev_from_med)
        return mad
    mad = __helper(_mad, signal)
    return mad

# Smith's motion complexity


def maxvalue(signal: array) -> float:
    def _max(signal):
        if not signal:
            return float('nan')
        return max(signal)
    max_ = __helper(_max, signal)
    return max_


def minvalue(signal: array) -> float:
    def _min(signal):
        if not signal:
            return float('nan')
        return min(signal)
    min_ = __helper(_min, signal)
    return min_


#def length(signal: array) -> float:
#    def _length(signal):
#        return len(signal)
#    len_ = __helper(_length, signal)
#    return len_


def mean(signal: array) -> float:
    def _mean(signal):
        if len(signal) < 2:
            return float('nan')
        return sts.mean(signal)
    mean_val = __helper(_mean, signal)
    return mean_val


def median(signal: array) -> float:

    def _median(signal):
        if not signal:
            return float('nan')
        if not hasattr(signal, '__iter__'):
            return float('nan')
        return sts.median(signal)
    median = __helper(_median, signal)
    return median


def mode(signal: array) -> float:
    def _mode(signal):
        if not signal:
            return float('nan')
        return sts.mode(signal)
    mode = __helper(_mode, signal)
    return mode


def stdev(signal: array) -> float:
    def _stdev(signal):
        if len(signal) < 2:
            return float('nan')
        is_nan = map(op.ne, signal, signal)
        if any(is_nan):
            return float('nan')
        return sts.stdev(signal)
    stdev = __helper(_stdev, signal)
    return stdev


def variance(signal: array) -> float:
    def _variance(signal):
        if len(signal) < 2:
            return float('nan')
        is_nan = map(op.ne, signal, signal)
        if any(is_nan):
            return float('nan')
        return sts.variance(signal)
    var = __helper(_variance, signal)
    return var


def skew(signal: array) -> float:
    def _skew(signal):
        any_nan = map(op.ne, signal, signal)
        if any(any_nan):
            return float('nan')
        stddev = stdev(signal)
        mean_val = mean(signal)
        if not all(map(math.isfinite, (stddev, mean_val,))):
            return float('nan')
        mean_abs = max(1, abs(mean_val))
        sigma = 1e-10
        if stddev < sigma*mean_abs:
            return float('nan')
        return stats.skew(signal)
    skew = __helper(_skew, signal)
    return skew


def kurtosis(signal: array) -> float:
    def _kurtosis(signal):
        stddev = stdev(signal)
        mean_val = mean(signal)
        mean_abs = max(1, abs(mean_val))
        if not all(map(math.isfinite, (stddev, mean_val,))):
            return float('nan')
        sigma = 1e-10
        if stddev < sigma*mean_abs:
            return float('nan')
        return float(stats.kurtosis(signal))
    kurt = __helper(_kurtosis, signal)
    return kurt
