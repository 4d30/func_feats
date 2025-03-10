#!/bin/env python

import itertools as its
import operator as op
import statistics as sts

from scipy import signal
from scipy import fft

from array import array

import func_feats.transform.single as single


def passalong(signal_pair: tuple[array]) -> tuple[array]:
    signal_pair = map(single.passalong, signal_pair)
    signal_pair = tuple(signal_pair)
    return signal_pair


def dft(signal_pair: tuple[array]) -> tuple[array]:
    signal_pair = map(single.dft, signal_pair)
    signal_pair = tuple(signal_pair)
    return signal_pair


def autocorrelate(signal_pair: tuple[array]) -> tuple[array]:
    value = map(single.autocorrelate, signal_pair)
    value = tuple(value)
    return value


def zerosq(signal_pair: tuple[array]) -> tuple[array]:
    signal_pair = map(single.zerosq, signal_pair)
    signal_pair = tuple(signal_pair)
    return signal_pair


def findpeaks(signal_pair: tuple[array]) -> tuple[array]:
    signal_pair = map(single.findpeaks, signal_pair)
    signal_pair = tuple(signal_pair)
    return signal_pair


def cross_correlate(signal_pair: tuple[array]) -> tuple[array]:
    """ Cross-correlates two signals. The function first windows
    the signal, then calculates the cross correlation of each window,
    locates the max cross correlation in each window, and then selects
    the median value of the max cross correlations from the windows.

    Keyword arguments:
        signal_pair -- a tuple of two timeseries signals
    """
    # TODO REVISE TO COVER SHAPE OF SERIES OF WINDOWS AND TWO SETS OF STREAMS
    #  -- COVARIANCE WILL NEED SAME TREATMENT
    sig_a = map(op.itemgetter(0), signal_pair)
    sig_a = tuple(sig_a)
    sig_b = map(op.itemgetter(1), signal_pair)
    sig_b = tuple(sig_b)
    corr = map(signal.correlate, sig_a, sig_b)
    corr = map(array, its.repeat('d'), corr)
    corr = tuple(corr)
    return corr
