class LightController:
    def __init__(self, n: int, corresponding_lights_list: list[list[int]]) -> None:
        self.n = n  # number of lights
        self.m = len(corresponding_lights_list)  # number of switches
        self.basis = []
        self.solution_vectors = []
        self.pivot_col = [-1] * n  # light i is controlled by basis row j

        # Build matrix: each row is a switch → represented as an integer of light toggles
        A = []
        switch_vectors = []

        for i, lights in enumerate(corresponding_lights_list):
            row = 0
            for l in lights:
                row |= 1 << l
            A.append(row)
            switch_vectors.append(1 << i)

        # Gauss-Jordan elimination in GF(2)
        for i in range(self.m):
            row = A[i]
            vec = switch_vectors[i]
            for j in range(n):
                if (row >> j) & 1:
                    if self.pivot_col[j] == -1:
                        # pivot found
                        self.pivot_col[j] = len(self.basis)
                        self.basis.append(row)
                        self.solution_vectors.append(vec)
                        break
                    else:
                        k = self.pivot_col[j]
                        row ^= self.basis[k]
                        vec ^= self.solution_vectors[k]

    def solve(self, lights: list[int]) -> list[int] | None:
        target = 0
        for l in lights:
            target |= 1 << l

        x = 0
        for j in range(self.n):
            if (target >> j) & 1:
                k = self.pivot_col[j]
                if k == -1:
                    return None
                target ^= self.basis[k]
                x ^= self.solution_vectors[k]

        return [i for i in range(self.m) if (x >> i) & 1]
