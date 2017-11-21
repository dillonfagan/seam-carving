import imagematrix
from time import time

class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self, dp = True):
        seam = None

        if not dp:
            # dynamic programming disabled
            seam = self.naive()
        else:
            # dynamic programming enabled
            seam = self.dynamic()

        return seam

    def dynamic(self):
        max_x = self.width - 1
        max_y = self.height - 1
        memo = {} # energy of points already evaluated
        prev = {} # previous pixel (lowest energy) for every pixel
        start = 0 # i value of cheapest pixel in last row

        # first row of pixels (j = 0)
        for i in range(0, max_x + 1):
            memo[i, 0] = self.energy(i, 0)

        # remaining rows
        for j in range(1, max_y + 1):
            for i in range(0, max_x + 1):
                lowest = (i, j-1)

                try:
                    if memo[i-1, j-1] < memo[lowest]:
                        lowest = (i-1, j-1)
                except KeyError:
                    pass

                try:
                    if memo[i+1, j-1] < memo[lowest]:
                        lowest = (i+1, j-1)
                except KeyError:
                    pass

                memo[i, j] = memo[lowest] + self.energy(i, j)
                prev[i, j] = lowest

                if j == max_y:
                    if memo[i, max_y] < memo[start, max_y]:
                        start = i

        # climb up matrix to assemble seam
        seam = []
        j = max_y
        i = start # start from pixel in last row with min energy
        while j >= 0:
            seam.append((i, j))
            if j == 0:
                break

            # determine next pixel in seam
            i, j = prev[i, j]

        return seam

    def naive(self):
        def recurse(i, j, memo = {}, seam = []):
            if (i, j) not in memo:
                memo[i, j] = self.energy(i, j)

            if j == 0:
                return seam
            else:
                p = []

                p.append((self.energy(i, j-1), (i, j-1)))

                try:
                    p.append((self.energy(i-1, j-1), (i-1, j-1)))
                except Exception:
                    pass

                try:
                    p.append((self.energy(i+1, j-1), (i+1, j-1)))
                except Exception:
                    pass

                lowest = min(p, key = lambda x: x[0])
                seam.append(lowest[1])

                return recurse(lowest[1][0], j-1, memo, seam)

        memo = {}
        seams = []
        i = 0
        while i < self.width:
            s = recurse(i, self.height - 1, memo)
            seams.append(s)
            i += 1

        seam = seams[0]
        for s in seams:
            if memo[s[0]] < memo[seam[0]]:
                seam = s

        return seam

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
