#!/usr/bin/env python2
'''
    Passphrase generator.

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

    Uses Python 2 for compatibility with the Pattern module.
    Requires the following packages:
     * pattern
     * nltk
    Both packages are available via pip.
'''
from __future__ import division, with_statement, print_function, generators

import sys
import entropy.random as random
import generators.wordnet

if __name__ == '__main__':
    if len(sys.argv) == 2:
        print("Using stdin as source of space-delimited random values in the "
              "range 0-%i in base ten." % int(sys.argv[1]))
        random.urandom = random.argv_random(int(sys.argv[1]))

    phrase, entropy = generators.wordnet.generate_phrase_2()
    print('%0.2f bits of entropy' % entropy)
    print(phrase)