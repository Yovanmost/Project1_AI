import tkinter as tk
import random
import heapq

# CONSTANT
WALL = 1
HIDER = 2
SEEKER = 3
PATH = 0

def tao_map(n):
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

def them_agent(map, n, agent_type):
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

def diem_duong_di(start, end):
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

def tim_duong_di(map, start, end):
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
                        priority = new_cost + diem_duong_di(new_node, end)
                        heapq.heappush(open_list, (priority, new_node, current_path + [current_node]))

    # Không tìm thấy đường đi
    return None

def move_seeker(map, seeker_position, hider_position):
    """
    Hàm di chuyển Seeker

    Tham số:
        map: Ma trận 2 chiều chứa bản đồ trò chơi
        seeker_position: Vị trí hiện tại của Seeker
        hider_position: Vị trí hiện tại của Hider

    Trả về:
        Vị trí mới của Seeker
    """
    # Tìm đường đi ngắn nhất từ Seeker đến Hider
    path = tim_duong_di(map, seeker_position, hider_position)
    if path:
        # Di chuyển Seeker đến ô tiếp theo trong đường đi
        new_position = path[1]
        map[seeker_position[0]][seeker_position[1]] = PATH
        map[new_position[0]][new_position[1]] = SEEKER
        return new_position
    else:
        return seeker_position  # Không tìm thấy đường đi, Seeker giữ nguyên vị trí

def move_hider(map, hider_position, seeker_position):
    """
    Hàm di chuyển Hider

    Tham số:
        map: Ma trận 2 chiều chứa bản đồ trò chơi
        hider_position: Vị trí hiện tại của Hider
        seeker_position: Vị trí hiện tại của Seeker

    Trả về:
        Vị trí mới của Hider
    """
    # Tìm đường đi ngắn nhất từ Hider đến Seeker
    path = tim_duong_di(map, hider_position, seeker_position)
    if path:
        # Di chuyển Hider đến ô tiếp theo trong đường đi
        new_position = path[1]
        map[hider_position[0]][hider_position[1]] = PATH
        map[new_position[0]][new_position[1]] = HIDER
        return new_position
    else:
        return hider_position  # Không tìm thấy đường đi, Hider giữ nguyên vị trí

def main():
    map_size = 40  # Kích thước mặc định
    map = tao_map(map_size)
    them_agent(map, map_size, 'SEEKER')
    them_agent(map, map_size, 'HIDER')

    root = tk.Tk()
    root.title("Bản đồ trò chơi trốn tìm")

    canvas = tk.Canvas(root, width=map_size * 20, height=map_size * 20)
    canvas.pack()

    def move_agents():
        nonlocal map, map_size, canvas

        # Di chuyển Seeker và Hider
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
            # Di chuyển Seeker và Hider
            move_seeker(map, seeker_position, hider_position)
            move_hider(map, hider_position, seeker_position)

            # Cập nhật hiển thị bản đồ trên canvas
            canvas.delete("all")
            for i in range(map_size):
                for j in range(map_size):
                    color = "black" if map[i][j] == WALL else "white"
                    if map[i][j] == SEEKER:
                        color = "blue"
                    elif map[i][j] == HIDER:
                        color = "green"
                    canvas.create_rectangle(i * 20, j * 20, (i + 1) * 20, (j + 1) * 20, fill=color)

        # Tự động di chuyển lại sau một khoảng thời gian
        root.after(1000, move_agents)

    # Bắt đầu di chuyển Seeker và Hider
    move_agents()

    root.mainloop()

if __name__ == "__main__":
    main()
