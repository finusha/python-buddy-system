import math

class BuddySystem:
    def __init__(self, total_memory):
        self.total_memory = total_memory
        self.memory = {0: total_memory}  # A single block starting at 0 with total memory
        self.allocated_blocks = {}

    def allocate_process(self, process_id, process_size):
        block_to_allocate = None
        for block, size in sorted(self.memory.items()):
            if size >= process_size:
                block_to_allocate = block
                break

        if block_to_allocate is None:
            print(f"Allocation failed: Not enough memory available for process {process_id}.")
            return None

        required_block_size = 2 ** math.ceil(math.log2(process_size))  # Find smallest power of 2

        # Split blocks if the block is larger than the required size
        while self.memory[block_to_allocate] > required_block_size:
            half_size = self.memory[block_to_allocate] // 2
            self.memory[block_to_allocate] = half_size
            self.memory[block_to_allocate + half_size] = half_size

        # Allocate the block
        allocated_block = block_to_allocate
        del self.memory[allocated_block]  # Remove block from free list
        self.allocated_blocks[process_id] = required_block_size
        print(f"Successfully allocated memory for process {process_id}.")
        return allocated_block

    def deallocate_process(self, process_id):
        if process_id not in self.allocated_blocks:
            print(f"Deallocation failed: Process {process_id} not found.")
            return

        # Retrieve the size of the allocated block
        block_size = self.allocated_blocks[process_id]
        del self.allocated_blocks[process_id]

        # Add the block back to the free list
        self.memory[block_size] = block_size  # The free block size should match the block size
        print(f"Successfully deallocated memory for process {process_id}.")

        # Try to merge with adjacent blocks if they are the same size
        self.merge_block()

    def merge_block(self):
        # Merging adjacent blocks of the same size in free memory
        free_blocks = sorted(self.memory.items())
        i = 0
        while i < len(free_blocks) - 1:
            block1, size1 = free_blocks[i]
            block2, size2 = free_blocks[i + 1]
            if size1 == size2:
                # Merge the blocks if they are of the same size
                del self.memory[block1]
                del self.memory[block2]
                self.memory[min(block1, block2)] = size1 * 2
                i = 0  # Restart merging check from the beginning
                free_blocks = sorted(self.memory.items())  # Re-sort after merge
            else:
                i += 1

    def display_memory(self):
        print("\nMemory State:")
        # Create a sorted list of all blocks and their states (allocated or free)
        blocks = []

        # Add free blocks
        for block, size in sorted(self.memory.items()):
            blocks.append(f"{size} KB (free)")

        # Add allocated blocks
        for process_id, block_size in self.allocated_blocks.items():
            blocks.append(f"{block_size} KB (allocated)")

        # Display the memory blocks state as requested
        for block in blocks:
            print(f" {block}")

def main():
    print("-Buddy System -s92061036-")
    total_memory = int(input("Enter total size of memory: "))
    buddy_system = BuddySystem(total_memory)

    while True:
        print("\n1. Allocate process into memory")
        print("2. Remove process from memory")
        print("3. Display memory allocation status")
        print("4. Exit")

        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Invalid choice. Please enter a number between 1 and 4.")
            continue

        if choice == 1:
            process_id = input("Enter Process ID: ")
            try:
                process_size = int(input("Enter size of process (in KB): "))
            except ValueError:
                print("Invalid process size. Please enter a valid integer.")
                continue
            buddy_system.allocate_process(process_id, process_size)

        elif choice == 2:
            process_id = input("Enter Process ID to deallocate: ")
            buddy_system.deallocate_process(process_id)

        elif choice == 3:
            buddy_system.display_memory()

        elif choice == 4:
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
