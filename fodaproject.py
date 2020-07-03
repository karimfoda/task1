from sympy import *
from numpy import *
from array import array
import sys
from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication, QVBoxLayout, QWidget, QFormLayout, QLabel,
                               QMessageBox)
from pyqtgraph import PlotWidget


class Window(QWidget):
    # Creating the constructor
    def __init__(self):
        super().__init__()
        # Adjusting the plot
        self.pg = PlotWidget()
        self.pg.plot()
        # Adjusting the window
        self.setWindowTitle('Function Plotter')
        self.setGeometry(400, 100, 600, 500)
        # Creating welcome message and some instructions to the user
        self.message = QLabel()
        self.message1 = QLabel()
        self.message2 = QLabel()
        # Creating text boxes
        self.box = QLineEdit()
        self.box1 = QLineEdit()
        self.box2 = QLineEdit()
        # Creating the plot button
        self.button = QPushButton("Plot f(x)")
        # Choosing and adjusting the layouts
        self.layout = QVBoxLayout()
        self.nested_layout = QFormLayout()
        self.nested_layout.addRow('**Welcome to Function Plotter**', self.message)
        self.nested_layout.addRow('The operators supplied are:+,-,*,/,^', self.message1)
        self.nested_layout.addRow('Please enter the function of (x), its minimum and maximum value', self.message2)
        self.nested_layout.addRow('f(x)', self.box)
        self.nested_layout.addRow('Minimum Value', self.box1)
        self.nested_layout.addRow('Maximum Value', self.box2)
        self.layout.addLayout(self.nested_layout)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.pg)
        self.setLayout(self.layout)
        # Connecting the plot button to the functions which needs to be executed
        self.button.clicked.connect(self.my_function)

    def my_function(self):
        # This is the main function that calls all functions responsible for handling and executing the mathematical
        # function entered by the user
        self.pg.clear()  # Clearing the plot
        expr = self.input_expression()
        expr = self.lowercase_string(expr)
        expr = self.remove_spaces(expr)
        expr, flag = self.expression_error_alert(expr)
        if flag == True:
            minimum, maximum = self.min_and_max_values()
            minimum, maximum, flag2 = self.min_and_max_values_error(minimum, maximum)
            if flag2 == True:
                expr = self.exponent_operator(expr)
                expr = self.valid_expression(expr)
                input_array, output_array = self.evaluating_expression(expr, minimum, maximum)
                self.pg.plot(input_array, output_array, pen='b')
                QMessageBox.information(self, 'Success', 'Successful Operation')

    def input_expression(self):
        # This function takes the function of x from the user
        expr = self.box.text()
        return expr

    def lowercase_string(self, expr):
        # This function lowercases all letters in the expression in case the user
        # entered capital letters
        expr = expr.lower()
        return expr

    def remove_spaces(self, expr):
        # This function removes all spaces in case the user entered spaces
        expr = expr.replace(' ', '')
        return expr

    def expression_error_alert(self, expr):
        # This function handles many of the typing errors caused by the user
        numbers = '0123456789'
        operators = '+-*/^'
        variable = 'x'
        brackets = '()'
        valid = numbers + operators + variable + brackets
        number_of_opening_brackets = 0
        number_of_closing_brackets = 0
        flag_for_validation = True
        # The following condition is used to detect if the user did not enter any function
        if expr == '':
            flag_for_validation = False
            message = 'No function entered!'
            self.error_box(message)
        for i in range(len(expr)):
            # The following condition is used to detect and calculate the number
            # of opening brackets in the expression
            if expr[i] == '(':
                number_of_opening_brackets = number_of_opening_brackets + 1
            # The following condition is used to detect and calculate the number
            # of closing brackets in the expression
            elif expr[i] == ')':
                number_of_closing_brackets = number_of_closing_brackets + 1
            # The following condition is used to guarantee that all the inputs are
            # valid (variable or operators or numbers or brackets)
            if expr[i] not in (valid):
                flag_for_validation = False
                message = 'A wrong symbol or variable is used'
                self.error_box(message)
            # The following condition is used to detect if the user ended the
            # expression with an operator
            elif expr[len(expr) - 1] in operators:
                flag_for_validation = False
                message = 'The function can not be ended with an operator'
                self.error_box(message)
        # The following condition is used to detect if the user entered the
        # number of opening brackets not equal to that of closing brackets
        if number_of_opening_brackets != number_of_closing_brackets:
            flag_for_validation = False
            message = 'Number of opening brackets does not equal to that of closing brackets'
            self.error_box(message)
        for i in range(len(expr) - 1):
            # The following condition is used to detect if the user entered the
            # variable and the number without any operator between them
            if expr[i] in numbers and expr[i + 1] in variable:
                flag_for_validation = False
                message = 'An operator is missing between a number and the variable'
                self.error_box(message)
            # The following condition is used to detect if the user entered the
            # variable twice or more
            elif expr[i] in variable and expr[i + 1] in variable:
                flag_for_validation = False
                message = 'A variable can not be followed by a variable'
                self.error_box(message)
            # The following condition is used to detect if the user entered the
            # operator twice or more
            elif expr[i] in operators and expr[i + 1] in operators:
                flag_for_validation = False
                message = 'An operator can not be followed by an operator'
                self.error_box(message)
            # The following condition is used to detect if the user entered an opening bracket followed directly
            # by a closing bracket
            elif expr[i] == '(' and expr[i + 1] == ')':
                flag_for_validation = False
                message = 'An opening bracket can not be followed directly by a closing bracket'
                self.error_box(message)
            # The following condition is used to detect if the user entered a closing bracket followed directly
            # by an opening bracket with no operator between them
            elif expr[i] == ')' and expr[i + 1] == '(':
                flag_for_validation = False
                message = 'An operator is missing between the two opposite brackets'
                self.error_box(message)
            # The following condition is used to detect if the user entered a number followed directly
            # by an opening bracket with no operator between them
            elif expr[i] in numbers and expr[i + 1] == '(':
                flag_for_validation = False
                message = 'A number can not be followed directly by an opening bracket'
                self.error_box(message)
            # The following condition is used to detect if the user entered a closing bracket followed directly
            # by a number with no operator between them
            elif expr[i] == ')' and expr[i + 1] in numbers:
                flag_for_validation = False
                message = 'A closing bracket can not be followed directly by a number'
                self.error_box(message)
            # The following condition is used to detect if the user entered a variable followed directly
            # by an opening bracket with no operator between them
            elif expr[i] in variable and expr[i + 1] == '(':
                flag_for_validation = False
                message = 'A variable can not be followed directly by an opening bracket'
                self.error_box(message)
            # The following condition is used to detect if the user entered a closing bracket followed directly
            # by a variable with no operator between them
            elif expr[i] == ')' and expr[i + 1] in variable:
                flag_for_validation = False
                message = 'A closing bracket can not be followed directly by a variable'
                self.error_box(message)
            # The following condition is used to detect if the user entered an operator followed directly
            # by a closing bracket
            elif expr[i] in operators and expr[i + 1] == ')':
                flag_for_validation = False
                message = 'An operator can not be followed directly by a closing bracket'
                self.error_box(message)
            # The following condition is used to detect if the user entered an opening bracket followed directly
            # by *, / or ^ operators
            elif expr[i] == '(' and expr[i + 1] in ('*', '/', '^'):
                flag_for_validation = False
                message = 'An opening bracket can not be followed directly by *,/ or ^ operators'
                self.error_box(message)
        return expr, flag_for_validation

    def min_and_max_values(self):
        # This function is used to take the maximum and minimum values of x from the user
        minimum = self.box1.text()
        maximum = self.box2.text()
        return minimum, maximum

    def min_and_max_values_error(self, minimum, maximum):
        # This function is used to detect if the user entered the minimum and
        # maximum values wrongly or did not enter any or both of them
        flag_of_validation = True
        # The following condition is used to detect if the user did not enter neither the minimum nor th maximum
        # values
        if minimum == '' and maximum == '':
            flag_of_validation = False
            message = 'Neither the minimum nor the maximum values were entered!'
            self.error_box(message)
        # The following condition is used to detect if the user did not enter the minimum value
        elif minimum == '':
            flag_of_validation = False
            message = 'No minimum value was entered!'
            self.error_box(message)
        # The following condition is used to detect if the user did not enter the maximum value
        elif maximum == '':
            flag_of_validation = False
            message = 'No maximum value was entered!'
            self.error_box(message)
        # The following condition is used to convert both the minimum and the maximum values to float numbers
        # and checking for error in typing the numbers
        else:
            minimum = float(minimum)
            maximum = float(maximum)
            # The following condition is used to detect if the user entered the minimum value larger than
            # the maximum value
            if minimum > maximum:
                message = 'Value of Minimum is not smaller than that of Maximum'
                self.error_box(message)
                flag_of_validation = False
            # The following condition is used to detect if the user entered the minimum value equal to the
            # maximum value
            elif minimum == maximum:
                message = 'There is no range of values to be plotted'
                QMessageBox.warning(self, 'Warning', message)
        return minimum, maximum, flag_of_validation

    def exponent_operator(self, expr):
        # This function is used to convert the exponent operator from ^ to ** that
        # can be defined in python
        expr = expr.replace('^', '**')
        return expr

    def valid_expression(self, expr):
        # This function is used to convert the string into a function of x that
        # can be computed then
        expr = sympify(expr)
        return expr

    def evaluating_expression(self, expr, minimum, maximum):
        # This function is used to evaluate the function of x by substituting
        # with the range from the minimum to the maximum values entered by the user
        # and making an input array and an output array
        input_array = array('d')
        output_array = array('d')
        step_size = 0.001
        x = symbols('x')
        # Creating the input and output arrays
        for value in arange(minimum, maximum + step_size, step_size):
            input_array.append(float(value))
            output_array.append(float(expr.subs(x, value)))
        return input_array, output_array

    def error_box(self,message):
        # This function gives the error messages to the user that he did one or more wrong thing
        QMessageBox.critical(self, 'Error Message', message)


if __name__ == '__main__':
    # Create the Qt Application
    my_app = QApplication(sys.argv)
    # Create and show the form
    my_window = Window()
    my_window.show()
    # Run the main Qt loop
    sys.exit(my_app.exec_())
