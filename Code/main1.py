import random
from new_gcms import GCMS
from object import Color
from exceptions import NoBinFoundException

class StupidGCMS:
    def __init__(self):
        self.gcm = {}
        self.sorted_by_capacities = {}
        self.object_info_dic = {}

    def add_bin(self, bin_id, capacity):
        self.gcm[bin_id] = {'capacity': capacity, 'objects': []}
        if capacity not in self.sorted_by_capacities:
            self.sorted_by_capacities[capacity] = []
        self.sorted_by_capacities[capacity].append(bin_id)

    def add_object(self, object_id, size, color):
        bin_id = None
        if color == Color.BLUE:
            for capacity in sorted(self.sorted_by_capacities.keys()):
                if capacity >= size:
                    bin_id = sorted(self.sorted_by_capacities[capacity])[0]
                    break
        elif color == Color.YELLOW:
            for capacity in sorted(self.sorted_by_capacities.keys()):
                if capacity >= size:
                    bin_id = sorted(self.sorted_by_capacities[capacity])[-1]
                    break
        elif color == Color.RED:
            capacity = sorted(self.sorted_by_capacities.keys())[-1]
            if capacity >= size:
                bin_id = sorted(self.sorted_by_capacities[capacity])[0]
        else:
            capacity = sorted(self.sorted_by_capacities.keys())[-1]
            if capacity >= size:
                bin_id = sorted(self.sorted_by_capacities[capacity])[-1]
        if bin_id is None:
            raise NoBinFoundException
        capacity = self.gcm[bin_id]['capacity']
        self.gcm[bin_id]['objects'].append(object_id)
        self.object_info_dic[object_id] = {'size': size, 'color': color, 'bin_id': bin_id}
        self.sorted_by_capacities[self.gcm[bin_id]['capacity']].remove(bin_id)
        if len(self.sorted_by_capacities[self.gcm[bin_id]['capacity']]) == 0:
            del self.sorted_by_capacities[self.gcm[bin_id]['capacity']]
        self.gcm[bin_id]['capacity'] -= size
        if (capacity - size) not in self.sorted_by_capacities:
            self.sorted_by_capacities[capacity - size] = []
        self.sorted_by_capacities[capacity-size].append(bin_id)

    def delete_object(self, object_id):
        if object_id not in self.object_info_dic:
            return
        bin_id = self.object_info_dic[object_id]['bin_id']
        size = self.object_info_dic[object_id]['size']
        capacity = self.gcm[bin_id]['capacity']
        self.gcm[bin_id]['objects'].remove(object_id)
        self.sorted_by_capacities[self.gcm[bin_id]['capacity']].remove(bin_id)
        self.gcm[bin_id]['capacity'] += size
        if (capacity + size) not in self.sorted_by_capacities:
            self.sorted_by_capacities[capacity+size] = []
        self.sorted_by_capacities[capacity+size].append(bin_id)
        if not self.sorted_by_capacities[capacity]:
            del self.sorted_by_capacities[capacity]
        del self.object_info_dic[object_id]

    def bin_info(self, bin_id):
        return self.gcm[bin_id]['capacity'], self.gcm[bin_id]['objects']

    def object_info(self, object_id):
        if object_id not in self.object_info_dic:
            return None
        return self.object_info_dic[object_id]['bin_id']


def main(n=10**4, b=1000, bin_sizes=(10, 1000, 10), colors=None):
    if colors is None:
        colors = list(Color)
    gcms = GCMS()
    stupid_gcms = StupidGCMS()
    objs = [(random.randint(1, 100), random.choice(list(colors))) for _ in range(n)]
    bins = [random.choice(list(range(bin_sizes[0], bin_sizes[1], bin_sizes[2]))) for _ in range(b)]
    for i in range(b):
        bin_size = bins[i]
        gcms.add_bin(i, bin_size)
        stupid_gcms.add_bin(i, bin_size)
        c = str(i).rjust(len(str(b-1)), ' ')
        bin_size_s = str(bin_size).rjust(len(str(bin_sizes[1])), ' ')
        print(f"Added bin {c} - {bin_size_s}")
    for i in range(b):
        assert gcms.bin_info(i) == stupid_gcms.bin_info(i)
        print(f"Checked Bin Info - {str(i).rjust(len(str(b-1)), ' ')}")
    for i in range(n):
        color = objs[i][1]
        size = objs[i][0]
        e1 = False
        e2 = False
        try:
            gcms.add_object(i, size, color)
        except NoBinFoundException:
            e1 = True
        try:
            stupid_gcms.add_object(i, size, color)
        except NoBinFoundException:
            e2 = True
        for j in range(b):
            if gcms.bin_info(j) != stupid_gcms.bin_info(j):
                print(gcms.bin_info(j), stupid_gcms.bin_info(j))
            assert gcms.bin_info(j) == stupid_gcms.bin_info(j)
            print(f"Checked Bin Info - {str(j).rjust(len(str(b-1)), ' ')}")
        if e1 != e2:
            print(e1, e2)
        assert e1 == e2
        if not e1:
            print(f"Added Object - {str(i).rjust(len(str(n-1)), ' ')} to Bin - {str(gcms.object_info(i)).rjust(len(str(b-1)), ' ')}")
    for i in range(n):
        assert gcms.object_info(i) == stupid_gcms.object_info(i)
        print(f"Checked Object Info - {str(i).rjust(len(str(n-1)), ' ')}")
    for i in range(b):
        assert gcms.bin_info(i) == stupid_gcms.bin_info(i)
        print(f"Checked Bin Info - {str(i).rjust(len(str(b-1)), ' ')}")
    x = list(range(n))
    random.shuffle(x)
    for i in x[:len(x)//100]:
        gcms.delete_object(i)
        stupid_gcms.delete_object(i)
        print(f"Deleted Object - {str(i).rjust(len(str(n-1)), ' ')}")
        for j in range(b):
            assert gcms.bin_info(j) == stupid_gcms.bin_info(j)
            # print(f"Checked Bin Info - {str(i).rjust(len(str(b-1)), ' ')}")
        assert gcms.object_info(i) == stupid_gcms.object_info(i)
        print(f"Checked Object - {str(i).rjust(len(str(n-1)), ' ')}")
    for i in range(b):
        assert gcms.bin_info(i) == stupid_gcms.bin_info(i)
        print(f"Checked Bin Info - {str(i).rjust(len(str(b-1)), ' ')}")
    for i in range(n):
        assert gcms.object_info(i) == stupid_gcms.object_info(i)
        print(f"Checked Object Info - {str(i).rjust(len(str(n-1)), ' ')}")
    for i in range(b//10):
        bin_size = random.choice(list(range(bin_sizes[0], bin_sizes[1], bin_sizes[2])))
        gcms.add_bin(i+b, bin_size)
        stupid_gcms.add_bin(i+b, bin_size)
        print(f"Added bin {str(i+b).rjust(len(str(b)), ' ')}")
    for i in range(b + b//10):
        assert gcms.bin_info(i) == stupid_gcms.bin_info(i)
        print(f"Checked Bin Info - {str(i).rjust(len(str(b)), ' ')}")
    for i in range(n//10):
        color = random.choice(list(Color))
        size = random.randint(1, 100)
        e1 = False
        e2 = False
        try:
            gcms.add_object(i+n, size, color)
        except NoBinFoundException:
            e1 = True
        try:
            stupid_gcms.add_object(i+n, size, color)
        except NoBinFoundException:
            e2 = True
        assert e1 == e2
        if not e1:
            print(f"Added Object - {str(i+n).rjust(len(str(n)), ' ')} to Bin - {str(gcms.object_info(i+n)).rjust(len(str(b)), ' ')}")
    for i in range(n + n//10):
        assert gcms.object_info(i) == stupid_gcms.object_info(i)
        print(f"Checked Object Info - {str(i).rjust(len(str(n)), ' ')}")
    for i in range(b + b//10):
        assert gcms.bin_info(i) == stupid_gcms.bin_info(i)
        print(f"Checked Bin Info - {str(i).rjust(len(str(b)), ' ')}")
    x = list(range(n + n//10))
    random.shuffle(x)
    for i in x[:len(x)//100]:
        gcms.delete_object(i)
        stupid_gcms.delete_object(i)
        print(f"Deleted Object - {str(i).rjust(len(str(n)), ' ')}")
        for j in range(b + b//10):
            assert gcms.bin_info(j) == stupid_gcms.bin_info(j)
            # print(f"Checked Bin Info - {str(i).rjust(len(str(b)), ' ')}")
        assert gcms.object_info(i) == stupid_gcms.object_info(i)
        print(f"Checked Object - {str(i).rjust(len(str(n)), ' ')}")
    for i in range(b + b//10):
        assert gcms.bin_info(i) == stupid_gcms.bin_info(i)
        print(f"Checked Bin Info - {str(i).rjust(len(str(b)), ' ')}")
    for i in range(n + n//10):
        assert gcms.object_info(i) == stupid_gcms.object_info(i)
        print(f"Checked Object Info - {str(i).rjust(len(str(n)), ' ')}")
    # print(gcms)
    print("All tests passed!!")


if __name__ == "__main__":
    main(10000, 1000, (10, 1000, 10), None)