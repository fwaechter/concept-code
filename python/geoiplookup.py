#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#  Author:
#    Flavio Waechter chuehbueb@gmail.com
#
#  Copyright (c) 2012, Flavio Waechter
#
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without modification,
#       are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright notice,
#       this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the distribution.
#     * Neither the name of the [ORGANIZATION] nor the names of its contributors may
#       be used to endorse or promote products derived from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import locale
import argparse

from babel import Locale
from babel.core import UnknownLocaleError

import GeoIP

def resolve_address(ip):
    return GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE).country_code_by_addr(ip)

def set_default_locale(locale_module=locale):
    locale = locale_module
    locale.setlocale(locale.LC_ALL, '')
    language_code, _ = locale.getlocale()
    language, territory = language_code.split('_')
    return (language, territory)

def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', help='IP to resolve')
    parser.add_argument('-l', '--language', help='the language code')
    parser.add_argument('-t', '--territory', help='the territory (country or region) code')
    return parser

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    option_parser = parse_options()
    args = option_parser.parse_args(argv)
    default_language, default_territory = set_default_locale()
    language = default_language if args.language is None else args.language
    territory = default_territory if args.territory is None else args.territory
    try:
        locale = Locale(language, territory)
    except UnknownLocaleError, e:
        option_parser.error(str(e))
    return locale.territories[resolve_address(args.ip)]

if __name__ == '__main__':
    print main()