import sys

# Create one matrix (80 x 120)
matrix = [[{'base': 1} for _ in range(120)] for _ in range(80)]

# Calculate memory usage of the entire matrix
matrix_size = sys.getsizeof(matrix) + sum(sys.getsizeof(row) + sum(sys.getsizeof(cell) for cell in row) for row in matrix)

print(f"Memory usage of one matrix: {matrix_size / 1024:.2f} KB")
total_size = 4 * matrix_size
print(f"Estimated memory usage for 4 matrices: {total_size / 1024:.2f} KB")