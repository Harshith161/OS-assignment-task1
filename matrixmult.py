import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from concurrent.futures import ThreadPoolExecutor
import queue

SIZE = 100

A = np.random.randint(1, 10, (SIZE, SIZE))
B = np.random.randint(1, 10, (SIZE, SIZE))

result_queue = queue.Queue()


def compute_cell(i, j):
    value = np.dot(A[i, :], B[:, j])
    result_queue.put((i, j, value))


display_C = np.full((SIZE, SIZE), np.nan)

plt.style.use("dark_background")

fig, (axA, axB, axC) = plt.subplots(1, 3, figsize=(18, 6))

axA.imshow(A, cmap="Blues")
axB.imshow(B, cmap="Greens")

imgC = axC.imshow(
    display_C,
    cmap="inferno",
    vmin=0,
    vmax=6000
)

axA.set_title("Matrix A (100×100)")
axB.set_title("Matrix B (100×100)")
axC.set_title("Matrix C Building Live")

for ax in [axA, axB, axC]:
    ax.set_xticks([])
    ax.set_yticks([])

row_rect = plt.Rectangle(
    (-0.5, -0.5),
    SIZE,
    1,
    fill=False,
    edgecolor="red",
    linewidth=2
)

col_rect = plt.Rectangle(
    (-0.5, -0.5),
    1,
    SIZE,
    fill=False,
    edgecolor="yellow",
    linewidth=2
)

axA.add_patch(row_rect)
axB.add_patch(col_rect)

status = fig.text(
    0.5,
    0.02,
    "",
    ha="center",
    fontsize=11
)

executor = ThreadPoolExecutor(max_workers=16)

for i in range(SIZE):
    for j in range(SIZE):
        executor.submit(compute_cell, i, j)

completed = 0
current_row = 0
current_col = 0


def update(frame):
    global completed, current_row, current_col

    processed = 0

    while not result_queue.empty() and processed < 50:

        i, j, value = result_queue.get()

        display_C[i][j] = value

        current_row = i
        current_col = j

        completed += 1
        processed += 1

    imgC.set_data(display_C)

    row_rect.set_xy((-0.5, current_row - 0.5))
    col_rect.set_xy((current_col - 0.5, -0.5))

    status.set_text(
        f"Completed Cells: {completed}/{SIZE*SIZE}"
    )

    return imgC, row_rect, col_rect, status


anim = FuncAnimation(
    fig,
    update,
    interval=20,
    blit=False
)

plt.tight_layout()
plt.show()