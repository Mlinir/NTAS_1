import random
from collections import deque

class MoviesData:
    def __init__(self, movie_id, short_title, long_title):
        self.movie_id = int(movie_id)
        self.short_title = short_title.strip()
        self.long_title = long_title.strip()

    def __repr__(self):
        return f"ID: {self.movie_id}, Short: '{self.short_title}', Long: '{self.long_title}'"


class BinaryNode:
    def __init__(self, key):
        self.value = key
        self.left = None
        self.right = None
        self.height = 0

    def update_height(self):
        left_height = self.left.height if self.left else -1
        right_height = self.right.height if self.right else -1
        self.height = 1 + max(left_height, right_height)


class MovieNode(BinaryNode):
    def __init__(self, key, movie_data):
        super().__init__(key)
        self.movie_data = movie_data


class BinaryTree:
    def __init__(self):
        self.root = None
        self.left_rotations = 0
        self.right_rotations = 0

    def add(self, movie_data):
        def insert(node, data):
            if node is None:
                return MovieNode(data.short_title, data)
            if data.short_title < node.value:
                node.left = insert(node.left, data)
            elif data.short_title > node.value:
                node.right = insert(node.right, data)
            node.update_height()
            return self.balance(node)

        self.root = insert(self.root, movie_data)

    def balance(self, node):
        balance_factor = self.get_balance(node)
        if balance_factor > 1:
            if self.get_balance(node.left) < 0:
                node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if balance_factor < -1:
            if self.get_balance(node.right) > 0:
                node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        return node

    def get_balance(self, node):
        left = node.left.height if node.left else -1
        right = node.right.height if node.right else -1
        return left - right

    def rotate_left(self, z):
        self.left_rotations += 1
        y = z.right
        z.right = y.left
        y.left = z
        z.update_height()
        y.update_height()
        return y

    def rotate_right(self, z):
        self.right_rotations += 1
        y = z.left
        z.left = y.right
        y.right = z
        z.update_height()
        y.update_height()
        return y

    def height(self):
        return self.root.height if self.root else -1

    def assertAVLProperty(self):
        def check(node):
            if not node:
                return True
            balance = self.get_balance(node)
            if abs(balance) > 1:
                return False
            return check(node.left) and check(node.right)
        return check(self.root)

    def search(self, pattern):
        results = []

        def dfs(node):
            if not node:
                return
            if pattern.endswith("*"):
                prefix = pattern[:-1]
                if node.value.startswith(prefix):
                    results.append(node.movie_data)
                if prefix <= node.value:
                    dfs(node.left)
                if prefix >= node.value:
                    dfs(node.right)
            else:
                if node.value == pattern:
                    results.append(node.movie_data)
                elif pattern < node.value:
                    dfs(node.left)
                else:
                    dfs(node.right)

        dfs(self.root)
        return results

    def range_search(self, start_pattern, end_pattern):
        results = []

        def dfs(node):
            if not node:
                return
            if start_pattern[:-1] <= node.value <= end_pattern[:-1] + 'z':
                results.append(node.movie_data)
            if start_pattern[:-1] <= node.value:
                dfs(node.left)
            if node.value <= end_pattern[:-1] + 'z':
                dfs(node.right)

        dfs(self.root)
        return results

    def find_min(self):
        node = self.root
        while node and node.left:
            node = node.left
        return node.movie_data if node else None

    def find_max(self):
        node = self.root
        while node and node.right:
            node = node.right
        return node.movie_data if node else None

    def print_rotation_counts(self):
        print(f"Lijeve rotacije: {self.left_rotations}")
        print(f"Desne rotacije: {self.right_rotations}")

    def zigzag_level_order(self, max_levels=3):
        if not self.root:
            return
        result = []
        current_level = deque([self.root])
        left_to_right = True
        level = 0

        while current_level and level < max_levels:
            level_size = len(current_level)
            level_nodes = []

            for _ in range(level_size):
                if left_to_right:
                    node = current_level.popleft()
                    level_nodes.append(node.value)
                    if node.left:
                        current_level.append(node.left)
                    if node.right:
                        current_level.append(node.right)
                else:
                    node = current_level.pop()
                    level_nodes.append(node.value)
                    if node.right:
                        current_level.appendleft(node.right)
                    if node.left:
                        current_level.appendleft(node.left)

            print(" ".join(level_nodes))
            left_to_right = not left_to_right
            level += 1


class UnbalancedTree:
    def __init__(self):
        self.root = None

    def add(self, movie_data):
        def insert(node, data):
            if node is None:
                return MovieNode(data.short_title, data)
            if data.short_title < node.value:
                node.left = insert(node.left, data)
            else:
                node.right = insert(node.right, data)
            return node

        self.root = insert(self.root, movie_data)

    def height(self):
        def compute_height(node):
            if not node:
                return -1
            return 1 + max(compute_height(node.left), compute_height(node.right))
        return compute_height(self.root)


# === Glavni program ===

filmovi_tim07 = []

with open("movie.txt", encoding="windows-1250") as file:
    for i, line in enumerate(file):
        if i >= 6 and (i - 6) % 11 == 0:
            parts = line.strip().split("\t")
            if len(parts) >= 3:
                film = MoviesData(parts[0], parts[1], parts[2])
                filmovi_tim07.append(film)

print(f"TIM07 - Učitano {len(filmovi_tim07)} filmova")

# Stvaranje AVL stabla
stablo = BinaryTree()
for film in filmovi_tim07:
    stablo.add(film)

print(f"Visina AVL stabla: {stablo.height()}")
print(f"AVL svojstvo zadovoljava: {stablo.assertAVLProperty()}")
stablo.print_rotation_counts()

print("\nZig-zag ispis razina:")
stablo.zigzag_level_order()

print("\nMinimalni film:", stablo.find_min())
print("Maksimalni film:", stablo.find_max())

# Pretraživanje primjera
print("\nPretraga za 'Bug*':", stablo.search("Bug*"))
print("Pretraga u rangu 'F*' do 'M*':", stablo.range_search("F*", "M*"))

# Usporedba sa nebalansiranim stablom
random.shuffle(filmovi_tim07)
ubt = UnbalancedTree()
for film in filmovi_tim07:
    ubt.add(film)

print(f"\nVisina običnog BST: {ubt.height()}")

# AVL sa istim podacima
avl_random = BinaryTree()
for film in filmovi_tim07:
    avl_random.add(film)

print(f"Visina AVL stabla za isti niz: {avl_random.height()}")

info = 1
while info:
    print("\n=== IZBORNIK ===")
    print("a) Ispiši visinu dobivenog AVL stabla.")
    print("b) Pretraživanje podataka o filmu (koristi * za nepotpun naslov)")
    print("c) Pretraživanje u rangu od do za sve filmove")
    print("d) Ispiši minimalni i maksimalni film po indeksu")
    print("e) Ispiši broj lijevih i desnih rotacija")
    print("f) Zig-zag ispis prvih 10 razina AVL stabla")
    print("g) Usporedba visine nebalansiranog i AVL stabla")
    print("0) Izlaz")
    
    info = input("Odaberi: ").strip().lower()
    
    match info:
        case "a":
            print(f"Visina AVL stabla je: {stablo.height()}")
        case "b":
            upit = input("Unesite puni ili djelomični naziv filma (npr. Bug*): ")
            rezultat = stablo.search(upit)
            if rezultat:
                print("Pronađeni filmovi:")
                for r in rezultat:
                    print(r)
            else:
                print("Nema rezultata.")
        case "c":
            od = input("Unesite početak ranga (npr. F*): ")
            do = input("Unesite kraj ranga (npr. M*): ")
            rezultati = stablo.range_search(od, do)
            print(f"Filmovi u rangu {od} do {do}:")
            for r in rezultati:
                print(r)
        case "d":
            print("Minimalni film:", stablo.find_min())
            print("Maksimalni film:", stablo.find_max())
        case "e":
            stablo.print_rotation_counts()
        case "f":
            print("Zig-zag ispis prvih 10 razina:")
            stablo.zigzag_level_order()
        case "g":
            # Ponovno koristi isti niz zapisa
            random.shuffle(filmovi_tim07)
            ubt = UnbalancedTree()
            avl = BinaryTree()
            for f in filmovi_tim07:
                ubt.add(f)
                avl.add(f)
            print("Visina običnog BST:", ubt.height())
            print("Visina AVL stabla:", avl.height())
        case "0":
            print("Izlaz iz programa.")
            break
        case _:
            print("Nepoznata opcija, pokušajte ponovno.")
