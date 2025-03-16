import numpy as np
import random
import time

def solve_cleaning_duty_simulated_annealing(N, L, T):
    temperature = 20.0
    cooling_rate = 0.95
    max_iterations = 500
    probabilities = np.array(T) / L
    
    current_a = np.zeros(N, dtype=int)
    current_b = np.zeros(N, dtype=int)
    
    for i in range(N):
        current_a[i] = np.random.choice(N, p=probabilities)
        while True:
            current_b[i] = np.random.choice(N, p=probabilities)
            if current_b[i] != current_a[i]:  # 無限ループ防止
                break

    current_error, current_errors = evaluate_solution_probabilistic(N, L, current_a, current_b, T)
    best_a, best_b = current_a.copy(), current_b.copy()
    best_error = current_error
    best_errors = current_errors.copy()
    
    start_time = time.time()
    
    for iteration in range(max_iterations):
        if time.time() - start_time > 1.8:
            break
        
        temperature *= cooling_rate
        
        new_a, new_b = current_a.copy(), current_b.copy()
        
        error_indices = np.argsort(current_errors)[::-1]
        num_changes = max(1, N // 10)
        selected_indices = error_indices[:num_changes]

        for i in selected_indices:
            if random.random() < 0.5:
                new_a[i] = np.random.choice(N, p=probabilities)
            else:
                new_b[i] = np.random.choice(N, p=probabilities)
            
            if new_a[i] == new_b[i]:  # 無限ループ防止
                new_b[i] = (new_b[i] + 1) % N

        new_error, new_errors = evaluate_solution_probabilistic(N, L, new_a, new_b, T)
        
        if accept_solution(current_error, new_error, temperature):
            current_a, current_b = new_a.copy(), new_b.copy()
            current_error, current_errors = new_error, new_errors.copy()
            
            if new_error < best_error:
                best_a, best_b = new_a.copy(), new_b.copy()
                best_error, best_errors = new_error, new_errors.copy()
    
    return best_a, best_b, best_error

def evaluate_solution_probabilistic(N, L, a, b, T):
    transition_matrix = np.zeros((N, N))
    
    for i in range(N):
        transition_matrix[i, a[i]] += 0.5
        transition_matrix[i, b[i]] += 0.5

    state_vector = np.zeros(N)
    state_vector[0] = 1.0

    for _ in range(30):
        state_vector = np.dot(state_vector, transition_matrix)
    
    predicted_count = state_vector * L
    errors = predicted_count - T
    total_error = np.sum(np.abs(errors))
    
    return total_error, errors

def accept_solution(current_error, new_error, temperature):
    if new_error < current_error:
        return True
    probability = np.exp((current_error - new_error) / temperature)
    return random.random() < probability

def main():
    N, L = map(int, input().split())
    T = list(map(int, input().split()))
    
    a, b, _ = solve_cleaning_duty_simulated_annealing(N, L, T)
    
    for i in range(N):
        print(f"{a[i]} {b[i]}")

if __name__ == "__main__":
    main()
