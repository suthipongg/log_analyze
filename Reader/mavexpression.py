def evaluate_expression(expression, vars, nocondition=False):
    '''evaluation an expression'''
    # first check for conditions which take the form EXPRESSION{CONDITION}
    if expression[-1] == '}':
        startidx = expression.rfind('{')
        if startidx == -1:
            return None
        condition=expression[startidx+1:-1]
        expression=expression[:startidx]
        try:
            v = eval(condition, globals(), vars)
        except Exception:
            return None
        if not nocondition and not v:
            return None
    try:
        v = eval(expression, globals(), vars)
    except NameError:
        return None
    except ZeroDivisionError:
        return None
    except IndexError:
        return None
    return v