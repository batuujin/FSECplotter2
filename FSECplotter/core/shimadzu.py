#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
FSECplotter2 - The interactive plotting application for FSEC.

Copyright 2015-2017, TaizoAyase, tikuta, biochem-fan

This file is part of FSECplotter2.

FSECplotter2 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re
import os
import codecs

import numpy as np

from FSECplotter.core import Logfile, LogfileError


class ShimadzuLogFile(Logfile):

    def __init__(self, filename):
        self.sections = []
        super().__init__(filename)

    def data(self, **kwargs):
        detector = kwargs['detector']
        channel  = kwargs['channel']
        sec_name = "LC Chromatogram(Detector %s-Ch%d)" % (detector, channel)
        sec = self.__find_section(sec_name)
        return sec.data()

    def _parse(self, filename):
        header_pattern = re.compile(r"\[.+\]")
        header_flag = False
        f = codecs.open(filename, "r", "shift_jis")
        for line in f:
            # search the header line
            if re.match(header_pattern, line):
                sec = Section(line)
                header_flag = True

            # search the end of the section
            if re.match(r"^\s+$", line):
                if header_flag:
                    header_flag = False
                    self.__append_section(sec)
                    del sec

            sec.append_data(line) if 'sec' in locals() else None

        f.close()

        self.__set_num_detectors()
        self.__set_num_channels()
        self.__set_flowrate()

    # private methods

    def __append_section(self, section):
        section.convert_to_npary()
        self.sections.append(section)
        return self.sections

    # get flow rate from the file name of method file
    # if cannot, raise Error

    def __set_flowrate(self):
        try:
            methodfiles_ary = self.__get_params_ary(
                "Original Files", "Method File")
        except NoSectionError as e:
            raise e

        # search float in file name
        pat = re.compile(r"\d\.\d+")
        matched_str = pat.findall(methodfiles_ary[0])
        if matched_str:
            self.flowrate = float(matched_str[0])
        else:
            self.flowrate = None

    # detector/channel num. is written in Configuration section
    def __set_num_detectors(self):
        num_detectors_ary = self.__get_params_ary(
            "Configuration", "# of Detectors")
        self.num_detectors = int(num_detectors_ary[0])
        return self.num_detectors

    def __set_num_channels(self):
        num_channels_ary = self.__get_params_ary(
            "Configuration", "# of Channels")
        self.num_channels = int(num_channels_ary[-1])
        return self.num_channels

    # return section that match the RE of section_name
    def __find_section(self, section_name):
        # first, replace "()" to "\(\)"
        secname = self.__sub_parenthesis(section_name)
        pat = re.compile(secname)
        name_ary = [x.name() for x in self.sections]
        index = [i for i, name in enumerate(name_ary) if pat.search(name)]
        if not index:
            raise NoSectionError
        return self.sections[index[0]]

    def __sub_parenthesis(self, section_name):
        tmp = re.sub(r"\(", "\(", section_name)
        return re.sub(r"\)", "\)", tmp)

    def __get_params_ary(self, section_name, param_name):
        params_ary = self.__find_section(section_name).params()
        for par in params_ary:
            if param_name in par:
                tmp_name_ary = par.copy()  # deep copy of list
                tmp_name_ary.pop(0)  # remove param name
                return tmp_name_ary


class Section:
    # initialized with section header name

    def __init__(self, header_str):
        self.__section_name = header_str.strip("\r\n")
        self.__parameters = []
        self.__data_table = []
        self.__np_data_table = None

    # add row to the datatable
    # list should be a array of float
    def append_data(self, line):
        ary = line.strip("\r\n").split("\t")

        # try to convert the first col to float
        try:
            float(ary[0])
        # if cannot, this is the paramter part
        except ValueError:
            self.__parameters.append(ary)
            return self

        # if can, this is the time table part
        ary_f = [float(ary[0]), float(ary[1])]
        self.__data_table.append([ary_f[0], ary_f[1]])
        return self

    def convert_to_npary(self):
        self.__np_data_table = np.array(self.__data_table)

    # getters
    def name(self):
        return self.__section_name

    def data(self):
        if self.__np_data_table is None:
            return None

        if self.__np_data_table.any():
            return self.__np_data_table
        return self.__data_table

    def params(self):
        return self.__parameters


# exceptions
class NoMatchedFlowRateError(LogfileError):
    pass


class NoSectionError(LogfileError):
    pass
