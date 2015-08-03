'''
    Random integer generator.
    
    Copyright (C) 2015 jonathan lung <lungj+git@heresjono.com>
    
    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''
## TODO: ensure entropy is good!
from __future__ import division, with_statement, print_function, generators

from os import urandom
from math import log, ceil, floor

import sys

def random_item_from_list(l):
    '''
    Return an item from l with uniform probability.
    '''
    return l[randint(len(l))]

def randint(n, bias_limit=0.0001):
    '''
    Return a random number from 0 to n - 1.
    The most likely number is expected to appear no more than bias_limit% more than 1/n.
    '''
    # Number of bits required to express n - 1
    entropy_bits_required = log((n + 1), 2)
    bias = (1 / n) / (1 / (2 ** ceil(entropy_bits_required))) - 1

    # Number of extra bits more than entropy_bits_required required to reduce bias below
    # the bias limit.
    oversample_bits = max(int(ceil(log(bias / (bias_limit / 100), 2))), 0)

    # Total number of bytes of entropy required from the entropy source.
    bytes_required = int(ceil((entropy_bits_required + oversample_bits) / 8))

    # Generate a random number and then map it to the range 0..(n-1)
    random_number = int(urandom(bytes_required).encode('hex'), 16)
    return int(floor((random_number) / (256 ** bytes_required) * n))

def argv_random(var_range):
    '''
    Get entropy from standard input. E.g., take a set of dice rolls.
    No debiasing or tests for randomness are performed.
    '''
    # TODO: Fix rounding errors from this function in amount of available bits.

    def get_byte(state=[0, 0]):
        '''Use a state machine to convert input from stdin into 8-bit chunks.'''
        cur_val, cur_bits = state
        tokens_to_read = log((var_range + 1), 2) / 8 - cur_bits

        token = ''
        while cur_bits < 8:
            token += sys.stdin.read(1)
            if token[-1].isspace():
                cur_val = cur_val * var_range + int(token[:-1])
                cur_bits += log(var_range, 2)
                token = ''

        state[:] = [cur_val // 256, cur_bits - 8]

        return chr(cur_val % 256)

    def urandom(bytes_required):
        '''Return a string of random bytes of length bytes_required.'''
        return ''.join(get_byte() for i in range(bytes_required))

    return urandom
