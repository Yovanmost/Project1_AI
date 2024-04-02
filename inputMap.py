def readInputFile(file_name):
    with open(file_name, 'r') as file:
        # Read N and M
        N, M = map(int, file.readline().split())

        # Read map matrix
        game_map = []
        for _ in range(N):
            row = list(map(int, file.readline().split()))
            game_map.append(row)

        # Read obstacle positions for hider and seeker
        obstacle_positions = []
        while True:
            line = file.readline().strip()
            if not line:
                break
            obstacle_positions.append(tuple(map(int, line.split())))

    return N, M, game_map, obstacle_positions