class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.size = 0
    
    def parent(self, i):
        return (i - 1) // 2
    
    def left_child(self, i):
        return 2 * i + 1
    
    def right_child(self, i):
        return 2 * i + 2
    
    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def insert(self, key):
        self.heap.append(key)
        self.size += 1
        self._heapify_up(self.size - 1)
    
    def _heapify_up(self, i):
        parent = self.parent(i)
        if i > 0 and self.heap[i].frequency < self.heap[parent].frequency:
            self.swap(i, parent)
            self._heapify_up(parent)
    
    def _heapify_down(self, i):
        min_idx = i
        left = self.left_child(i)
        right = self.right_child(i)
        
        if left < self.size and self.heap[left].frequency < self.heap[min_idx].frequency:
            min_idx = left
        
        if right < self.size and self.heap[right].frequency < self.heap[min_idx].frequency:
            min_idx = right
            
        if min_idx != i:
            self.swap(i, min_idx)
            self._heapify_down(min_idx)
    
    def extract_min(self):
        if self.size == 0:
            return None
        
        if self.size == 1:
            self.size -= 1
            return self.heap.pop()
        
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.size -= 1
        self._heapify_down(0)
        
        return root

class HuffmanNode:
    def __init__(self, char=None, frequency=0):
        self.char = char
        self.frequency = frequency
        self.left = None
        self.right = None
        
    def is_leaf(self):
        return self.left is None and self.right is None

class HuffmanCoding:
    def __init__(self):
        self.codes = {}
        self.reverse_codes = {}
        
    def make_frequency_dict(self, text):
        frequency = {}
        for char in text:
            frequency[char] = frequency.get(char, 0) + 1
        return frequency
    
    def build_huffman_tree(self, text):
        frequency = self.make_frequency_dict(text)
        
        pq = PriorityQueue()
        for char, freq in frequency.items():
            node = HuffmanNode(char, freq)
            pq.insert(node)
        
        while pq.size > 1:
            left = pq.extract_min()
            right = pq.extract_min()
            
            internal = HuffmanNode()
            internal.frequency = left.frequency + right.frequency
            internal.left = left
            internal.right = right
            
            pq.insert(internal)
            
        return pq.extract_min()
    
    def make_codes_helper(self, root, current_code):
        if root is None:
            return
        
        if root.is_leaf():
            self.codes[root.char] = current_code
            self.reverse_codes[current_code] = root.char
            return
        
        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")
    
    def make_codes(self, root):
        self.make_codes_helper(root, "")
    
    def encode_text(self, text):
        encoded_text = ""
        for char in text:
            encoded_text += self.codes[char]
        return encoded_text
    
    def pad_encoded_text(self, encoded_text):
        padding_amount = 8 - (len(encoded_text) % 8)
        if padding_amount == 8:
            padding_amount = 0
            
        padded_text = encoded_text + "0" * padding_amount
        padded_info = format(padding_amount, "08b")
        
        return padded_info + padded_text
    
    def get_byte_array(self, padded_text):
        byte_array = bytearray()
        for i in range(0, len(padded_text), 8):
            byte = padded_text[i:i+8]
            byte_array.append(int(byte, 2))
        return byte_array
    
    def compress(self, input_file, output_file):
        with open(input_file, 'r') as file:
            text = file.read()
        
        root = self.build_huffman_tree(text)
        self.make_codes(root)
        
        encoded_text = self.encode_text(text)
        padded_text = self.pad_encoded_text(encoded_text)
        byte_array = self.get_byte_array(padded_text)

        with open(output_file, 'wb') as output:
            import pickle
            pickle.dump(self.codes, output)
            output.write(bytes(byte_array))

        dict_file = output_file + '_dictionary.txt'
        with open(dict_file, 'w') as dict_output:
            for char, code in sorted(self.codes.items()):
                dict_output.write(f'{repr(char)}: {code}\n')
    
    def remove_padding(self, padded_text):
        padding_info = padded_text[:8]
        padding_amount = int(padding_info, 2)
        
        actual_text = padded_text[8:]
        actual_text = actual_text[:-padding_amount] if padding_amount > 0 else actual_text
        
        return actual_text
    
    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""
        
        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_codes:
                decoded_text += self.reverse_codes[current_code]
                current_code = ""
                
        return decoded_text
    
    def decompress(self, input_file, output_file):
        with open(input_file, 'rb') as file:
            import pickle
            self.codes = pickle.load(file)
            self.reverse_codes = {v: k for k, v in self.codes.items()}

            byte_array = file.read()

        bit_string = ""
        for byte in byte_array:
            bits = format(byte, '08b')
            bit_string += bits
            
        actual_text = self.remove_padding(bit_string)
        decompressed_text = self.decode_text(actual_text)
        
        with open(output_file, 'w') as output:
            output.write(decompressed_text)

def Compression_Example():
    huffman = HuffmanCoding()        
    input_file = "tekst.txt"
    compressed_file = "skompresowany.bin"
    huffman.compress(input_file, compressed_file)

def Decompression_Example():
    huffman = HuffmanCoding()        
    decompressed_file = "zdekompresowany.txt"
    compressed_file = "skompresowany.bin"
    huffman.decompress(compressed_file, decompressed_file)   

if __name__ == "__main__":
    Compression_Example()
    #Decompression_Example()