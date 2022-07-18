from pathlib import WindowsPath
import os
import re

import numpy as np
import pandas as pd


def file_read_lines(path_name, file_name):
    '''
    Function to return file contents as list of individual lines.

    :param str path_name: Path to file
    :param str file_name: Name of file

    :return: All lines in specified file
    :rtype: list
    '''
    f = open(WindowsPath(f"{path_name}\\{file_name}"), "r")
    lines = f.readlines()
    f.close()

    return lines


def tower_version_info(path_name):
    '''
    Function to return tower version.

    :param str path_name: Path to file

    :return: PLS Tower version
    :rtype: dict
    '''
    f = open(WindowsPath(f"{path_name}\\tower\\uninstall.dat"), "r")
    lines = f.readlines()
    f.close()

    tower_version_string = "SOURCE='Setup Version "
    system_version_string = ".exe"
    unit_string = "UNITS="

    ret_dict = {}

    for line in lines:
        if unit_string in line:
            ret_dict["units"] = line.split(unit_string)[1].split()[0].strip("'")
        if tower_version_string in line:
            ret_dict["version"] = line.split(tower_version_string)[1].split()[0].strip("'")
        if system_version_string in line:
            file_name = re.split(system_version_string, os.path.split(line.strip("'"))[1])[0]
            ret_dict["system"] = re.search("\d+", file_name)[0]

    return ret_dict


class TowerBuilder:
    def __init__(self, path_name):
        '''
        Class to read Excel input sheet and produce tower files based on input.

        :param str path_name: Path to input Excel sheet
        '''
        'Input for setup'
        self.path_name_excel = path_name
        self.tower_init_file_path = path_name
        # self.pls_path = r"C:\Program Files\PLS"
        # self.tower_catalogues_path = r"C:\temp\pls\catalogues"
        # self.tower_init_file_path = r"C:\temp\pls\python_tower"
        # self.tower_init_file_name = r"test_tower_original.tow"

    @classmethod
    def read_all_input(cls, excel_path_name):
        cls_object = cls(excel_path_name)
        excel_object = pd.ExcelFile(os.path.join(cls_object.path_name_excel, "Input.xlsx"))
        cls_object._excel_read_general_sheet(excel_object, sheet="General")
        cls_object._excel_read_primary_joints(excel_object, sheet="PrimaryJoints")

    def _excel_read_general_sheet(self, excel_object, sheet):
        '''
        Read general information from Excel input sheet and store in TowerBuilder object

        :param pd.ExcelFile excel_object:
        :param str sheet:

        '''
        inp_df = excel_object.parse(
            index_col=0,
            skiprows=0,
            sheet_name=sheet
        )
        inp_df = inp_df.loc[inp_df.index.notna()]
        inp_df.index = [x.lower() for x in inp_df.index]
        self.pls_path = inp_df.loc["pls_path", "Value"]
        self.tower_catalogues_path = inp_df.loc["tow_cat", "Value"]
        self.tower_init_file_name = inp_df.loc["tow_base", "Value"]

    def _excel_read_primary_joints(self, excel_object, sheet):
        '''
        Read general information from Excel input sheet and store in TowerBuilder object

        :param pd.ExcelFile excel_object:
        :param str sheet:

        '''
        inp_df = excel_object.parse(
            index_col=0,
            skiprows=0,
            sheet_name=sheet,
        )
        inp_df = inp_df.loc[inp_df.index.notna()]
        inp_df.iloc[:, 4:] = inp_df.iloc[:, 4:].fillna(0).astype(int)
        a = 1

