from random import randint

# Picks a random neighbor different from room u and formats it as a sorted tuple (undirected edge)
def creating_corridors(u, rooms):
    v = randint(0, len(rooms) - 1)  
    while u == v:
        v = randint(0, len(rooms) - 1)
    edge = tuple(sorted((u, v)))
    return edge, u, v

def generate_dungeon():
    number_rooms = randint(6, 10)
    number_corridors = number_rooms + randint(0, 8) - 1
    number_isolated_rooms = 3

    rooms = []
    
    # dungeon_map: stores the final structure. 
    # The first element is the required header (N, M), followed by the list of edges.
    dungeon_map = [] 
    dungeon_map.append((number_rooms, number_corridors))

    # Number_neighbours: acts as a degree counter to track how many corridors connect to each room.
    Number_neighbours = [0 for i in range(number_rooms)]

    for i in range(number_rooms):
        rooms.append(i)

    # existing_edges: a set storing sorted tuples (u, v) for O(1) duplicate checks on undirected edges.
    existing_edges = set()

    # Build random corridors without duplicates
    for i in range(number_corridors):
        edge, u, v = creating_corridors(randint(0, len(rooms) - 1), rooms)
        
        while edge in existing_edges:
            edge, u, v = creating_corridors(randint(0, len(rooms) - 1), rooms) 
        
        existing_edges.add(edge)
        dungeon_map.append(edge)
        Number_neighbours[u] += 1
        Number_neighbours[v] += 1

    # Fix rooms with fewer than 2 neighbors to support potential Hamiltonian paths
    isolated_rooms = []
    while number_isolated_rooms > 2:
        number_isolated_rooms = 0
        isolated_rooms = [] 

        #Scan all rooms to see which ones are stuck with fewer than 2 neighbors
        for i in range(len(Number_neighbours)):
            if Number_neighbours[i] < 2:
                isolated_rooms.append(i)
                number_isolated_rooms += 1
        # If we find rooms that are too isolated, we force-create new corridors for them        
        if number_isolated_rooms > 1:
            for i in range(len(isolated_rooms)):
                # If we find rooms that are too isolated, we force-create new corridors for them
                edge, u, v = creating_corridors(isolated_rooms[i], rooms) 
                
                while edge in existing_edges:
                    edge, u, v = creating_corridors(isolated_rooms[i], rooms) 
                    
                existing_edges.add(edge)
                dungeon_map.append(edge)
                Number_neighbours[u] += 1
                Number_neighbours[v] += 1

    return dungeon_map

def main():
    generate_dungeon()

if __name__ == "__main__":
    main()