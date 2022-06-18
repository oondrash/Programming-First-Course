"""
Author: Nazarenko Andriy.
Group: K-11
Variant: 52.
Classes: Information, Student, Grades.
"""


class Information:
    """
    A class to collect, analise and represent information about students` winter session results.
    """

    def __init__(self) -> None:
        """
        Collects all necessary and additional fields for Information class object.
        """
        self.__students = {}
        self.__non_admissions = 0
        self.__non_debt_students = set()
        self.__min_surname_len = 25
        self.__exc_students = set()

    def clear(self) -> None:
        """
        Resets fields of the class to default values.
        :return: None
        """
        self.__students = {}
        self.__non_admissions = 0
        self.__non_debt_students = set()
        self.__min_surname_len = 25
        self.__exc_students = set()

    def add_info(self, total: int, semester: int, state_rating: int, exam: int, group: str, subject: str, name: str,
                 gb_id: str, surname: str) -> None:
        """
        Makes an Student object if it is not created before,
        otherwise, checks whether information about the student is equal,
        makes necessary analyses of given information.

        :param total: int Total grade for subject.
        :param semester: int Semester grade for the subject.
        :param state_rating: int State rating grade for the subject.
        :param exam: int Exam grade for the subject.
        :param group: str Group id of the student.
        :param subject: str Subject name.
        :param name: str Name of the student.
        :param gb_id: str Gradebook id.
        :param surname: str Surname of the student.
        :return: None
        """
        if gb_id not in self.__students:
            self.__students[gb_id] = _Student(group, name, gb_id, surname)
        else:
            self.__students[gb_id].compare_information(group, name, gb_id, surname)
        self.__students[gb_id].add_grades(total, semester, state_rating, exam, subject)
        self.__info_analyses(gb_id, state_rating, surname)

    def __non_admission_check(self, state_rating: int) -> None:
        """
        Checks whether non admission and counts its number.
        :param state_rating: int State rating grade for the subject.
        :return: None
        """
        if state_rating == 1:
            self.__non_admissions += 1

    def __non_debt_check(self, gb_id: str) -> None:
        """
        Checks whether student has no debts and, if yes, adds it to the field.
        Otherwise, discards it.
        :param gb_id: int Gradebook id to identify the student
        :return: None
        """
        if not self.__students[gb_id].has_debt():
            self.__non_debt_students.add(self.__students[gb_id])
        else:
            self.__non_debt_students.discard(self.__students[gb_id])

    def __min_surname_check(self, surname: str) -> None:
        """
        Checks whether given surname is the shortest and, if yes, keeps it len in a field.
        :param surname: str Surname of the student.
        :return:
        """
        surname_len = len(surname)
        if surname_len < self.__min_surname_len:
            self.__min_surname_len = surname_len

    def __excellent_student_check(self, gb_id: str) -> None:
        """
        Checks whether student has state rating grades for 5 for all subjects and,
        if yes, adds it to the field. Otherwise, discards it from the field.
        :param gb_id: int Gradebook id to identify the student.
        :return: None
        """
        if self.__students[gb_id].excellent_student():
            self.__exc_students.add(self.__students[gb_id])
        else:
            self.__exc_students.discard(self.__students[gb_id])

    def __info_analyses(self, gb_id: str, state_rating: int, surname: str) -> None:
        """
        Calls methods to check and, in positive case, save necessary information to the fields.
        :param gb_id: int Gradebook id to identify the student.
        :param state_rating: int State rating grade for the subject.
        :param surname: str Surname of the student.
        :return: None
        """
        self.__min_surname_check(surname)
        self.__non_admission_check(state_rating)
        self.__non_debt_check(gb_id)
        self.__excellent_student_check(gb_id)

    @property
    def get_non_admissions_num(self) -> int:
        """
        Getter of the number of non admissions.
        :return: int Number of non admissions.
        """
        return self.__non_admissions

    @property
    def get_non_debts_num(self) -> int:
        """
        Getter of the number of students who have no debts.
        :return: int Number of students who have no debts.
        """

        return len(self.__non_debt_students)

    @property
    def get_min_surname_len(self) -> int:
        """
        Getter of the shortest surname length.
        :return: int Shortest surname length.
        """
        return self.__min_surname_len

    def output(self, output_fname: str, encoding: str) -> None:
        """
        Outputs processed information to the output file with its encoding.
        :param output_fname: str Name of the output file.
        :param encoding: str Encoding of the output file.
        :return: None
        """
        with open(output_fname, 'w', encoding=encoding) as output_file:
            for st in self.__exc_students:
                output_file.write(f'{str(st)}\n')


class _Student:
    """
    A class to collect, analise and represent information about a specific student.
    """

    def __init__(self, group: str, name: str, gb_id: str, surname: str):
        """
        Collects all necessary and additional fields for Student class object.
        :param group: str Group of the student.
        :param name: str Name of the student.
        :param gb_id: str Gradebook id of the student.
        :param surname: str Surname of the student.
        """
        if 0 < len(name) <= 27 and 0 < len(surname) <= 24 and 0 < len(group) <= 4 and len(gb_id) == 7:
            self.__name = name
            self.__surname = surname
            self.__gb_id = gb_id
            self.__group = group
            self.__grades = []
        else:
            raise Exception('Incorrect Student object`s information.')

    def __repr__(self) -> str:
        """
        Fully represents the student.
        :return: str
        """
        num_of_exams = self.__num_of_exams()
        stability = self.__stability()
        rating = self.__rating()
        grades = self.__sort_grades()
        return f'{self.__surname}\t{self.__name}\t{self.__gb_id}\t{num_of_exams}\t{stability}\t{rating}\n{grades}'

    def add_grades(self, total_grade: int, semester_grade: int, state_rating: int, exam_grade: int,
                   subject: str) -> None:
        """
        Adds grades for the subject if student have not passed it already.
        :param total_grade: int Total grade for the subject.
        :param semester_grade: int Total grade for the subject.
        :param state_rating: int Total grade for for subject.
        :param exam_grade: int Total grade for for subject.
        :param subject: str Name of the subject.
        :return: None
        """
        if not any(grade.get_subject_name == subject for grade in self.__grades):
            self.__grades.append(_Grades(total_grade, semester_grade, state_rating, exam_grade, subject))
        else:
            raise Exception('Student cant pass one subject more than one time.')

    def compare_information(self, group: str, name: str, gb_id: str, surname: str) -> None:
        """
        Checks whether repeated student`s information is equal.
        Otherwise exception is raised.
        :param group: str Group of the student.
        :param name: str Name of the student.
        :param gb_id: str Gradebook id of the student.
        :param surname: str Surname of the student.
        :return: None
        """
        if self.__name != name or self.__surname != surname or \
                self.__gb_id != gb_id or self.__group != group:
            raise Exception('Incorrect Student object`s information.')

    def has_debt(self) -> bool:
        """
        Checks whether student has debts.
        :return: bool
        """
        return all(subj.get_state_rating in {0, 1, 2} for subj in self.__grades)

    def excellent_student(self) -> bool:
        """
        Checks whether student is an excellent student.
        :return: bool
        """
        return all(subj.get_state_rating == 5 for subj in self.__grades)

    def __stability(self) -> int:
        """
        Counts the stability of the student.
        :return: int Stability of the student
        """
        grades = self.__grades
        highest_g = max(g.get_total for g in grades)
        lowest_g = min(g.get_total for g in grades)
        return highest_g - lowest_g

    def __num_of_exams(self) -> int:
        """
        Counts the number of exams.
        :return: int Number of exams
        """
        return len(self.__grades)

    def __rating(self) -> float:
        """
        Counts the rating of the student.
        :return: float Rating of the student.
        """
        grades = self.__grades
        total_grades = [g.get_total for g in grades]
        rating = sum(total_grades) / len(total_grades)
        return round(rating, 1)

    def __sort_grades(self) -> str:
        """
        Sorts the grades and converts it to str.
        :return: str Grades of the student.
        """
        self.__grades.sort(key=lambda x: (x.get_total, x.get_subject_name))
        grades_str = ''
        for g in self.__grades:
            grades_str += str(g)
        return grades_str


class _Grades:
    """
    A class to collect, analise and represent information about subject results of the student.
    """

    def __init__(self, total_grade: int, semester_grade: int, state_rating: int, exam_grade: int,
                 subject_name: str):
        """
        Collects all necessary and additional fields for Grades class object.
        :param total_grade: int Total grade for the subject.
        :param semester_grade: int Semester grade for the subject.
        :param state_rating: int State rating grade for the subject.
        :param exam_grade: int Exam grade for the subject.
        :param subject_name: str Name for the subject.
        """
        if self.__check_args(total_grade, semester_grade, state_rating, exam_grade, subject_name):
            self.__total = total_grade
            self.__semester = semester_grade
            self.__exam = exam_grade
            self.__state_rating = state_rating
            self.__subject_name = subject_name
        else:
            raise Exception('Wrong Grades object`s information.')

    def __repr__(self) -> str:
        """
        Represents grades for a subject.
        :return:
        """
        return f'\t{self.get_total}\t{self.__exam}\t{self.__semester}\t{self.__state_rating}\t{self.get_subject_name}\n'

    @staticmethod
    def __check_args(total_grade: int, semester_grade: int, state_rating: int, exam_grade: int,
                     subject_name: str) -> bool:
        """
        Checks whether arguments of Grades class object are correct.
        :param total_grade: int Total grade for the subject.
        :param semester_grade: int Semester grade for the subject.
        :param state_rating: int State rating grade for the subject.
        :param exam_grade: int Exam grade for the subject.
        :param subject_name: str Name for the subject.
        :return: bool
        """
        if 4 <= len(subject_name) <= 70 and semester_grade + exam_grade == total_grade \
                and (24 <= exam_grade <= 40 or exam_grade == 0) and 0 < semester_grade <= 60:
            return (90 <= total_grade <= 100 and state_rating == 5) \
                   or (75 <= total_grade < 90 and state_rating == 4) \
                   or (60 <= total_grade < 75 and state_rating == 3) \
                   or (0 <= total_grade < 60 and state_rating == 2) \
                   or (0 <= total_grade < 60 and state_rating in {1, 0})
        else:
            return False

    @property
    def get_state_rating(self) -> int:
        """
        Getter of the state rating grade for the subject.
        :return: int State rating grade.
        """
        return self.__state_rating

    @property
    def get_total(self) -> int:
        """
        Getter of the total grade for the subject.
        :return: int Total grade for the subject.
        """
        return self.__total

    @property
    def get_subject_name(self) -> str:
        """
        Getter of the name of the subject.
        :return: str Name of the subject.
        """
        return self.__subject_name
