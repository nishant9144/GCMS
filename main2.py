import random
from gcms import GCMS
from object import Color
from exceptions import NoBinFoundException
import time

random.seed(42)

def progress_bar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    total = len(iterable)
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    printProgressBar(0)
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    print()


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
    fixed_len = 25
    if colors is None:
        colors = list(Color)
    gcms = GCMS()
    stupid_gcms = StupidGCMS()
    objs = [(random.randint(1, 100), random.choice(list(colors))) for _ in range(n)]
    bins = [random.choice(list(range(bin_sizes[0], bin_sizes[1], bin_sizes[2]))) for _ in range(b)]
    x = list(range(n))
    random.shuffle(x)
    
    for i in progress_bar(range(b), prefix="Adding New Bins".ljust(fixed_len)):
        bin_size = bins[i]
        gcms.add_bin(i, bin_size)
        stupid_gcms.add_bin(i, bin_size)

    for i in progress_bar(range(b), prefix="Checking Added Bins".ljust(fixed_len)):
        if gcms.bin_info(i) != stupid_gcms.bin_info(i):
            print(f"[!] ERROR: Expected Bin Info for Bin - {i}: {stupid_gcms.bin_info(i)}, Received: {gcms.bin_info(i)}")
            return

    for i in progress_bar(range(n), prefix="Adding Objects".ljust(fixed_len)):
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
        if e1 != e2 and e1:
            print(f"[!] ERROR: Did not expect BinNotFoundException for Object - {i} with Size - {size} and Color - {color}")
            return
        elif e1 != e2 and e2:
            print(f"[!] ERROR: Expected BinNotFoundException for Object - {i} with Size - {size} and Color - {color}")
            return

    for i in progress_bar(range(n), prefix="Checking Added Objects".ljust(fixed_len)):
        if gcms.object_info(i) != stupid_gcms.object_info(i):
            print(f"[!] ERROR: Expected Object Info for Object - {i}: {stupid_gcms.object_info(i)}, Received: {gcms.object_info(i)}")
            return

    for i in progress_bar(range(b), prefix="Checking Updated Bins".ljust(fixed_len)):
        if gcms.bin_info(i) != stupid_gcms.bin_info(i):
            print(f"[!] ERROR: Expected Bin Info for Bin - {i}: {stupid_gcms.bin_info(i)}, Received: {gcms.bin_info(i)}")
            return

    for i in progress_bar(x[:len(x)//100], prefix="Deleting Objects".ljust(fixed_len)):
        gcms.delete_object(i)
        stupid_gcms.delete_object(i)
        for j in range(b):
            if gcms.bin_info(j) != stupid_gcms.bin_info(j):
                print(f"[!] ERROR: Expected Bin Info for Bin - {j} while deleting object {i}: {stupid_gcms.bin_info(j)}, Received: {gcms.bin_info(j)}")
                return
            # print(f"Checked Bin Info - {str(i).rjust(len(str(b-1)), ' ')}")
        if gcms.object_info(i) != stupid_gcms.object_info(i):
            print(f"[!] ERROR: Expected Object Info for Object - {i}: {stupid_gcms.object_info(i)}, Received: {gcms.object_info(i)}")
            return

    for i in progress_bar(range(b), prefix="Checking Updated Bins".ljust(fixed_len)):
        if gcms.bin_info(i) != stupid_gcms.bin_info(i):
            print(f"[!] ERROR: Expected Bin Info for Bin - {i}: {stupid_gcms.bin_info(i)}, Received: {gcms.bin_info(i)}")
            return

    for i in progress_bar(range(n), prefix="Checking Added Objects".ljust(fixed_len)):
        if gcms.object_info(i) != stupid_gcms.object_info(i):
            print(f"[!] ERROR: Expected Object Info for Object - {i}: {stupid_gcms.object_info(i)}, Received: {gcms.object_info(i)}")
            return
    for i in progress_bar(range(b//10), prefix="Adding New Bins".ljust(fixed_len)):
        bin_size = random.choice(list(range(bin_sizes[0], bin_sizes[1], bin_sizes[2])))
        gcms.add_bin(i+b, bin_size)
        stupid_gcms.add_bin(i+b, bin_size)
    for i in progress_bar(range(b+b//10), prefix="Checking Updated Bins".ljust(fixed_len)):
        if gcms.bin_info(i) != stupid_gcms.bin_info(i):
            print(f"[!] ERROR: Expected Bin Info for Bin - {i}: {stupid_gcms.bin_info(i)}, Received: {gcms.bin_info(i)}")
            return
    for i in progress_bar(range(n), prefix="Adding Objects".ljust(fixed_len)):
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
        if e1 != e2 and e1:
            print(f"[!] ERROR: Did not expect BinNotFoundException for Object - {i+n} with Size - {size} and Color - {color}")
            return
        elif e1 != e2 and e2:
            print(f"[!] ERROR: Expected BinNotFoundException for Object - {i} with Size - {size} and Color - {color}")
            return

    for i in progress_bar(range(n+n//10), prefix="Checking Added Objects".ljust(fixed_len)):
        if gcms.object_info(i) != stupid_gcms.object_info(i):
            print(f"[!] ERROR: Expected Object Info for Object - {i}: {stupid_gcms.object_info(i)}, Received: {gcms.object_info(i)}")
            return

    for i in progress_bar(range(b+b//10), prefix="Checking Updated Bins".ljust(fixed_len)):
        if gcms.bin_info(i) != stupid_gcms.bin_info(i):
            print(f"[!] ERROR: Expected Bin Info for Bin - {i}: {stupid_gcms.bin_info(i)}, Received: {gcms.bin_info(i)}")
            return

    x = list(range(n + n//10))
    random.shuffle(x)

    for i in progress_bar(x[:len(x)//100], prefix="Deleting Objects".ljust(fixed_len)):
        gcms.delete_object(i)
        stupid_gcms.delete_object(i)
        for j in range(b + b//10):
            if gcms.bin_info(j) != stupid_gcms.bin_info(j):
                print(f"[!] ERROR: Expected Bin Info for Bin - {j}: {stupid_gcms.bin_info(j)}, Received: {gcms.bin_info(j)}")
                return
            # print(f"Checked Bin Info - {str(i).rjust(len(str(b)), ' ')}")
        if gcms.object_info(i) != stupid_gcms.object_info(i):
            print(f"[!] ERROR: Expected Object Info for Object - {i}: {stupid_gcms.object_info(i)}, Received: {gcms.object_info(i)}")
            return
    for i in progress_bar(range(b + b // 10), prefix="Checking Updated Bins".ljust(fixed_len)):
        if gcms.bin_info(i) != stupid_gcms.bin_info(i):
            print(
                f"[!] ERROR: Expected Bin Info for Bin - {i}: {stupid_gcms.bin_info(i)}, Received: {gcms.bin_info(i)}")
            return
    for i in progress_bar(range(n + n // 10), prefix="Checking Objects".ljust(fixed_len)):
        if gcms.object_info(i) != stupid_gcms.object_info(i):
            print(f"[!] ERROR: Expected Object Info for Object - {i}: {stupid_gcms.object_info(i)}, Received: {gcms.object_info(i)}")
            return
    # print(gcms)
    print("[+] All tests passed!!")


if __name__ == "__main__":
    main(10000, 1000, (10, 1000, 10), None)
    # pass