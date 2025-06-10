import random
from collections import deque


class MoviesData:
    def __init__(self, movie_id, short_title, long_title):
        self.movie_id = int(movie_id)
        self.short_title = short_title.strip()
        self.long_title = long_title.strip()

    def __repr__(self):
        return (
            f"ID: {self.movie_id}, "
            f"Short: '{self.short_title}', "
            f"Long: '{self.long_title}'"
        )


class BinaryNode:
    def __init__(self, key):
        self.value = key
        self.left = None
        self.right = None
        self.height = 0

    def update_height(self):
        left_h = self.left.height if self.left else -1
        right_h = self.right.height if self.right else -1
        self.height = 1 + max(left_h, right_h)


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
        bf = self.get_balance(node)

        if bf > 1:
            if self.get_balance(node.left) < 0:
                node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        if bf < -1:
            if self.get_balance(node.right) > 0:
                node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def get_balance(self, node):
        left_h = node.left.height if node.left else -1
        right_h = node.right.height if node.right else -1
        return left_h - right_h

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

    def assert_avl_property(self):
        def check(node):
            if node is None:
                return True
            if abs(self.get_balance(node)) > 1:
                return False
            return check(node.left) and check(node.right)

        return check(self.root)

    def search(self, pattern):
        results = []

        def dfs(node):
            if node is None:
                return

            if pattern.endswith("*"):
                prefix = pattern[:-1]
                if node.value.startswith(prefix):
                    results.append(node.movie_data)
                if node.value >= prefix:
                    dfs(node.left)
                if not node.value.startswith(prefix) or len(node.value) > len(prefix):
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
        start_pref = start_pattern[:-1] if start_pattern.endswith("*") else start_pattern
        end_pref = end_pattern[:-1] if end_pattern.endswith("*") else end_pattern

        def dfs(node):
            if node is None:
                return
            if start_pref <= node.value <= end_pref:
                results.append(node.movie_data)
            if node.value > start_pref:
                dfs(node.left)
            if node.value < end_pref:
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

    def zigzag_level_order(self, max_levels=10):
        if not self.root:
            return
    
        current_level = [self.root]
        left_to_right = True
        level = 0
    
        while current_level and level < max_levels:
            level_values = []
            next_level = []
        
            for node in current_level:
                level_values.append(str(node.movie_data.movie_id))
            
                if node.left:
                    next_level.append(node.left)
                if node.right:
                    next_level.append(node.right)
        
            if left_to_right:
                print(" ".join(level_values))
            else:
                print(" ".join(reversed(level_values)))
        
            current_level = next_level
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
        def compute_h(node):
            if node is None:
                return -1
            return 1 + max(compute_h(node.left), compute_h(node.right))

        return compute_h(self.root)


if __name__ == "__main__":
    filmovi_tim07 = []

    try:
        with open("movie.txt", encoding="windows-1250") as f:
            for i, line in enumerate(f):
                if i >= 6 and (i - 6) % 11 == 0:
                    parts = line.strip().split("\t")
                    if len(parts) >= 3:
                        filmovi_tim07.append(MoviesData(*parts[:3]))
    except FileNotFoundError:
        print("movie.txt nije pronađena, koristim test podatke.")
        test_data = [
            ("1", "Avatar", "Avatar (2009)"),
            ("2", "Bug", "Bug Life (1998)"),
            ("3", "Cars", "Cars (2006)"),
            ("4", "Dune", "Dune (2021)"),
            ("5", "Elf", "Elf (2003)"),
            ("6", "Frozen", "Frozen (2013)"),
            ("7", "Ghost", "Ghost (1990)"),
            ("8", "Heat", "Heat (1995)"),
            ("9", "Ice Age", "Ice Age (2002)"),
            ("10", "Jaws", "Jaws (1975)"),
        ]
        for mid, s, l in test_data:
            filmovi_tim07.append(MoviesData(mid, s, l))

    print(f"TIM07 - Učitano {len(filmovi_tim07)} filmova")

    stablo = BinaryTree()
    for film in filmovi_tim07:
        stablo.add(film)

    print(f"Visina AVL stabla: {stablo.height()}")
    print(f"AVL svojstvo zadovoljava: {stablo.assert_avl_property()}")
    stablo.print_rotation_counts()

    print("\nZig-zag ispis razina:")
    stablo.zigzag_level_order()

    print("\nMinimalni film:", stablo.find_min())
    print("Maksimalni film:", stablo.find_max())

    print("\nPretraga za 'Bug*':", stablo.search("Bug*"))
    print("Pretraga u rangu 'F*' do 'M*':", stablo.range_search("F*", "M*"))

    random.shuffle(filmovi_tim07)
    ubt = UnbalancedTree()
    for film in filmovi_tim07:
        ubt.add(film)

    print(f"\nVisina običnog BST: {ubt.height()}")

    avl_random = BinaryTree()
    for film in filmovi_tim07:
        avl_random.add(film)

    print(f"Visina AVL stabla za isti niz: {avl_random.height()}")


running = True
while running:
    print("\n=== IZBORNIK ===")
    print("a) Ispiši visinu dobivenog AVL stabla.")
    print("b) Pretraživanje podataka o filmu (koristi * za nepotpun naslov)")
    print("c) Pretraživanje u rangu od do za sve filmove")
    print("d) Ispiši minimalni i maksimalni film po indeksu")
    print("e) Ispiši broj lijevih i desnih rotacija")
    print("f) Zig-zag ispis prvih 10 razina AVL stabla")
    print("g) Usporedba visine nebalansiranog i AVL stabla")
    print("0) Izlaz")
    
    choice = input("Odaberi: ").strip().lower()
    
    match choice:
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
            running = False
        case _:
            print("Nepoznata opcija, pokušajte ponovno.")
