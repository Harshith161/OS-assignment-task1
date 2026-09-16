import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Matrix size
SIZE = 100


class CompletedCells:
    """
    Stores the order in which cells are completed.
    """

    def __init__(self):
        self.completed = []
        self.lock = threading.Lock()

    def add_cell(self, row, col):
        # Lock prevents multiple threads from updating the list together
        with self.lock:
            self.completed.append((row, col))


def generate_matrix():
    """
    Create a random matrix with values from 1 to 19.
    """
    return tf.random.uniform(
        shape=(SIZE, SIZE),
        minval=1,
        maxval=20,
        dtype=tf.int32
    )


def compute_cell(matrix_a, matrix_b, result_matrix,
                 row_index, column_index, tracker):
    """
    Calculate one cell of Matrix C.
    """

    # Get row from A
    selected_row = matrix_a[row_index, :]

    # Get column from B
    selected_column = matrix_b[:, column_index]

    # Multiply and sum
    cell_value = tf.reduce_sum(
        selected_row * selected_column
    )

    # Save result
    result_matrix[row_index][column_index] = int(
        cell_value.numpy()
    )

    # Record completion order
    tracker.add_cell(row_index, column_index)


def multiply_matrices():
    """
    Perform matrix multiplication using threads.
    """

    print("\nGenerating matrices...\n")

    matrix_a = generate_matrix()
    matrix_b = generate_matrix()

    result_matrix = [
        [0 for _ in range(SIZE)]
        for _ in range(SIZE)
    ]

    tracker = CompletedCells()

    total_threads = os.cpu_count() or 4

    print(f"Using {total_threads} worker threads")

    start_time = time.perf_counter()

    futures = []

    with ThreadPoolExecutor(
        max_workers=total_threads
    ) as executor:

        for row in range(SIZE):
            for col in range(SIZE):

                future = executor.submit(
                    compute_cell,
                    matrix_a,
                    matrix_b,
                    result_matrix,
                    row,
                    col,
                    tracker
                )

                futures.append(future)

        for future in as_completed(futures):
            future.result()

    end_time = time.perf_counter()

    execution_time = (
        end_time - start_time
    ) * 1000

    print("\nMatrix multiplication completed")
    print(
        f"Execution Time: "
        f"{execution_time:.2f} ms"
    )

    print("\nFirst 3 x 3 Result Sample:\n")

    for row in result_matrix[:3]:
        print(row[:3])

    return (
        matrix_a,
        matrix_b,
        result_matrix,
        tracker.completed
    )


def create_animation(
        matrix_a,
        matrix_b,
        result_matrix,
        completed_order):
    """
    Create animation showing Matrix C
    being filled.
    """

    matrix_a = matrix_a.numpy()
    matrix_b = matrix_b.numpy()

    visible_matrix = np.full(
        (SIZE, SIZE),
        np.nan
    )

    fig, axes = plt.subplots(
        1,
        3,
        figsize=(15, 5)
    )

    ax_a = axes[0]
    ax_b = axes[1]
    ax_c = axes[2]

    ax_a.imshow(
        matrix_a,
        cmap="Blues",
        vmin=1,
        vmax=20
    )

    ax_b.imshow(
        matrix_b,
        cmap="Greens",
        vmin=1,
        vmax=20
    )

    result_display = ax_c.imshow(
        visible_matrix,
        cmap="Oranges"
    )

    ax_a.set_title("Matrix A")
    ax_b.set_title("Matrix B")
    ax_c.set_title("Matrix C")

    for axis in axes:
        axis.set_xticks([])
        axis.set_yticks([])

    # Highlight current row in A
    row_marker = plt.Rectangle(
        (-0.5, -0.5),
        SIZE,
        1,
        fill=False,
        edgecolor="red",
        linewidth=2
    )

    # Highlight current column in B
    column_marker = plt.Rectangle(
        (-0.5, -0.5),
        1,
        SIZE,
        fill=False,
        edgecolor="red",
        linewidth=2
    )

    ax_a.add_patch(row_marker)
    ax_b.add_patch(column_marker)

    progress_text = fig.text(
        0.5,
        0.02,
        "",
        ha="center",
        fontsize=11
    )

    cells_per_frame = 25

    total_frames = (
        len(completed_order)
        + cells_per_frame - 1
    ) // cells_per_frame

    def update(frame):

        start = frame * cells_per_frame

        end = min(
            start + cells_per_frame,
            len(completed_order)
        )

        current_row = 0
        current_col = 0

        for index in range(start, end):

            row, col = completed_order[index]

            visible_matrix[row][col] = (
                result_matrix[row][col]
            )

            current_row = row
            current_col = col

        result_display.set_data(
            visible_matrix
        )

        row_marker.set_y(
            current_row - 0.5
        )

        column_marker.set_x(
            current_col - 0.5
        )

        progress_text.set_text(
            f"Completed: {end}/"
            f"{len(completed_order)}"
            f" | Current Cell: "
            f"C[{current_row}]"
            f"[{current_col}]"
        )

        return (
            result_display,
            row_marker,
            column_marker,
            progress_text
        )

    animation = FuncAnimation(
        fig,
        update,
        frames=total_frames,
        interval=50,
        repeat=False
    )

    plt.tight_layout()
    plt.show()

    return animation


if __name__ == "__main__":

    matrix_a, matrix_b, result_matrix, completion_order = (
        multiply_matrices()
    )

    animation = create_animation(
        matrix_a,
        matrix_b,
        result_matrix,
        completion_order
    )

    print("\nSaving GIF...")

    animation.save(
        "matrix_multiplication.gif",
        writer="pillow",
        fps=10
    )

    print(
        "\nGIF saved successfully as "
        "'matrix_multiplication.gif'"
    )