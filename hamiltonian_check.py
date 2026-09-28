from dungeon_generator import generate_dungeon

def validate_dungeon(dungeon_map):
    n, _ = dungeon_map[0]
    edges = dungeon_map[1:]
    
    adj = {i: [] for i in range(n)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # we test every room as a potential starting point
    for start in range(n):
        # we use a Depth-First Search (DFS) with backtracking
        waiting_list = [(start, [start], {start})]

        while waiting_list:
            curr, path, visited = waiting_list.pop()

            # if the path reaches length n, every room has been visited exactly once
            if len(path) == n:
                print("Valid dungeon! Hamiltonian Path:", " -> ".join(map(str, path)), "\n")
                return path

            for nxt in adj[curr]:
                if nxt not in visited:
                    waiting_list.append((nxt, path + [nxt], visited | {nxt}))

    print("No valid path exists.\n")
    return None
