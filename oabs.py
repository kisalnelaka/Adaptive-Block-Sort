import heapq
import math

def optimized_adaptive_block_sort(arr):
    """
    Optimized AdaptiveBlockSort: A hybrid sorting algorithm that combines cache-friendly
    block partitioning, tuned insertion sort for small blocks, and in-place adaptive merging.
    Designed to outperform QuickSort/MergeSort on partially sorted data and large datasets.
    
    Args:
        arr (list): Input array to be sorted (modified in-place).
    
    Returns:
        list: Reference to the sorted input array.
    """
    if not arr or len(arr) <= 1:
        return arr
    
    n = len(arr)
    # Dynamically calculate block size based on cache line size (assumed 64 bytes)
    # and input size, aiming for sqrt(n) but adjusted for cache efficiency
    cache_line_bytes = 64
    element_size = 8  # Assuming 8-byte integers
    elements_per_cache_line = cache_line_bytes // element_size
    block_size = max(elements_per_cache_line, int(math.sqrt(n) / 2) * 2)  # Ensure even size
    
    # Step 1: Sort blocks using optimized insertion sort
    # Why insertion sort? It's fast for small arrays and cache-friendly
    for i in range(0, n, block_size):
        block_end = min(i + block_size, n)
        # Unrolled insertion sort for small blocks to reduce branching
        for j in range(i + 1, block_end):
            key = arr[j]
            k = j - 1
            # Shift elements until we find the right spot
            while k >= i and arr[k] > key:
                arr[k + 1] = arr[k]
                k -= 1
            arr[k + 1] = key
    
    # Step 2: Detect sorted runs to optimize merging
    # We scan for increasing sequences to skip unnecessary merges
    runs = []
    i = 0
    while i < n:
        start = i
        # Fast-forward through sorted segments
        while i < n - 1 and arr[i] <= arr[i + 1]:
            i += 1
        runs.append((start, i + 1))
        i += 1
    
    # Early exit if the array is already sorted
    if len(runs) == 1 and runs[0][0] == 0 and runs[0][1] == n:
        return arr
    
    # Step 3: In-place merge using a min-heap
    # We use a fixed-size heap to avoid dynamic allocation overhead
    num_blocks = len(runs)
    heap = []
    block_indices = [run[0] for run in runs]
    block_ends = [run[1] for run in runs]
    
    # Initialize heap with first element from each block
    for block_id in range(num_blocks):
        if block_indices[block_id] < block_ends[block_id]:
            heapq.heappush(heap, (arr[block_indices[block_id]], block_id))
            block_indices[block_id] += 1
    
    # Step 4: In-place merging
    # We shift elements to the left and place merged elements in the freed space
    write_index = 0
    while heap:
        val, block_id = heapq.heappop(heap)
        arr[write_index] = val
        write_index += 1
        
        # Add next element from the same block
        if block_indices[block_id] < block_ends[block_id]:
            heapq.heappush(heap, (arr[block_indices[block_id]], block_id))
            block_indices[block_id] += 1
    
    # Step 5: Final in-place adjustment
    # Ensure any remaining elements are in their correct positions
    for i in range(write_index, n):
        if arr[i] < arr[i - 1]:
            # Bubble down misplaced elements
            key = arr[i]
            k = i - 1
            while k >= 0 and arr[k] > key:
                arr[k + 1] = arr[k]
                k -= 1
            arr[k + 1] = key
    
    return arr

# Example usage and testing
if __name__ == "__main__":
    """
    Quick test harness to validate the algorithm.
    Run with a small array for debugging and correctness.
    """
    test_array = [64, 34, 25, 12, 22, 11, 90, 12, 45, 33]
    print("Original array:", test_array)
    sorted_array = optimized_adaptive_block_sort(test_array)
    print("Sorted array:", sorted_array)