#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name:        logical_expression
# Purpose:     Contains logical_expression class, inference engine,
#              and assorted functions
#
# Created:     09/25/2011
# Last Edited: 07/22/2013  
# Notes:       *This contains code ported by Christopher Conly from C++ code
#               provided by Dr. Vassilis Athitsos
#              *Several integer and string variables are put into lists. This is
#               to make them mutable so each recursive call to a function can
#               alter the same variable instead of a copy. Python won't let us
#               pass the address of the variables, so put it in a list which is
#               passed by reference. We can also now pass just one variable in
#               the class and the function will modify the class instead of a
#               copy of that variable. So, be sure to pass the entire list to a
#               function (i.e. if we have an instance of logical_expression
#               called le, we'd call foo(le.symbol,...). If foo needs to modify
#               le.symbol, it will need to index it (i.e. le.symbol[0]) so that
#               the change will persist.
#              *Written to be Python 2.4 compliant for omega.uta.edu
#-------------------------------------------------------------------------------

import sys
from copy import copy

#-------------------------------------------------------------------------------
# Begin code that is ported from code provided by Dr. Athitsos
class logical_expression:
    """A logical statement/sentence/expression class"""
    # All types need to be mutable, so we don't have to pass in the whole class.
    # We can just pass, for example, the symbol variable to a function, and the
    # function's changes will actually alter the class variable. Thus, lists.
    def __init__(self):
        self.symbol = ['']
        self.connective = ['']
        self.subexpressions = []


def print_expression(expression, separator):
    """Prints the given expression using the given separator"""
    if expression == 0 or expression == None or expression == '':
        print '\nINVALID\n'

    elif expression.symbol[0]: # If it is a base case (symbol)
        sys.stdout.write('%s' % expression.symbol[0])

    else: # Otherwise it is a subexpression
        sys.stdout.write('(%s' % expression.connective[0])
        for subexpression in expression.subexpressions:
            sys.stdout.write(' ')
            print_expression(subexpression, '')
            sys.stdout.write('%s' % separator)
        sys.stdout.write(')')


def read_expression(input_string, counter=[0]):
    """Reads the next logical expression in input_string"""
    # Note: counter is a list because it needs to be a mutable object so the
    # recursive calls can change it, since we can't pass the address in Python.
    result = logical_expression()
    length = len(input_string)
    while True:
        if counter[0] >= length:
            break

        if input_string[counter[0]] == ' ':    # Skip whitespace
            counter[0] += 1
            continue

        elif input_string[counter[0]] == '(':  # It's the beginning of a connective
            counter[0] += 1
            read_word(input_string, counter, result.connective)
            read_subexpressions(input_string, counter, result.subexpressions)
            break

        else:  # It is a word
            read_word(input_string, counter, result.symbol)
            break
    return result


def read_subexpressions(input_string, counter, subexpressions):
    """Reads a subexpression from input_string"""
    length = len(input_string)
    while True:
        if counter[0] >= length:
            print '\nUnexpected end of input.\n'
            return 0

        if input_string[counter[0]] == ' ':     # Skip whitespace
            counter[0] += 1
            continue

        if input_string[counter[0]] == ')':     # We are done
            counter[0] += 1
            return 1

        else:
            expression = read_expression(input_string, counter)
            subexpressions.append(expression)


def read_word(input_string, counter, target):
    """Reads the next word of an input string and stores it in target"""
    word = ''
    while True:
        if counter[0] >= len(input_string):
            break

        if input_string[counter[0]].isalnum() or input_string[counter[0]] == '_':
            target[0] += input_string[counter[0]]
            counter[0] += 1

        elif input_string[counter[0]] == ')' or input_string[counter[0]] == ' ':
            break

        else:
            print('Unexpected character %s.' % input_string[counter[0]])
            sys.exit(1)


def valid_expression(expression):
    """Determines if the given expression is valid according to our rules"""
    if expression.symbol[0]:
        return valid_symbol(expression.symbol[0])

    if expression.connective[0].lower() == 'if' or expression.connective[0].lower() == 'iff':
        if len(expression.subexpressions) != 2:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() == 'not':
        if len(expression.subexpressions) != 1:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() != 'and' and \
         expression.connective[0].lower() != 'or' and \
         expression.connective[0].lower() != 'xor':
        print('Error: unknown connective %s.' % expression.connective[0])
        return 0

    for subexpression in expression.subexpressions:
        if not valid_expression(subexpression):
            return 0
    return 1


def valid_symbol(symbol):
    """Returns whether the given symbol is valid according to our rules."""
    if not symbol:
        return 0

    for s in symbol:
        if not s.isalnum() and s != '_':
            return 0
    return 1

# End of ported code
#-------------------------------------------------------------------------------
# Add all your functions here

def current_model(statement):
    # Creating an empty Dictionary to store the current model
    model = {}
    # If the symbol has a value in knowledge base, then adding it to model
    for expression in statement.subexpressions:
        if expression.symbol[0]:
            model[expression.symbol[0]] = True
        elif expression.connective[0].lower() == 'not' and expression.subexpressions[0].symbol[0]:
            model[expression.subexpressions[0].symbol[0]] = False
    return model

def all_symbols(statement):
    # Creating an Empty List
    result = []
    # Appending the symbol if exists in the current statement
    if statement.symbol[0]:
        result.append(statement.symbol[0])
    else:
        # Appending symbols from all subexpressions
        for expression in statement.subexpressions:
            exp_symbols = all_symbols(expression)
            for symbol in exp_symbols:
                if symbol not in result:
                    result.append(symbol)
    return result

def pl_true(statement, model):

    if statement.symbol[0]:
        return model[statement.symbol[0]]

    elif statement.connective[0].lower() == 'if':
        if pl_true(statement.subexpressions[0], model) and (not pl_true(statement.subexpressions[1], model)):
            return False
        else:
            return True

    elif statement.connective[0].lower() == 'iff':
        if pl_true(statement.subexpressions[0], model) == pl_true(statement.subexpressions[1], model):
            return True
        else:
            return False

    elif statement.connective[0].lower() == 'not':
        return not pl_true(statement.subexpressions[0], model)

    elif statement.connective[0].lower() == 'and':
        result = True
        for expression in statement.subexpressions:
            result = result and pl_true(expression, model)
        return result

    elif statement.connective[0].lower() == 'or':
        result = False
        for expression in statement.subexpressions:
            result = result or pl_true(expression, model)
        return result

    elif statement.connective[0].lower() == 'xor':
        result = False
        for expression in statement.subexpressions:
            value = pl_true(expression, model)
            result = (not result and value) or (result and not value)
        return result

def extend(model, symbol, value):
    model[symbol] = value
    return model

def tt_check_all(knowledge_base, statement, symbols, model):
    if len(symbols) == 0:
        if pl_true(knowledge_base, model):
            print("True")
            return pl_true(statement, model)
        else:
            return True

    P = symbols.pop(0)
    return tt_check_all(knowledge_base, statement, symbols, extend(model, P, True)) and tt_check_all(knowledge_base, statement, symbols, extend(model, P, False))

def tt_entails(knowledge_base, statement):
    symbols           = all_symbols(knowledge_base)
    statement_symbols = all_symbols(statement)
    model             = current_model(knowledge_base)

    symbols = symbols + list(set(statement_symbols) - set(symbols))
    
    for symbol in model:
        if symbol in symbols:
            symbols.remove(symbol)

    return tt_check_all(knowledge_base, statement, symbols, model)

def check_true_false(knowledge_base, statement):
    check_statement = tt_entails(knowledge_base, statement)

    negation = logical_expression()
    negation.connective[0] = 'not'
    negation.subexpressions.append(statement)
    check_negation = tt_entails(knowledge_base, negation)

    file = open("result.txt", "w")
    if check_statement and not check_negation:
        file.write('definitely true.')
    elif (not check_statement) and check_negation:
        file.write('definitely false.')
    elif not (check_statement and check_negation):
        file.write('possibly true, possibly false.')
    elif check_statement and check_negation:
        file.write('both true and false.')
    file.close()