import numpy as np


def calculate_grade(exam: float, coursework: float, overall: float) -> str:
    """
    Calculates the grade based on exam, coursework, and overall marks.

    Parameters:
    exam (float): The exam mark
    coursework (float): The coursework mark
    overall (float): The overall mark

    Returns:
    str: The grade ('first', 'second', 'third', or 'failed')
    """
    if exam < 30 or coursework < 30:
        return "failed"

    if overall >= 70:
        return "first"
    elif 50 <= overall <= 69:
        return "second"
    elif 40 <= overall <= 49:
        return "third"
    else:
        return "failed"


def process_students_mark(students_data: np.ndarray, number: int) -> np.ndarray:
    """
    Processes student marks and creates structured array with grades.

    Parameters:
    students_data (np.ndarray): Array containing student data
    number (int): Number of students to process

    Returns:
    np.ndarray: Sorted structured array containing student information and grades
    """
    studType = [('reg_number', int), ('exam_mark', float), ('coursework_mark', float),
                ('overall_mark', float), ('grade', 'S20')]
    students = np.array([(0, 0, 0, 0, '') for _ in range(number)], dtype=studType)
    for m in range(number):
        regis = students_data[m][0]
        exam = round(students_data[m][1])
        coursework = round(students_data[m][2])
        overall = round(students_data[m][3])
        grade = calculate_grade(exam, coursework, overall)
        students[m] = (regis, exam, coursework, overall, grade)

    sorted_students = np.sort(students, order='overall_mark')

    return sorted_students


def write_output_file(students: np.ndarray, output_file: str) -> None:
    """
    Writes student data to output file.

    Parameters:
    students (np.ndarray): Array containing processed student data
    output_file (str): Name of the file to write to

    Returns:
    None
    """
    with open(output_file, 'w') as f:
        print(students, file=f)
    print("Write output file successfully!")
    return


def read_input_file() -> tuple:
    """
    Reads student data from input file.

    Returns:
    tuple: Contains two elements:
        - np.ndarray: Raw student data
        - str: Number of students
    """
    while True:
        try:
            file_name = input("Input file name (include extension) : ")
            with open(file_name, 'r') as file:
                print(f"{file_name} opened successfully")
                number, coursework_wight = file.readline().split()
                raw_students_data = np.array([[0, 0.0, 0.0, 0.0]] * int(number))
                i = 0
                for line in file:
                    reg_number, exam_mark, coursework_mark = line.strip().split()
                    raw_students_data[i][0] = int(reg_number)
                    raw_students_data[i][1] = float(exam_mark)
                    raw_students_data[i][2] = float(coursework_mark)
                    raw_students_data[i][3] = (float(coursework_mark) * (float(coursework_wight) / 100)) + (
                            float(exam_mark) * (100 - float(coursework_wight)) / 100)
                    i += 1
                return raw_students_data, number
        except FileNotFoundError:
            print("Incorrect file name!")


def analyze_grade_output(output: np.ndarray) -> tuple:
    """
    Analyzes grade distribution from processed student data.

    Parameters:
    output (np.ndarray): Array containing processed student data

    Returns:
    tuple: Contains five elements:
        - int: Count of first class grades
        - int: Count of second class grades
        - int: Count of third class grades
        - int: Count of failed grades
        - list: Registration numbers of failed students
    """
    count_first, count_second, count_third, count_failed = 0, 0, 0, 0
    failed_students = []
    for i in range(output.size):
        if output[i][4].decode('utf-8') == "first":
            count_first += 1
        elif output[i][4].decode('utf-8') == "second":
            count_second += 1
        elif output[i][4].decode('utf-8') == "third":
            count_third += 1
        elif output[i][4].decode('utf-8') == "failed":
            failed_students.append(output[i][0])
            count_failed += 1
    return count_first, count_second, count_third, count_failed, failed_students


if __name__ == "__main__":
    input_students, number_of_students = read_input_file()
    output_students = process_students_mark(input_students, int(number_of_students))
    write_output_file(output_students, "ex5data_out.txt")

    number_of_first_class_students, number_of_second_class_students, number_of_third_class_students, number_of_failed_students, all_failed_students = analyze_grade_output(
        output_students)

    print(f"Number of students who have first-class marks : {number_of_first_class_students}")
    print(f"Number of students who have second-class marks : {number_of_second_class_students}")
    print(f"Number of students who have third-class marks : {number_of_third_class_students}")
    print(f"Number of students who have failed : {number_of_failed_students}")
    print(f"Students who have failed : {all_failed_students}")
