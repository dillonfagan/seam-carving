import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self, dp=True):
        seam = None

        if not dp:
            # dynamic programming disabled
            seam = self.naive()
        else:
            # dynamic programming enabled
            seam = self.dynamic()

        return seam

    def naive(self):
        max_x = self.width - 1
        max_y = self.height - 1
        matrix = []

        seam = []
        return seam

    def dynamic(self):
        max_x = self.width - 1
        max_y = self.height - 1
        memo = {}
        start = 0 # minimum energy pixel (i) in last row

        # first row of pixels (j = 0)
        for i in range(0, max_x):
            memo[i, 0] = self.energy(i, 0)

        # remaining rows
        for j in range(1, max_y):
            for i in range(0, max_x):
                p = []
                p.append(memo[i, j-1])

                try:
                    p.append(memo[i-1, j-1])
                except KeyError:
                    pass

                try:
                    p.append(memo[i+1, j-1])
                except KeyError:
                    pass

                memo[i, j] = min(x for x in p) + self.energy(i, j)

                if j == max_y and memo[i, j] < memo[start, j]:
                        start = i

        # climb up matrix to assemble seam
        seam = []
        j = max_y
        i = start # start from pixel in last row with min energy
        while j >= 0:
            seam.append((i, j))
            if j == 0:
                break

            j -= 1

            # determine next pixel in seam
            a = memo[i, j] # up
            b = None
            c = None

            if i > 0:
                b = memo[i-1, j] # up left
            if i < max_x:
                c = memo[i+1, j] # up right

            if b and b < a and b < c:
                i -= 1
            elif c and c < a and c < b:
                i += 1

        return seam

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
