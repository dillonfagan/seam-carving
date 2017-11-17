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
        max_x = self.width
        max_y = self.height
        matrix = []
        start = 1 # minimum energy pixel (i) in last row

        # first row of pixels
        matrix.append([])
        for x in range(0, max_x):
            matrix[0].append(self.energy(x, 0))

        # remaining rows
        for j in range(1, max_y):
            matrix.append([])
            for i in range(0, max_x):
                p = []
                p.append(matrix[j - 1][i])

                try:
                    p.append(matrix[j - 1][i - 1])
                except IndexError:
                    pass

                try:
                    p.append(matrix[j - 1][i + 1])
                except IndexError:
                    pass

                matrix[j].append(min(x for x in p) + self.energy(i, j))

                if j == max_y and matrix[j][i] < matrix[j][start]:
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

            print(j, i)
            # determine next pixel in seam
            a = matrix[j][i] # up
            b = None
            c = None

            if i > 0:
                b = matrix[j][i - 1] # up left
            if i < max_x:
                c = matrix[j][i + 1] # up right

            if b and b < a and b < c:
                i -= 1
            elif c and c < a and c < b:
                i += 1

        return seam

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
