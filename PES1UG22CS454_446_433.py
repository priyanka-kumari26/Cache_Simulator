import math

class Cache:
    def __init__(self):
        self.tag = -1
        self.block = 0
        self.valid = 0
        self.dirty = 0  # Add the dirty attribute


class CacheSimulator:
    def __init__(self):
        self.hit = 0
        self.miss = 0
        self.evictions = 0
        self.mem_size = 0
        self.cache_size = 0
        self.block_size = 0
        self.lines = 0
        self.offset_bits = 0
        self.index_bits = 0
        self.tag_bits = 0
        self.cache = []

    def initialize_cache(self):
        self.cache = [Cache() for _ in range(self.lines)]

    def display(self):
      print("Index\tValid\tTag\t\tData (Hex)\tDirty Bit")
      for i, entry in enumerate(self.cache):
        if entry.tag != -1:
            print(f"{i}\t{entry.valid}\t{entry.tag:07b}\tBLOCK {entry.block} ")
        else:
            print(f"{i}\t{entry.valid}\t-\t\t0\t{entry.dirty}")


    def direct_mapping(self, ref):
        offset = ref & ((1 << self.offset_bits) - 1)
        temp = ref >> self.offset_bits
        index = temp & ((1 << self.index_bits) - 1)
        tag = temp >> self.index_bits

        print("---------------------------------------")
        print("Tag \t\t Index \t\t Offset")
        print(f"{tag:0{self.tag_bits}b}\t\t {index:0{self.index_bits}b}\t\t {offset:0{self.offset_bits}b}")
        print(f"{self.tag_bits} bits \t\t {self.index_bits} bits \t\t {self.offset_bits} bits")

        print("---------------------------------------")

        if self.cache[index].valid == 0:
            print("Miss")
            self.miss += 1
            self.cache[index].tag = tag
            self.cache[index].valid = 1
            self.cache[index].block = temp
        else:
            if self.cache[index].tag != tag:
                print("Miss")
                self.miss += 1
                self.evictions += 1
                self.cache[index].tag = tag
                self.cache[index].block = temp
            else:
                print("Hit")
                self.hit += 1

    def get_input(self):
        self.mem_size = int(input("Enter the size of main memory: "))
        while self.mem_size <= 0 or not self.is_power_of_two(self.mem_size):
            self.mem_size = int(input("Main memory size should be greater than 0 and a power of 2. Please enter again: "))

        self.cache_size = int(input("Enter the size of the cache: "))
        while self.cache_size <= 0 or not self.is_power_of_two(self.cache_size):
            self.cache_size = int(input("Cache size should be greater than 0 and a power of 2. Please enter again: "))

        self.block_size = int(input("Enter the block size: "))
        while self.block_size <= 0 or not self.is_power_of_two(self.block_size):
            self.block_size = int(input("Block size should be greater than 0 and a power of 2. Please enter again: "))

        self.lines = self.cache_size // self.block_size
        self.offset_bits = self.log2(self.block_size)
        self.index_bits = self.log2(self.lines)
        self.tag_bits = int(math.log2(self.mem_size)-self.index_bits-self.offset_bits)

    def simulate_cache(self):
        print("---------------------------------------")
        self.display()
        print("---------------------------------------")

        while True:
            ref = int(input("Enter main memory address (in decimal) (-1 to exit): "))
            if ref == -1:
                break
            if ref > self.mem_size:
                print("Enter valid memory address")
            else:
                self.direct_mapping(ref)
                print("---------------------------------------")
                self.display()
                print("---------------------------------------")

        print("---------------------------------------")
        print(f"Total Hits: {self.hit} Total Misses: {self.miss} Total Evictions: {self.evictions}")
        print(f"Hit Ratio: {self.hit / (self.hit + self.miss)} Miss Ratio: {self.miss / (self.hit + self.miss)}")
        print("---------------------------------------")

    @staticmethod
    def log2(n):
        return int(math.log2(n))

    @staticmethod
    def is_power_of_two(n):
        return (n & (n - 1)) == 0 and n != 0

def main():
    simulator = CacheSimulator()
    simulator.get_input()
    simulator.initialize_cache()
    simulator.simulate_cache()

if __name__ == "__main__":
    main()