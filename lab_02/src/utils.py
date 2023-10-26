import numpy as np
import scipy.integrate as sp 


def normalize(probs):
    s = sum(probs)
    
    for i in range(len(probs)):
        probs[i] /= s


def derivative(y, t, coefficient_matrix):
    result = list()
    
    for i in range(len(y)):
        result.append(0)
        for p, intensity in zip(y, coefficient_matrix[i]):
            result[i] += p * intensity

    return result


def solve_ode(matrix, initial_conditions, step, steady_states, eps):
    coefficient_matrix = [
        [-sum(matrix[i]) if j == i else matrix[j][i] for j in range(len(matrix))]
        for i in range(len(matrix))]
    t_vector = np.arange(0, 100, step)
    results = sp.odeint(derivative, initial_conditions, t_vector,
                     args=(coefficient_matrix,), atol=1.0e-8, rtol=1.0e-6)
    results = np.transpose(results)
    times = list()

    for i in range(len(results)):
        row = results[i]
        flag = True
        
        for j in range(len(row) - 1, -1, -1):
            if abs(steady_states[i] - row[j]) > eps:
                times.append(t_vector[j])
                flag = False
                break
        if flag:
            times.append(0)

    return times


def solve(matrix, initial_conditions, step, eps):
    normalize(initial_conditions)
    
    dependent_vars = [0 for _ in range(len(matrix) - 1)]
    dependent_vars.append(1)
    
    coefficient_matrix = [
        [-sum(matrix[i]) if j == i else matrix[j][i] for j in range(len(matrix))]
        for i in range(len(matrix) - 1)]
    coefficient_matrix.append([1 for _ in range(len(matrix))])
    
    probabilities = np.linalg.solve(coefficient_matrix, dependent_vars)
    times = solve_ode(matrix, initial_conditions, step, probabilities, eps)

    return probabilities, times
