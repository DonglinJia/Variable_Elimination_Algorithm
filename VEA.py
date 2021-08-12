import numpy as np
import copy

list_a = ['AS', 'AB']
matrix_a = [
    [0, 1, 0.1],
    [1, 1, 0.6],
    [0, 0, 0.9],
    [1, 0, 0.4]
]

list_b = ['AS', 'M', 'NH', 'AH']
matrix_b = [
    [0,0,0,1,0],
    [0,0,1,1,0.2],
    [0,1,0,1,0.4],
    [0,1,1,1,0.65],
    [1,0,0,1,0.5],
    [1,0,1,1,0.75],
    [1,1,0,1,0.9],
    [1,1,1,1,0.99],
    [0,0,0,0,1.0],
    [0,0,1,0,0.8],
    [0,1,0,0,0.6],
    [0,1,1,0,0.35],
    [1,0,0,0,0.5],
    [1,0,1,0,0.25],
    [1,1,0,0,0.1],
    [1,1,1,0,0.01]
]

list_c = ['AS']
matrix_c = [
    [1, 0.05],
    [0, 0.95]
]

list_d = ['M']
matrix_d = [
    [1, 0.0357],
    [0, 0.9643]
]

list_e = ['NA']
matrix_e = [
    [1, 0.3],
    [0, 0.7]
]

list_f = ['M', 'NA', 'NH']
matrix_f = [
    [0,0,1,0],
    [0,1,1,0.5],
    [1,0,1,0.4],
    [1,1,1,0.8],
    [0,0,0,1.0],
    [0,1,0,0.5],
    [1,0,0,0.6],
    [1,1,0,0.2]
]


class Factor:
    # states is parent-states + self-state. -- list of string
    #   Thus the conditional dependence is P(self|parent_state1 and parent_state2 and ... and parent_staten)
    # prob_matrix: -- multi-demension array 
    #   row = 2^ number of parents
    #   col = number of states (parent-states + self)

    # check conditions:
    #   1. if prob_matrix has only one row left, then it represents a number (probability)

    def __init__(self, states, prob_matrix):
        self.states = states
        self.prob_matrix = prob_matrix
        self.name = self.get_name()
    
    def get_name(self):
        if len(self.states) == 0:
            return 'f()'
        else:
            name = 'f('
            for i in range(len(self.states) - 1):
                name += self.states[i] + ', '
            name += self.states[-1] + ')'
            return name

def restrict(factor, variable, value):
    index = factor.states.index(variable)
    states = copy.deepcopy(factor.states)
    states.remove(variable)
    new_prob_matrix = []
    for row in factor.prob_matrix:
        if row[index] == value:
            new_prob_matrix.append(row[:index] + row[index + 1:])
    return Factor(states, new_prob_matrix)

def multiply(fa, fb):
    if len(fa.states) == 0 and len(fb.states) == 0:
        return Factor([],fa.prob_matrix[0][0] * fb.prob_matrix[0][0])
    elif len(fa.states) > 0 and len(fb.states) == 0:
        fc = copy.deepcopy(fa)
        for row in fc.prob_matrix:
            row[-1] = row[-1] * fb.prob_matrix[0][0]
        return fc
    elif len(fa.states) == 0 and len(fb.states) > 0:
        fc = copy.deepcopy(fb)
        for row in fc.prob_matrix:
            row[-1] = row[-1] * fa.prob_matrix[0][0]
        return fc
    else:
        common_state = list(set(fa.states).intersection(fb.states))
        fa_indice = []
        fb_indice = []
        for state in common_state:
            fa_indice.append(fa.states.index(state))
            fb_indice.append(fb.states.index(state))

        fb_rest_indices = [ i for i in range(len(fb.states)) if i not in fb_indice ] 
        new_states = copy.deepcopy(fa.states)
        for index in fb_rest_indices:
            new_states.insert(0, fb.states[index])
        
        new_prob_matrix = []
        # for each common value in factor a
        for row_a in fa.prob_matrix:
            fa_values = []
            for index_a in fa_indice:
                fa_values.append(row_a[index_a])
            # loop through the entire factor b locate the exact same value
            for row_b in fb.prob_matrix:
                fb_values = []
                for index_b in fb_indice:
                    fb_values.append(row_b[index_b])
                # if common values are the same, then we need to 
                if fb_values == fa_values:
                    new_row = copy.deepcopy(row_a)
                    for index in fb_rest_indices:
                        new_row.insert(0, row_b[index])
                    new_row[-1] = row_a[-1] * row_b[-1]
                    new_prob_matrix.append(new_row)

        return Factor(new_states, new_prob_matrix)

def sumout(factor, variable):
    index = factor.states.index(variable)
    new_states = copy.deepcopy(factor.states)
    new_states.remove(variable)
    f_rest_indices = [ i for i in range(len(factor.states)) if i != index ]
    checked_set = list()
    new_matrix = []
    for i in range(len(factor.prob_matrix)):
        tmp_value = []
        for ri in f_rest_indices:
            tmp_value.append(factor.prob_matrix[i][ri])
        for j in range(i + 1, len(factor.prob_matrix)):
            check_value = []
            for rj in f_rest_indices:
                check_value.append(factor.prob_matrix[j][rj])
            if check_value == tmp_value and check_value not in checked_set:
                new_row = copy.deepcopy(factor.prob_matrix[i])
                new_row.pop(index)
                new_row[-1] = factor.prob_matrix[i][-1] + factor.prob_matrix[j][-1]
                new_matrix.append(new_row)
                checked_set.append(check_value)

    return Factor(new_states, new_matrix)

def normalize(factor):
    total_sum = 0
    new_states = copy.deepcopy(factor.states)
    new_matrix = []
    for row in factor.prob_matrix:
        total_sum += row[-1]
    for row in factor.prob_matrix:
        new_row = copy.deepcopy(row)
        new_row[-1] = new_row[-1] / total_sum
        new_matrix.append(new_row)
    return Factor(new_states, new_matrix)

def print_factor(factor_list):
    fn = ''
    for factor in factor_list:
        fn += factor.name + ' '
    return fn

def inference(factor_list, query_variable, ordered_hidden_var_list, evidence_list):
    print('Define factors ' + print_factor(factor_list) + '.')

    # Restrict the factors based on evidence_list
    # f_remove_set = set()
    for k_val in evidence_list:
        key = k_val[0]
        value = k_val[1]
        index = 0
        while index < len(factor_list) - 1:
            factor = factor_list[index]
            if key in factor.states:
                n_f = restrict(factor, key, value)
                factor_list.remove(factor)
                print('Restrict {} to {} = {} to produce factor {}'.format(factor.name, key, value, n_f.name))
                factor_list.append(n_f)
                index -= 1
            index += 1

    # Eliminate hidden variable
    for var in ordered_hidden_var_list:
        multi_factor_list = []
        remove_list = []
        for factor in factor_list:
            if var in factor.states:
                multi_factor_list.append(factor)
                remove_list.append(factor)
        
        for item in remove_list:
            factor_list.remove(item)

        f = multi_factor_list[0]
        if len(multi_factor_list) != 0:
            for mf in range(1, len(multi_factor_list)):
                f = multiply(f, multi_factor_list[mf])
        if len(multi_factor_list) != 1:
            print('Multiply {}to produce {}'.format(print_factor(multi_factor_list), f.name))

        # print(np.array(f.prob_matrix))
        factor_f = sumout(f, var)
        print('Sum out {} from {} to produce {}'.format(var, f.name, factor_f.name))
        # print(np.array(factor_f.prob_matrix))
        factor_list.append(factor_f)
        
    # print(np.array(factor_f.prob_matrix))
    # multiply all remaining factor
    f = factor_list[0]
    if len(factor_list) != 0:
        for mf in range(1, len(factor_list)):
            f = multiply(f, factor_list[mf])
    if len(factor_list) != 1:
        print('Multiply {}to produce {}'.format(print_factor(factor_list), f.name))
    #normalize the factor
    f_final = normalize(f)
    print('Normalize {} to produce {}'.format(f.name, f_final.name))
    return f_final

fa = Factor(list_a, matrix_a)
fb = Factor(list_b, matrix_b)
fc = Factor(list_c, matrix_c)
fd = Factor(list_d, matrix_d)
fe = Factor(list_e, matrix_e)
ff = Factor(list_f, matrix_f)

print('Situation 1')
ra = inference([fa,fb,fc,fd,fe,ff],['AH'], ['AB', 'AS', 'M', 'NA', 'NH'], [])
print(np.array(ra.states))
print(np.array(ra.prob_matrix))
print()

print('Situation 2')
rb = inference([fa,fb,fc,fd,fe,ff],['AS'], ['AB', 'NA', 'NH'], [['AH', 1], ['M', 1]])
print(np.array(rb.states))
print(np.array(rb.prob_matrix))
print()

print('Situation 3')
rc = inference([fa,fb,fc,fd,fe,ff],['AS'], ['NA', 'NH'], [['AH', 1], ['M', 1],['AB', 1]])
print(np.array(rc.states))
print(np.array(rc.prob_matrix))
print()

print('Situation 4')
rd = inference([fa,fb,fc,fd,fe,ff],['AS'], ['NH'], [['AH', 1], ['M', 1],['AB', 1], ['NA', 1]])
print(np.array(rd.states))
print(np.array(rd.prob_matrix))


