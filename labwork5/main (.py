"""
Author: Nazarenko Andriy.
Group: K-11.
Variant: 52.
Main function.
"""
import sys
import load_data as ld
import information as info


def author_info() -> None:
    """
    Displays information about author of program.
    :return: None
    """
    print('Author: Nazarenko Andriy.\nGroup: K-11.\nVariant: 52.')


def task_condition() -> None:
    """
    Displays detailed task conditions.
    :return: None
    """
    print("""
Task: 
Process students` winter session results.
Find all students who received a state rating grade of 5 for each subject.
Display information on each of them:
    - On the first line:
    last name, first name, gradebook id, number of exams, stability, rating out of points (rounded to one mark);
    - On the following lines, starting with the tab, display for the student all his results (one per line):
    semester grade, exam grade, total grade, subject.
    In this sort: points in the semester, subject.
    """)


def start_notification() -> None:
    """
    Displays a notification of the start.
    :return: None
    """
    print('*****', end='')


def cmd_input() -> int or str:
    """
    Checks whether right command line input was given and, if yes, returns it.
    :return: int or str input.
    """
    if len(sys.argv) == 2:
        return sys.argv[1]
    else:
        raise Exception('Command Line Error.')


def main(ini_path0: str) -> None:
    """
    Processes given settings-file path and load it, makes an info object, which collect information,
    Calls the functions to load the main and additional file with main-file encoding and
     to output processed information to a given output file with its encoding.

    :param ini_path0: str path of the settings file.
    :return: None
    """
    ini = ld.load_ini(ini_path0)
    info_obj = info.Information()
    ld.load(info_obj, ini['input']['csv'], ini['input']['json'], ini['input']['encoding'])
    ld.output(info_obj, ini['output']['fname'], ini['output']['encoding'])


if __name__ == '__main__':
    try:
        author_info()
        task_condition()
        start_notification()
        ini_path = cmd_input()
        main(ini_path)
    except BaseException as e:
        print(f'\n***** program aborted *****\n{e}')
