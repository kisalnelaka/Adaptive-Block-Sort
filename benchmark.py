import random
import time
import statistics
import tracemalloc
import pandas as pd
from oabs import optimized_adaptive_block_sort
from tqdm import tqdm  # NEW: for progress tracking

def quicksort(arr):
    """Standard QuickSort implementation for comparison."""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

def mergesort(arr):
    """Standard MergeSort implementation for comparison."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = mergesort(arr[:mid])
    right = mergesort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    """Helper function for MergeSort to merge two sorted arrays."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    return result + left[i:] + right[j:]

def insertion_sort(arr):
    """Standard Insertion Sort implementation for small arrays."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def generate_test_inputs(n, input_type):
    """Generate test arrays of size n with specified complexity."""
    if input_type == "random":
        return [random.randint(0, n) for _ in range(n)]
    elif input_type == "nearly_sorted":
        arr = sorted([random.randint(0, n) for _ in range(n)])
        # Randomly shuffle 10% of the array
        for _ in range(n // 10):
            i, j = random.randint(0, n-1), random.randint(0, n-1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    elif input_type == "reverse_sorted":
        return list(range(n, 0, -1))
    elif input_type == "duplicates":
        return [random.randint(0, 100) for _ in range(n)]  # Limited range for duplicates
    else:
        raise ValueError(f"Unknown input type: {input_type}")

def benchmark_algorithm(alg_func, arr, runs=5, in_place=False):
    """Measure average runtime and peak memory usage for an algorithm."""
    times = []
    peak_memory = []
    
    for _ in range(runs):
        arr_copy = arr.copy()
        tracemalloc.start()
        
        start = time.time()
        if in_place:
            alg_func(arr_copy)
        else:
            arr_copy = alg_func(arr_copy)
        times.append(time.time() - start)
        
        current, peak = tracemalloc.get_traced_memory()
        peak_memory.append(peak / 1024 / 1024)  # Convert to MB
        tracemalloc.stop()
    
    return statistics.mean(times), statistics.mean(peak_memory)

def verify_sorted(arr):
    """Verify if an array is sorted."""
    return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))

def run_benchmarks(sizes, input_types, runs=5):
    """
    Run benchmarks for all algorithms across specified sizes and input types.
    Outputs results in a tabular format.
    """
    algorithms = [
        ("OptimizedAdaptiveBlockSort", optimized_adaptive_block_sort, True),
        ("TimSort", lambda x: sorted(x), False),
        ("QuickSort", quicksort, False),
        ("MergeSort", mergesort, False),
        ("InsertionSort", insertion_sort, True)
    ]
    
    results = []
    total_tasks = len(sizes) * len(input_types) * len(algorithms)

    with tqdm(total=total_tasks, desc="Benchmark Progress", unit="task") as pbar:
        for size in sizes:
            for input_type in input_types:
                print(f"\nTesting size: {size}, Input type: {input_type}")
                arr = generate_test_inputs(size, input_type)
                
                for alg_name, alg_func, in_place in algorithms:
                    try:
                        avg_time, avg_memory = benchmark_algorithm(alg_func, arr, runs, in_place)
                        # Verify correctness
                        arr_copy = arr.copy()
                        if in_place:
                            alg_func(arr_copy)
                        else:
                            arr_copy = alg_func(arr_copy)
                        is_correct = verify_sorted(arr_copy)
                        
                        results.append({
                            "Size": size,
                            "Input Type": input_type,
                            "Algorithm": alg_name,
                            "Avg Time (s)": avg_time,
                            "Avg Memory (MB)": avg_memory,
                            "Correct": "Yes" if is_correct else "No"
                        })
                        print(f"{alg_name}: {avg_time:.6f} s, {avg_memory:.2f} MB, Correct: {is_correct}")
                    except Exception as e:
                        print(f"{alg_name}: Failed with error: {str(e)}")
                    finally:
                        pbar.update(1)  # update progress bar
    
    # Convert results to DataFrame for tabular output
    df = pd.DataFrame(results)
    print("\nBenchmark Results Summary:")
    print(df.to_string(index=False))
    
    # Save results to CSV for further analysis
    df.to_csv("sorting_benchmark_results.csv", index=False)
    print("\nResults saved to sorting_benchmark_results.csv")

def main():
    """Main function to configure and run benchmarks."""
    sizes = [1000000] 
    input_types = ["random", "nearly_sorted", "reverse_sorted", "duplicates"]
    runs = 5  # Number of runs per test for statistical reliability
    
    run_benchmarks(sizes, input_types, runs)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBenchmarking interrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
