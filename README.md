# Dungeon Generator & Hamiltonian Path Validator

## 1. Project Overview

This project generates random dungeon maps and checks whether they can be cleared according to the following rule:

> The player must visit every room exactly once without reusing any tunnel.

The dungeon is represented as an **undirected graph**:

- a **room** represents a vertex;
- a **corridor** represents an undirected edge between two rooms;
- a dungeon is considered **valid** if it contains a **Hamiltonian path**, i.e. a path that visits every vertex exactly once.

The project is divided into two main algorithms:

1. a procedural dungeon generator;
2. a Hamiltonian path validator.

---

## 2. Dungeon Representation

A generated dungeon is stored as a Python list.

The first element is a header containing:

```text
(number_of_rooms, number_of_corridors)
```

The remaining elements are the corridors:

```text
(room_1, room_2)
```

Example:

```python
[
    (6, 7),
    (0, 1),
    (0, 4),
    (1, 2),
    (1, 5),
    (2, 3),
    (3, 4),
    (4, 5)
]
```

This represents a dungeon with **6 rooms** and **7 corridors**.

Rooms are numbered from `0` to `N - 1`.

Because the graph is undirected, `(0, 3)` and `(3, 0)` represent the same corridor.  
To avoid duplicates, every edge is stored as a sorted tuple.

---

# 3. Algorithm 1 — Procedural Dungeon Generator

## 3.1 Purpose

The first algorithm procedurally generates a random dungeon.

It does **not** directly construct a Hamiltonian path. Instead, it creates a random graph that is later checked by the validation algorithm.

This separation allows the program to generate both:

- valid dungeons containing a Hamiltonian path;
- invalid dungeons containing no Hamiltonian path.

---

## 3.2 Number of Rooms

The number of rooms is randomly selected between 6 and 10:

```python
number_rooms = randint(6, 10)
```

The rooms are then numbered:

```text
0, 1, 2, ..., N - 1
```

---

## 3.3 Number of Corridors

The initial number of corridors is generated using:

```python
number_corridors = number_rooms + randint(0, 8) - 1
```

Therefore, the initial number of corridors is between:

```text
N - 1
```

and:

```text
N + 7
```

This creates dungeons with different graph densities.

Additional corridors may later be added when too many rooms have fewer than two neighbors.

> **Implementation note:** because extra corridors can be added after the initial generation, the final header should be updated before returning the dungeon:
>
> ```python
> dungeon_map[0] = (number_rooms, len(dungeon_map) - 1)
> ```

---

## 3.4 Corridor Generation

The function:

```python
creating_corridors(u, rooms)
```

randomly selects a second room `v`.

The algorithm guarantees:

```text
u != v
```

so a room cannot connect to itself.

Since the graph is undirected, the edge is normalized with:

```python
tuple(sorted((u, v)))
```

For example:

```text
(5, 2)
```

becomes:

```text
(2, 5)
```

---

## 3.5 Avoiding Duplicate Corridors

The generator uses a Python `set` called:

```python
existing_edges
```

to store every corridor that has already been created.

Before accepting a new corridor, the program checks:

```python
while edge in existing_edges:
```

and generates another edge if necessary.

Using a set makes duplicate checking efficient, with average-case membership testing in `O(1)` time.

---

## 3.6 Tracking Room Degrees

The list:

```python
Number_neighbours
```

stores the number of corridors connected to each room.

For example:

```python
Number_neighbours[3]
```

represents the degree of room `3`.

Whenever a corridor `(u, v)` is added, both degrees are updated:

```python
Number_neighbours[u] += 1
Number_neighbours[v] += 1
```

---

## 3.7 Handling Rooms With Too Few Neighbors

After the initial graph is generated, the algorithm searches for rooms having fewer than two neighbors.

These rooms are stored in:

```python
isolated_rooms
```

For a graph to contain a Hamiltonian path, vertices of degree `0` cannot participate, and vertices of degree `1` can only appear as endpoints of the path. Therefore, a Hamiltonian path can have at most two vertices with degree lower than `2`.

When more than two such rooms exist, the generator creates additional random corridors for them.

This process is repeated until at most two rooms have fewer than two neighbors.

This does **not guarantee** that a Hamiltonian path exists. It only removes some obvious structural obstacles and increases the chance of producing an interesting dungeon.

The second algorithm is still required to determine whether the dungeon is actually valid.

---

## 3.8 Generator Pseudocode

```text
Generate a random number N of rooms between 6 and 10

Generate an initial number M of corridors

Create rooms 0 ... N-1

Initialize:
    degree of every room = 0
    set of existing edges = empty

Repeat M times:
    choose two different random rooms u and v

    while edge (u, v) already exists:
        choose another pair

    add corridor (u, v)
    increase degree[u]
    increase degree[v]

Find rooms with degree < 2

while more than two such rooms exist:

    for each room with degree < 2:
        create a new random corridor
        avoid duplicate corridors
        update degrees

Update the final value of M
Return the generated dungeon
```

---

# 4. Algorithm 2 — Hamiltonian Path Validator

## 4.1 Purpose

The second algorithm checks whether the generated dungeon contains a **Hamiltonian path**.

A Hamiltonian path visits every vertex exactly once.

The starting and ending rooms are **not imposed** by the problem. Therefore, the validator tries every room as a possible starting point.

---

## 4.2 Building an Adjacency List

The generator produces an edge list.

For traversal, the validator converts it into an adjacency list.

For every corridor:

```text
(u, v)
```

the algorithm adds:

```text
v to the adjacency list of u
u to the adjacency list of v
```

Example:

```text
0 -- 1
0 -- 3
1 -- 2
```

becomes:

```python
{
    0: [1, 3],
    1: [0, 2],
    2: [1],
    3: [0]
}
```

---

## 4.3 Trying Every Starting Room

Unlike a Hamiltonian cycle, a Hamiltonian path cannot necessarily start from any vertex.

For example:

```text
0 -- 1 -- 2 -- 3
```

contains the Hamiltonian path:

```text
0 -> 1 -> 2 -> 3
```

but starting from room `1` does not allow all rooms to be visited exactly once.

For that reason, the validator tries each room as a possible starting point:

```python
for start in range(n):
```

---

## 4.4 Iterative Depth-First Search

For every starting room, the program performs an **iterative Depth-First Search (DFS)**.

The stack is stored in:

```python
waiting_list
```

Each state contains:

```python
(current_room, current_path, visited_rooms)
```

Example:

```python
(3, [0, 2, 3], {0, 2, 3})
```

means that:

- the algorithm is currently in room `3`;
- the current candidate path is `0 -> 2 -> 3`;
- rooms `0`, `2`, and `3` have already been used in this candidate path.

---

## 4.5 Backtracking

For each neighbor of the current room, the algorithm checks whether the neighbor has already been visited.

If not, it creates a new search state:

```python
(nxt, path + [nxt], visited | {nxt})
```

Each branch therefore receives its own:

- candidate path;
- set of visited rooms.

If one branch reaches a dead end, another previously stored state can still be explored.

This implements the principle of **backtracking through an iterative DFS**.

For example, the algorithm may first explore:

```text
0 -> 1 -> 4
```

and discover that it cannot continue.

It can then explore another candidate such as:

```text
0 -> 1 -> 3
```

without losing the previous search state.

---

## 4.6 Detecting a Hamiltonian Path

Each time a state is removed from the stack, the algorithm checks:

```python
if len(path) == n:
```

If this is true, every room has been visited exactly once.

The dungeon is therefore valid, and the program prints:

```text
Valid dungeon! Hamiltonian Path: ...
```

Example:

```text
Valid dungeon! Hamiltonian Path: 2 -> 4 -> 0 -> 3 -> 1 -> 5
```

The current implementation stops as soon as the **first** Hamiltonian path is found.

---

## 4.7 Detecting an Invalid Dungeon

If all possible paths from all possible starting rooms have been explored without finding a path of length `N`, then no Hamiltonian path exists.

The program prints:

```text
No valid path exists.
```

and returns:

```python
None
```

---

## 4.8 Validator Pseudocode

```text
Create an adjacency list from the dungeon corridors

for each room START:

    create a stack containing:
        START
        path = [START]
        visited = {START}

    while stack is not empty:

        remove the latest state from the stack

        if number of vertices in path == N:
            return the Hamiltonian path

        for every neighbor of the current room:

            if neighbor has not been visited:

                create a new path containing neighbor
                create a new visited set containing neighbor

                add this new state to the stack

return "No valid path exists"
```

---

# 5. Why DFS and Backtracking Are Required

A standard DFS can determine whether vertices are reachable, but reachability alone is not sufficient for Hamiltonicity.

A connected graph does not necessarily contain a Hamiltonian path.

The validator must therefore explore different possible orders in which rooms can be visited.

The search continues along one candidate path as deeply as possible. If that candidate cannot be completed without revisiting a room, the algorithm explores another previously stored possibility.

---

# 6. Valid Dungeon Example

Consider the following dungeon:

```text
0 -- 1 -- 2 -- 3 -- 4 -- 5
```

Its edge-list representation is:

```python
[
    (6, 5),
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5)
]
```

A Hamiltonian path exists:

```text
0 -> 1 -> 2 -> 3 -> 4 -> 5
```

Every room is visited exactly once.

Therefore, the dungeon is valid.

---

# 7. Invalid Dungeon Example

Consider the following dungeon:

```text
        1
        |
2 ----- 0 ----- 3
        |
        4
```

Its edge-list representation is:

```python
[
    (5, 4),
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4)
]
```

Any path through the central room `0` can connect at most two of the four outer rooms.

Visiting another outer room would require returning to room `0`, which would mean visiting the same room more than once.

Therefore, no Hamiltonian path exists.

The validator returns:

```text
No valid path exists.
```

---

# 8. Complexity

## 8.1 Dungeon Generator

The generator creates random corridors and checks duplicates using a set.

Average set membership checking is:

```text
O(1)
```

The exact running time depends on the randomly generated graph because a duplicate edge may require another random attempt.

For the small graphs used in this project, this cost remains limited.

---

## 8.2 Hamiltonian Path Validator

Finding a Hamiltonian path is computationally expensive because, in the worst case, many possible vertex orders must be explored.

The worst-case time complexity is approximately:

```text
O(N!)
```

This is acceptable for this project because generated dungeons contain only:

```text
6 to 10 rooms
```

The algorithm also stops immediately when the first Hamiltonian path is found.

---

# 9. Project Structure

```text
project/
│
├── dungeon_generator.py
├── hamiltonian_check.py
├── main.py
└── README.md
```

### `dungeon_generator.py`

Contains the procedural dungeon generation algorithm.

### `hamiltonian_check.py`

Contains the Hamiltonian path validation algorithm.

### `main.py`

Generates a dungeon and immediately validates it:

```python
from dungeon_generator import generate_dungeon
from hamiltonian_check import validate_dungeon

validate_dungeon(generate_dungeon())
```

---

# 10. How to Run

Make sure Python is installed.

From the project directory, run:

```bash
python main.py
```

The program first prints the generated dungeon:

```text
Number of nodes and edges: (N, M)
Edges in the dungeon: [...]
```

It then prints either a Hamiltonian path:

```text
Valid dungeon! Hamiltonian Path: ...
```

or:

```text
No valid path exists.
```

---

# 11. AI Usage Disclosure

AI was used to discuss the interpretation of the Hamiltonian path problem and to assist with the wording and organization of this README.
