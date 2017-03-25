import copy

import random
random.seed(1)

class CSP_Solver(object):
    # CSP Solver using min conflicts algorithm
    # See assignment description for details regarding the return value of each method

    def get_num_of_conflicts(self, student, arrangement):
        """ Returns the number of conflicts of a given student in a given sitting arrangement configuration.
        """
        # first, let's check equality of column size at each row in the given arrangement
        self.check_suitability(arrangement)
        # checking the sitting place of the given student in given arrangement
        nrow, ncol = len(arrangement), len(arrangement[0])
        row_num, col_num = -1, -1
        for row in range(nrow):
            for col in range(ncol):
                if arrangement[row][col] == student:
                    row_num = row
                    col_num = col
        if (row_num, col_num) == (-1, -1):
            raise AttributeError("This students is not sitting in anywhere in this arrangement.")
        # at next, checking places around student for any conlict
        conflict_dict = CSP_Solver().get_conflicts_from_txt("conflicts.txt")
        hasConflictWith = conflict_dict[student]
        num_of_conflicts = 0
        if (row_num > 0) and (row_num < nrow):
            if (arrangement[row_num - 1][col_num] in hasConflictWith):
                num_of_conflicts += 1
            if (col_num > 0) and (col_num < ncol):
                if (arrangement[row_num - 1][col_num - 1] in hasConflictWith):
                    num_of_conflicts += 1
            if (col_num < (ncol - 1)) and (col_num >= 0):
                if (arrangement[row_num - 1][col_num + 1] in hasConflictWith):
                    num_of_conflicts += 1
        if (row_num < (nrow - 1)) and (row_num >= 0):
            if (arrangement[row_num + 1][col_num] in hasConflictWith):
                num_of_conflicts += 1
            if (col_num > 0) and (col_num < ncol):
                if (arrangement[row_num + 1][col_num - 1] in hasConflictWith):
                    num_of_conflicts += 1
            if (col_num < (ncol - 1)) and (col_num >= 0):
                if (arrangement[row_num + 1][col_num + 1] in hasConflictWith):
                    num_of_conflicts += 1
        if (col_num > 0) and (col_num < ncol):
            if (arrangement[row_num][col_num - 1] in hasConflictWith):
                num_of_conflicts += 1
        if (col_num < (ncol - 1)) and (col_num >= 0):
            if (arrangement[row_num][col_num + 1] in hasConflictWith):
                num_of_conflicts += 1
        # result...
        return num_of_conflicts

    def get_total_conflicts(self, arrangement):
        """ Returns the total number of conflicts present in a given arrangement.
        """
        total_conflicts = 0
        nrow, ncol = len(arrangement), len(arrangement[0])
        for row in range(nrow):
            for col in range(ncol):
                total_conflicts += self.get_num_of_conflicts((arrangement[row][col]),arrangement)
        return total_conflicts
    
    def find_a_random_student(self, arrangement):
        return arrangement[random.randint(0,3)][random.randint(0,3)]

    def get_best_arrangement(self, student, current_arrangement):
        """ Returns the next arrangement for a given student that will give the minimum number of overall conflicts.
        """
        # first, let's check equality of column size at each row in the given arrangement
        self.check_suitability(current_arrangement)
        # next, check for the best arrangement ...
        checkedStudents = [student]
        best_swap = self.search_best_swap(student, current_arrangement, current_arrangement, checkedStudents)
        return best_swap

    def solve_csp(self, arrangement):
        total_conflicts = self.get_total_conflicts(arrangement)
        best_arrangement = copy.deepcopy(arrangement)
        max_repeat = 5
        repeat = 0
        while total_conflicts > 0:
            new_best_arrangement = copy.deepcopy(best_arrangement)
            for row in range(len(best_arrangement)):
                for col in range(len(best_arrangement[row])):
                    new_arrangement =self.get_best_arrangement(best_arrangement[row][col],best_arrangement)
                    new_total_conflicts = self.get_total_conflicts(new_arrangement)
                    if new_total_conflicts < total_conflicts:
                        new_best_arrangement = new_arrangement
                        total_conflicts = new_total_conflicts
                        #print(total_conflicts)
            if best_arrangement == new_best_arrangement:
                repeat += 1
                if repeat >= max_repeat:
                    break
            else:
                best_arrangement = new_best_arrangement
                repeat = 0
        return best_arrangement

    ####################################################################################################################

    def get_conflicts_from_txt(self, file1):
        """ This function takes the txt file of conflicts as an input and transforms it's data to a dictionary.
        """
        textFile = open(file1)
        text = textFile.read()
        conflicts_dict = {}
        for line in text.split("\n"):
            studentMain = line.strip().split("-")[0]
            hasConflictWith = [student for student in line.strip().split("-")[1].split(",")]
            conflicts_dict[studentMain] = hasConflictWith
        return conflicts_dict

    def num_all_students(self, arrangement):
        num_students = 0
        for row in range(len(arrangement)):
            for col in range(len(arrangement[row])):
                num_students += 1
        return num_students

    def check_suitability(self, arrangement):
        num_students = self.num_all_students(arrangement)
        num_equal_col_at_each_row = len(arrangement) * len(arrangement[0])
        if num_equal_col_at_each_row == num_students:
            return True
        else:
            raise IndexError("Given arrangement doesn't have equal column size at each row.")

    def swap(self, student1, student2, current_arrangement):
        row1, col1, row2, col2 = 0, 0, 0, 0
        nrow, ncol = len(current_arrangement), len(current_arrangement[0])
        new_arrangement = copy.deepcopy(current_arrangement)
        for row in range(nrow):
            for col in range(ncol):
                if current_arrangement[row][col] == student1:
                    row1, col1 = row, col
                elif current_arrangement[row][col] == student2:
                    row2, col2 = row, col
        new_arrangement[row1][col1] = student2
        new_arrangement[row2][col2] = student1
        return new_arrangement

    def search_best_swap(self, student, current_arrangement, minConflictedArrangement, checkedStudents):
        randomSelect = self.find_a_random_student(current_arrangement)
        num_students = self.num_all_students(current_arrangement)
        if randomSelect in checkedStudents:
            if len(checkedStudents) < num_students:
                repeat = self.search_best_swap(student, current_arrangement, minConflictedArrangement, checkedStudents)
                return repeat
            else:
                return minConflictedArrangement
        else:
            checkedStudents.append(randomSelect)
            min_num_of_conflicts = self.get_total_conflicts(minConflictedArrangement)
            new_arrangement = self.swap(student, randomSelect, current_arrangement)
            new_num_of_conflicts = self.get_total_conflicts(new_arrangement)
            if new_num_of_conflicts < min_num_of_conflicts:
                follow_min = self.search_best_swap(student, current_arrangement, new_arrangement, checkedStudents)
                return follow_min
            elif new_num_of_conflicts == min_num_of_conflicts:
                repeat = self.search_best_swap(student, current_arrangement, minConflictedArrangement, checkedStudents)
                return repeat
            else:
                repeat = self.search_best_swap(student, current_arrangement, minConflictedArrangement, checkedStudents)
                return repeat

########################################################################################################################
########################################################################################################################

init_arrangement = [ ["Alan","Bill","Jack","Jeff"],
                     ["Dan","Dave","Jill","Joe"],
                     ["John","Kim","Sam","Sue"],
                     ["Mike","Nick","Tom","Will"] ]

print(">>>init_arrangement")
print(init_arrangement)

print(">>>CSP_Solver().get_num_of_conflicts(\"Jill\", init_arrangement)")
print(CSP_Solver().get_num_of_conflicts("Will", init_arrangement))

print(">>>CSP_Solver().get_total_conflicts(init_arrangement)")
print(CSP_Solver().get_total_conflicts(init_arrangement))

print(">>>CSP_Solver().get_best_arrangement(\"Kim\", init_arrangement)")
print(CSP_Solver().get_best_arrangement("Kim", init_arrangement))

print(">>>CSP_Solver().solve_csp(init_arrangement)")
print(CSP_Solver().solve_csp(init_arrangement))