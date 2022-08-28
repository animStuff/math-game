"""
written by aryan govil
"""
import random as rand

class algebraRandom:
    def generate(self):
        percent = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2] # 60 percent chance of basicEq
        selects = rand.choice(percent)

        equated = None # capturing the function
        if selects == 1:
            equated = self.basicEquation()
            question = 'Solve This Algebric Equation {}'.format(equated[0])
        else:
            equated = self.identEquation()
            question = 'Which identity is {}'.format(equated[0])

        
        new_lst = [question, equated[1], equated[2]]
        return new_lst

    def basicEquation(self):
        # setting vars
        operations = rand.choice(['+', '-', '*', '/'])
        var = rand.choice(['x', 'z', 'a'])
        num1, num2 = rand.randint(0, 25), rand.randint(25, 100)

        # equation creation
        equation = '{} {} {}'.format(
            str(num1) + var, operations, str(num2) + var)
        
        # solving and extra generation
        constant_val = eval(f'{num1}{operations}{num2}')
        wrong_opts = [
            str(constant_val + 2) + var,
            str(constant_val - 1) + var,
            str(constant_val - 3) + var,
            ]
        
        if operations == '*':
            var = f'{var}^2'
        if operations == '/':
            var = ''
        
        if type(constant_val) == float: 
            constant_val = str(constant_val)
            constant_val = constant_val[:constant_val.index('.') + 3]
            for index, each in enumerate(wrong_opts):
                each = str(each)
                each = each[:each.index('.') + 3]
                wrong_opts[index] = each
                
        answer = str(constant_val) + var
        return equation, answer, wrong_opts

    def identEquation(self):
        num1, num2 = str(rand.randint(25, 150)), str(rand.randint(25, 100))
        wrong_opts = ['add', 'sub', '+ -', 'x +', 'x -']
        answer = rand.choice(wrong_opts)
        wrong_opts.remove(answer)
        wrong_opts.pop(rand.randint(0, 3))
    
        if answer == 'add':
            equation = f'{num1}^2 + {num2}^2 + 2({num1} + {num2})'
        
        elif answer == 'sub':
            equation = f'{num1}^2 + {num2}^2 - 2({num1} + {num2})'
        
        elif answer == 'x +':
            equation = f'(x + {num1})(x + {num2})'
        
        elif answer == 'x -':
            equation = f'(x - {num1})(x - {num2})'

        elif answer == '+ -':
            equation = f'({num1} - {num2})({num1} + {num2})'
        
        return equation, answer, wrong_opts 
        