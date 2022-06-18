"""
Author: Nazarenko Andriy.
Group: K-11
Variant: 52.
Load and output data functions.
"""
import json
import csv
import information as info


class Builder:
    """
    Builder class to process files.
    """

    @staticmethod
    def __check_csv_line(line: list) -> bool:
        """
        Checks whether csv line is correct.
        :param line: str Line of the main file.
        :return: bool Correctness of the line.
        """
        if not line:
            return False

        if len(line) != 9:
            raise Exception('CSV-file Error: line argument`s wrong number')

        total, semester, state_rating, exam, group, subject, name, gb_id, surname = line
        if not (total + semester + state_rating + exam + gb_id).isdigit():
            raise Exception('CSV-file Error: line argument`s wrong type')
        else:
            return True

    @staticmethod
    def __convert_fields(line: list) -> list:
        """
        Converts fields of the line to a proper type.
        :param line: list of words in the line.
        :return: list: list of words in the line in a proper type.
        """
        total, semester, state_rating, exam, group, subject, name, gb_id, surname = line
        return [int(total), int(semester), int(state_rating), int(exam), group, subject, name, gb_id, surname]

    def load_csv(self, info_obj: info.Information(), csv_name: str, encoding: str) -> None:
        """
        Writes converted fields of each csv-line to an Information class object if it is correct.
        :param info_obj: Information() object to collect information.
        :param csv_name: str Name of the csv file.
        :param encoding: str Encoding of the csv-file.
        :return: None.
        """
        print(f'input-csv {csv_name}: ', end='')
        info_obj.clear()
        reader = csv.reader(open(csv_name, encoding=encoding), delimiter=';')
        for line in reader:
            if self.__check_csv_line(line):
                total, semester, state_rating, exam, group, subject, name, gb_id, surname = self.__convert_fields(line)
                info_obj.add_info(total, semester, state_rating, exam, group, subject, name, gb_id, surname)
        print('OK')

    @staticmethod
    def __check_json(json_file: dict) -> None:
        """
        Check whether json file has all necessary keys.
        :param json_file: dict Read json file.
        :return: None.
        """
        keys = {"кількість недопусків", "кількість студентів без 'хвостиків'", "довжина найкоротшого прізвища"}
        if keys | set(json_file) != set(json_file) or \
                not all(isinstance(json_file[k], int) for k in keys):
            raise Exception('JSON-file Error.')

    def load_json(self, json_name: str, encoding: str) -> dict:
        """
        Loads necessary json values if the file is correct.
        :param json_name: str Name of the json file.
        :param encoding: str encoding of the json file.
        :return: dict With necessary json values.
        """
        print(f'input-json {json_name}: ', end='')
        json_file = json.load(open(json_name, encoding=encoding))
        self.__check_json(json_file)
        non_admissions = json_file["кількість недопусків"]
        non_debt = json_file["кількість студентів без 'хвостиків'"]
        shortest_surname = json_file["довжина найкоротшого прізвища"]
        print('OK')
        return {'n_a': non_admissions, 'n_d': non_debt, 'sh_s': shortest_surname}

    @staticmethod
    def compare_csv_to_json(info_obj: info.Information, jsonf: dict) -> bool:
        """
        Checks whether json values are relevant to csv-file statistics.
        :param info_obj: Information() object that collects information.
        :param jsonf: dict Necessary json values.
        :return: bool Equality of all fields.
        """
        csv_n_a = info_obj.get_non_admissions_num
        csv_n_d = info_obj.get_non_debts_num
        csv_sh_s = info_obj.get_min_surname_len
        return csv_n_a == jsonf['n_a'] and csv_n_d == jsonf['n_d'] and csv_sh_s == jsonf['sh_s']


def __check_ini(ini_file0: dict) -> None:
    """
    Checks whether ini file has all necessary keys.
    :param ini_file0: dict Read ini file.
    :return: None.
    """
    if {"input", "output"} | set(ini_file0) != set(ini_file0) or \
            {'encoding', 'csv', 'json'} | set(ini_file0["input"]) != set(ini_file0["input"]) or \
            {'fname', 'encoding'} | set(ini_file0["output"]) != set(ini_file0["output"]):
        raise Exception('INI-file Error.')


def load_ini(ini_path0: str) -> dict:
    """
    Loads ini file if it`s correct.
    :param ini_path0: str Path to the ini file.
    :return:dict Read ini file.
    """
    print(f'\nini {ini_path0}: ', end='')
    ini_file0 = json.load(open(ini_path0, encoding='utf-8'))
    __check_ini(ini_file0)
    print('OK')
    return ini_file0


def load(info_obj0: info.Information, csv_name0: str, json_name0: str, encoding0: str) -> None:
    """
    Loads all files with help of a Builder class object.
    :param info_obj0: Information object to collect information.
    :param csv_name0: str Path to the csv file.
    :param json_name0: str Path to the json file.
    :param encoding0: str Encoding of the csv-file.
    :return: None.
    """
    builder = Builder()
    builder.load_csv(info_obj0, csv_name0, encoding0)
    json_values0 = builder.load_json(json_name0, encoding0)
    print(f'json?=csv: ', end='')
    if builder.compare_csv_to_json(info_obj0, json_values0):
        print('OK')
    else:
        print('UPS')


def output(info_obj0: info.Information, output_fname0: str, encoding0: str) -> None:
    """
    Outputs the processed information to a file with it`s encoding by Information object methods.
    :param info_obj0: Information object to collect information.
    :param output_fname0: str Path to the output class object.
    :param encoding0: str Encoding of the output file.
    :return: None.
    """
    print(f'output {output_fname0}: ', end='')
    info_obj0.output(output_fname0, encoding0)
    print('OK')
