# Operating Systems Tasks

This repository contains implementations of Operating System concepts using Java and Python.

## 📌 Programs Included

### 1. Producer-Consumer Problem (Java)

A classic synchronization problem implemented using threads, `wait()`, and `notify()` methods.

#### Features

* Producer thread generates data.
* Consumer thread consumes data.
* Synchronization using monitor locks.
* Demonstrates Inter-Process Communication (IPC) concepts.

#### Concepts Used

* Multithreading
* Synchronization
* wait()
* notify()
* Producer-Consumer Problem

---

### 2. Matrix Multiplication Using Multithreading (Python)

A multithreaded matrix multiplication implementation where each matrix cell is computed in parallel using a thread pool.

#### Features

* Generates two random 100 × 100 matrices.
* Computes Matrix C using multiple worker threads.
* Records the completion order of each cell.
* Creates an animation showing Matrix C being built dynamically.
* Saves the visualization as a GIF.

#### Technologies Used

* Python
* TensorFlow
* NumPy
* Matplotlib
* Concurrent Futures (ThreadPoolExecutor)

#### Concepts Used

* Multithreading
* Parallel Processing
* Thread Pool
* Matrix Operations
* Visualization and Animation

---

## 📂 Repository Structure

```text
├── ProducerConsumer.java
├── MatrixMultiplicationAnimation.py
├── matrix_multiplication.gif
└── README.md
```

## 🚀 How to Run

### Java Program

```bash
javac ProducerConsumer.java
java ProducerConsumer
```

### Python Program

Install required libraries:

```bash
pip install tensorflow numpy matplotlib pillow
```

Run:

```bash
python MatrixMultiplicationAnimation.py
```

The generated animation will be saved as:

```text
matrix_multiplication.gif
```

---

## 🎯 Learning Objectives

* Understand thread creation and management.
* Learn synchronization mechanisms.
* Explore parallel computation techniques.
* Visualize multithreaded execution.
* Apply Operating System concepts in practical programs.

## 👨‍💻 Author

Harshith

Information Science Engineering
Operating Systems Task Repository
