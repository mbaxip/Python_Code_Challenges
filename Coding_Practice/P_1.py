def find_balanced_parenthesis(string):
    """
    
    Returns if the input is balanced in parens or not.
    Example:
    
    (()) -> True
    
    (())() True
    
    (())) False
    
    :param string: 
    :return: boolean 
    """
    stack = []
    par = ['(', ')']
    for char in string:
        if char == par[0]:
            stack.append(char)
        elif len(stack) != 0:
            stack.pop()
        else:
            return False
    if len(stack) == 0:
        return True
    else:
        return False

str = '(()))'
print(find_balanced_parenthesis(str))