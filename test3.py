import tkinter as tk
import random
import heapq

# CONSTANT
WALL = 1
HIDER = 2
SEEKER = 3
PATH = 0

RADIUS = 3  # Bán kính tầm nhìn của Seeker

def create_map(n):
    """
    Hàm tạo bản đồ trò chơi trốn tìm

    Tham số:
        n: Kích thước ma trận (n x n)

    Trả về:
        map: Ma trận 2 chiều chứa bản đồ trò chơi
    """
    # Khởi tạo map
    map = [[WALL for _ in range(n)] for _ in range(n)]

    # Tạo đường đi
    for i in range(1, n - 1):
        for j in range(1, n - 1):
            if random.random() < 0.85:
                map[i][j] = PATH

    # Xử lý trường hợp 2 ô WALL liền kề
    for i in range(1, n - 1):
        for j in range(1, n - 1):
            if map[i][j] == WALL and map[i - 1][j - 1] == WALL and map[i][j - 1] == PATH and map[i - 1][j] == PATH:
                # Xóa 2 ô WALL
                map[i][j] = PATH
                map[i - 1][j - 1] = PATH
            if map[i][j] == WALL and map[i + 1][j + 1] == WALL and map[i][j + 1] == PATH and map[i + 1][j + 1] == PATH:
                # Xóa 2 ô WALL
                map[i][j] = PATH
                map[i + 1][j + 1] = PATH
            if map[i][j] == WALL and map[i + 1][j - 1] == WALL and map[i][j - 1] == PATH and map[i + 1][j] == PATH:
                # Xóa 2 ô WALL
                map[i][j] = PATH
                map[i + 1][j - 1] = PATH

    return map

def add_agent(map, n, agent_type):
    """
    Hàm thêm Hider hoặc Seeker vào bản đồ

    Tham số:
        map: Ma trận 2 chiều chứa bản đồ trò chơi
        n: Kích thước ma trận (n x n)
        agent_type: Loại agent, có thể là HIDER hoặc SEEKER
    """
    while True:
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        if map[i][j] == PATH:
            map[i][j] = HIDER if agent_type == 'HIDER' else SEEKER
            break

def heuristic(start, end):
    """
    Hàm tính điểm ước lượng cho đường đi từ start đến end
    (Sử dụng khoảng cách Manhattan)

    Tham số:
        start: Tọa độ điểm bắt đầu
        end: Tọa độ điểm kết thúc

    Trả về:
        distance: Khoảng cách Manhattan giữa start và end
    """
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

def find_path(map, start, end):
    """
    Hàm tìm đường đi ngắn nhất từ start đến end trên bản đồ map
    (Sử dụng thuật toán A*)

    Tham số:
        map: Ma trận 2 chiều chứa bản đồ trò chơi
        start: Tọa độ điểm bắt đầu
        end: Tọa độ điểm kết thúc

    Trả về:
        path: Đường đi từ start đến end, là một danh sách các tọa độ
    """
    # Khởi tạo các biến cần thiết
    open_list = []
    closed_list = set()
    heapq.heappush(open_list, (0, start, []))

    # Bắt đầu tìm kiếm
    while open_list:
        current_cost, current_node, current_path = heapq.heappop(open_list)

        # Nếu đã đến đích, trả về đường đi
        if current_node == end:
            return current_path + [current_node]

        # Thêm nút hiện tại vào danh sách đã đóng
        closed_list.add(current_node)

        # Duyệt qua các ô lân cận
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue  # Bỏ qua ô hiện tại
                new_x, new_y = current_node[0] + dx, current_node[1] + dy

                # Kiểm tra xem ô mới có hợp lệ không
                if 0 <= new_x < len(map) and 0 <= new_y < len(map[0]) and map[new_x][new_y] != WALL:
                    new_node = (new_x, new_y)

                    # Nếu ô mới chưa được xét, thêm vào danh sách mở
                    if new_node not in closed_list:
                        new_cost = current_cost + 1
                        priority = new_cost + heuristic(new_node, end)
                        heapq.heappush(open_list, (priority, new_node, current_path + [current_node]))

    # Không tìm thấy đường đi
    return None

def display_seeker_view(canvas, map, seeker_position):
    """
    Hàm hiển thị tầm nhìn của Seeker trên bản đồ

    Tham số:
        canvas: Đối tượng Canvas để vẽ bản đồ
        map: Ma trận 2 chiều chứa bản đồ trò chơi
        seeker_position: Tọa độ của Seeker
    """
    seeker_x, seeker_y = seeker_position
    for dx in range(-RADIUS, RADIUS + 1):
        for dy in range(-RADIUS, RADIUS + 1):
            new_x, new_y = seeker_x + dx, seeker_y + dy
            if 0 <= new_x < len(map) and 0 <= new_y < len(map[0]):
                if map[new_x][new_y] != WALL:
                    map[new_x][new_y] = 3

def display_hider_view(canvas, map, hider_position):
    """
    Hàm hiển thị tầm nhìn của Hider trên bản đồ

    Tham số:
        canvas: Đối tượng Canvas để vẽ bản đồ
        map: Ma trận 2 chiều chứa bản đồ trò chơi
        hider_position: Tọa độ của Hider
    """
    hider_x, hider_y = hider_position
    for dx in range(-RADIUS, RADIUS + 1):
        for dy in range(-RADIUS, RADIUS + 1):
            new_x, new_y = hider_x + dx, hider_y + dy
            if 0 <= new_x < len(map) and 0 <= new_y < len(map[0]):
                if map[new_x][new_y] != WALL:
                    map[new_x][new_y] = 3

def main():
    map_size = 40  # Kích thước mặc định
    map = create_map(map_size)
    add_agent(map, map_size, 'SEEKER')
    add_agent(map, map_size, 'HIDER')

    root = tk.Tk()
    root.title("Bản đồ trò chơi trốn tìm")

    canvas = tk.Canvas(root, width=map_size * 20, height=map_size * 20)
    canvas.pack()

    def move_agents():
        nonlocal map, map_size, canvas

        def move_seeker_and_hider():
            seeker_position = None
            hider_position = None

            # Tìm vị trí của Seeker và Hider
            for i in range(map_size):
                for j in range(map_size):
                    if map[i][j] == SEEKER:
                        seeker_position = (i, j)
                    elif map[i][j] == HIDER:
                        hider_position = (i, j)

            if seeker_position and hider_position:
                # Xóa tầm nhìn cũ của Seeker và Hider trên bản đồ
                for i in range(map_size):
                    for j in range(map_size):
                        if map[i][j] == 3:
                            map[i][j] = PATH

                # Hiển thị tầm nhìn mới của Seeker và Hider trên bản đồ
                display_seeker_view(canvas, map, seeker_position)
                display_hider_view(canvas, map, hider_position)

                # Tìm đường đi ngắn nhất từ Seeker đến Hider
                seeker_path = find_path(map, seeker_position, hider_position)

                if seeker_path:
                    # Di chuyển Seeker đến ô tiếp theo trong đường đi
                    next_position = seeker_path[1]
                    map[seeker_position[0]][seeker_position[1]] = PATH
                    map[next_position[0]][next_position[1]] = SEEKER

                # Tìm đường đi ngắn nhất từ Hider đến Seeker
                hider_path = find_path(map, hider_position, seeker_position)

                if hider_path:
                    # Di chuyển Hider đến ô tiếp theo trong đường đi
                    next_position = hider_path[1]
                    map[hider_position[0]][hider_position[1]] = PATH
                    map[next_position[0]][next_position[1]] = HIDER

            # Cập nhật hiển thị bản đồ trên canvas
            canvas.delete("all")
            for i in range(map_size):
                for j in range(map_size):
                    color = "black" if map[i][j] == WALL else "white"
                    if map[i][j] == SEEKER:
                        color = "blue"
                    elif map[i][j] == HIDER:
                        color = "green"
                    elif map[i][j] == 3:  # Giá trị để hiển thị tầm nhìn của Seeker và Hider
                        color = "#ADD8E6"  # Màu xanh dương nhạt
                    canvas.create_rectangle(i * 20, j * 20, (i + 1) * 20, (j + 1) * 20, fill=color)

        # Di chuyển Seeker và Hider
        move_seeker_and_hider()

        # Tự động di chuyển lại sau một khoảng thời gian
        root.after(1000, move_agents)

    # Bắt đầu di chuyển Seeker và Hider
    move_agents()

    root.mainloop()

if __name__ == "__main__":
    main()
