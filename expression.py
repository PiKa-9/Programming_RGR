# calculating expression
import re
import math

def calculate(string : str, x : float):
    """
    Calculates the value of str in the point x
    """
    string = remove_first_and_last_parentheses(string)
    
    if string == 'e':
        return math.e
    
    if is_float(string):
        return float(string)

    if string == 'x':
        return x
    
    if string[:2] == 'ln':
        return math.log(calculate(string[2:], x))

    if string[:3] == 'sin':
        return math.sin(calculate(string[3:], x))

    if string[:3] == 'cos':
        return math.cos(calculate(string[3:], x))

    if string[:3] == 'tan':
        return math.tan(calculate(string[3:], x))

    if string[:4] == 'sqrt':
        return math.sqrt(calculate(string[4:], x))

    if string[:3] == 'abs':
        return abs(calculate(string[3:], x))



    split_str = split_by_simple_operations(string)
    
    if len(split_str) == 1:
        # In this case we have this type of expression: expression^exponent
        string = split_str[0]
        string, exponent = split_exponent(string)
        return calculate(string, x) ** calculate(exponent, x)
    else:
        # get rid of * and /
        i = 0
        result = []

        while i < len(split_str):
            j = i
            while (j < len(split_str)) and ((split_str[j] == '*') or (split_str[j] == '/')):
                # we have got: result[-1] - number; split_str[j], split_str[j+2] - operations
                if (split_str[j] == '*'):
                    result[-1] = result[-1] * calculate(split_str[j+1], x)
                if (split_str[j] == '/'):
                    result[-1] = result[-1] / calculate(split_str[j+1], x)
                j += 2
            
            if j >= len(split_str):
                break
            elif split_str[j] not in ['+', '-', '*', '/']:
                # split_str[j] - expression
                result.append(calculate(split_str[j], x))
            else:
                # split_str[j] - operation + or -
                result.append(split_str[j])

            i = j + 1


        # now get rid of + and -
        end_result = result[0]  #result[0] always is a number
        for i in range(2, len(result), 2):
            # result[i] - number; result[i-1] - operation + or -
            if result[i-1] == '-':
                end_result = end_result - result[i]
            if result[i-1] == '+':
                end_result = end_result + result[i]

        return end_result






def split_by_simple_operations(string : str):
    """
    Splits the expression by simple operations like +, -, *, /.
    It doesn't split by operations, which are in some parentheses.
    Returns a list of strings.
    Examples:
    split_by_simple_operations('x+2*x-x^2') = ['x', '+', '2', '*', 'x', '-', 'x^2']
    split_by_simple_operations('x*(x^2-56)-12') = ['x', '*', '(x^2-56)', '-', '12']
    """
    i = 0
    # Counts the "sum" of parentheses, '(' - adds 1, ')' - minus 1: 
    parentheses_count = 0
    
    result = []

    cur_str = "" # string, which we are going to add to result, when we find the operation character

    while i < len(string):
        checker = False # Checks if we need to make cur_str = ""

        # we split by operation only if parentheses_count = 0:
        if parentheses_count == 0:

            if string[i] in ['+', '-', '*', '/']:
                if cur_str == '':
                    result.append('0')
                else:
                    result.append(cur_str)

                result.append(string[i])
                checker = True
            
        
        cur_str = cur_str + string[i]
        # Make cur_str = "" only if currently we have splitted: 
        if checker:
            cur_str = ""

        # Update the parentheses count:
        if string[i] == '(':
            parentheses_count += 1
        if string[i] == ')':
            parentheses_count -= 1

        # Update i:
        i += 1


    if len(cur_str) > 0:
        if cur_str == '':
            result.append('0')
        else:
            result.append(cur_str)


    return result



def remove_first_and_last_parentheses(string : str):
    """
    Removes first and last elements of string until they aren't '(' and ')'
    """
    while (string[0] == '(') and (string[-1] == ')'):
        string = string[1:-1]

    return string



def remove_spaces(string : str):
    """
    Removes all spaces from string
    """
    # Finds all characters, which ARE NOT whitespaces:
    string = re.findall(r'[^\s]', string)
 
    string = ''.join(string)

    return string



def is_float(string : str):
        """
        Checks if string could be converted to float
        """
        try:
            string = float(string)
        except:
            return False
        else:
            return True


def split_exponent(string : str):
    """
    Splits the expression expression_1^expression_2 by '^'
    """
    exponent_ind = len(string)

    for i in range(len(string) - 1, 0, -1):
        if string[i] == '^':
            exponent_ind = i
            break
    
    expression_1 = string[ :exponent_ind]
    expression_2 = string[exponent_ind+1: ]
    
    return expression_1, expression_2

