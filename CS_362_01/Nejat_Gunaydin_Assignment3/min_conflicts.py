import random
random.seed(1)

class CSP_Solver(object):
    # CSP Solver using min conflicts algorithm
    # See assignment description for details regarding the return value of each method
    def get_num_of_conflicts(self, student, arrangement):
        nrow, ncol = len(arrangement), len(arrangement[0])
        row_num, col_num = -1, -1
        for row in range(nrow):
            for col in range(ncol):
                if arrangement[row][col] == student:
                    row_num = row
                    col_num = col
        if (row_num, col_num) != (-1, -1):

            return row_num, col_num
        else:
            raise AttributeError("This students is not sitting in anywhere in this arrangement.")

    def get_total_conflicts(self, arrangement):
        pass
    
    def find_a_random_student(self, arrangement):
        return arrangement[random.randint(0,3)][random.randint(0,3)]

    def get_best_arrangement(self, student, current_arrangement):
        pass

    def solve_csp(self, arrangement):
        pass

########################################################################################################################

def get_conflicts_from_txt(file):
    """

    :param file:
    :return:
    """
    textFile = open(file)
    text = textFile.read()
    conflicts_dict = {}
    for line in text.split("\n"):
        studentMain = line.strip().split("-")[0]
        hasConflictWith = [student for student in line.strip().split("-")[1].split(",")]
        conflicts_dict[studentMain] = hasConflictWith
    return conflicts_dict



init_arrangement = [ ["Alan","Bill","Jack","Jeff"],
                     ["Dan","Dave","Jill","Joe"],
                     ["John","Kim","Sam","Sue"],
                     ["Mike","Nick","Tom","Will"] ]

get_conflicts_from_txt("conflicts.txt")
conflict_dict = get_conflicts_from_txt("conflicts.txt")

print CSP_Solver().get_num_of_conflicts("Jill", init_arrangement)