import heapq
import math

def adaptive_block_sort(arr):
    if not arr or len(arr) <= 1:
        return arr
    
    n = len(arr)
    # Determine optimal block size based on input size (tuned for cache)
    block_size = max(32, int(math.sqrt(n)))
    
    # Step 1: Divide into blocks and sort each block with insertion sort
    for i in range(0, n, block_size):
        # Sort block [i, i+block_size) using insertion sort
        for j in range(i + 1, min(i + block_size, n)):
            key = arr[j]
            k = j - 1
            while k >= i and arr[k] > key:
                arr[k + 1] = arr[k]
                k -= 1
            arr[k + 1] = key
    
    # Step 2: Detect runs to optimize merging
    runs = []
    i = 0
    while i < n:
        start = i
        while i < n - 1 and arr[i] <= arr[i + 1]:
            i += 1
        runs.append((start, i + 1))
        i += 1
    
    # If the entire array is sorted, we're done
    if len(runs) == 1 and runs[0][0] == 0 and runs[0][1] == n:
        return arr
    
    # Step 3: Merge blocks using a min-heap
    result = []
    heap = []
    block_indices = [run[0] for run in runs]
    block_ends = [run[1] for run in runs]
    num_blocks = len(runs)
    
    # Initialize heap with first element from each block
    for block_id in range(num_blocks):
        if block_indices[block_id] < block_ends[block_id]:
            heapq.heappush(heap, (arr[block_indices[block_id]], block_id))
            block_indices[block_id] += 1
    
    # Merge blocks
    while heap:
        val, block_id = heapq.heappop(heap)
        result.append(val)
        
        # Add next element from the same block
        if block_indices[block_id] < block_ends[block_id]:
            heapq.heappush(heap, (arr[block_indices[block_id]], block_id))
            block_indices[block_id] += 1
    
    # Copy result back to original array
    for i in range(n):
        arr[i] = result[i]
    
    return arr

# Example usage
if __name__ == "__main__":
    # Test the algorithm
    test_array = [64, 34, 25, 12, 22, 11, 90, 12, 45, 33]
    print("Original array:", test_array)
    sorted_array = adaptive_block_sort(test_array)
    print("Sorted array:", sorted_array)