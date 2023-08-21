# Name: Blake Jennings
# Email: blakej94@gmail.com
# Description: A hash map that uses chaining and its various methods.

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Adds a key/value pair to the HashMap. If the key already exists,
        it updates the keys value to the new value. If the current load_factor
        is 1.0 or greater, it calls resize to increase the HashMap capacity.

        :param key:   string to assign to key of key/value pair
        :param value: object to assign to value of key/value pair

        :return:      None
        """
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity*2)
        hash = self._hash_function(key)
        ind = hash%self._capacity
        final = self._buckets.get_at_index(ind)
        check = final.contains(key)
        if check is not None:
            check.value = value
        else:
            final.insert(key, value)
            self._size += 1

    def new_put(self, key: str, value: object) -> None:
        """
        Helper method for find_mode that acts the same as put without
        replacing nodes if they have the same key.

        :param key:   string to assign to key of key/value pair
        :param value: object to assign to value of key/value pair

        :return:      None
        """
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity*2)
        hash = self._hash_function(key)
        ind = hash%self._capacity
        final = self._buckets.get_at_index(ind)
        final.insert(key, value)
        self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.

        :return: number of empty buckets
        """
        used = 0
        for bucket in range(self._capacity):
            if self._buckets.get_at_index(bucket).length() > 0:
                used += 1
        return self._capacity-used

    def table_load(self) -> float:
        """
        Returns the current load factor of the hash table.

        :return: float indicating load factor
        """
        return self._size/self._capacity

    def clear(self) -> None:
        """
        Clears the hash table without changing its capacity.

        :return: None
        """
        new = self._capacity
        self._buckets = DynamicArray()
        for ind in range(new):
            self._buckets.append(LinkedList())
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the capacity of the hash table and rehashes the current
        key/value pairs in the table. If new_capacity is 1 or more,
        makes sure it is a prime number and changes it to the next highest
        prime number if it is not.

        :param new_capacity: new desired capacity for the hash table

        :return:             None
        """
        if new_capacity < 1:
            return
        items = self.get_keys_and_values()
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)
        self._capacity = new_capacity
        self._buckets = DynamicArray()
        self._size = 0
        for ind in range(new_capacity):
            self._buckets.append(LinkedList())
        for item in range(items.length()):
            self.put(items.get_at_index(item)[0], items.get_at_index(item)[1])

    def get(self, key: str):
        """
        Returns the value associated with the given key.

        :param key: key to find value of

        :return:    value if the key exists in the hash map
                    None otherwise
        """
        hash = self._hash_function(key)
        ind = hash%self._capacity
        node = self._buckets.get_at_index(ind).contains(key)
        if node is not None:
            return node.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Determines if the given key is in the hash map.

        :param key: key to analyze if it exists in the hash map

        :return:    True if the key exists in the hash map
                    False otherwise
        """
        hash = self._hash_function(key)
        ind = hash%self._capacity
        node = self._buckets.get_at_index(ind).contains(key)
        if node is not None:
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its value from the hash map.
        Does nothing if the key does not exist.

        :param key: key to remove from the hash map

        :return:    None
        """
        hash = self._hash_function(key)
        ind = hash%self._capacity
        link = self._buckets.get_at_index(ind)
        if link.contains(key):
            link.remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a DynamicArray of all the key/value pairs in the hash map
        in the form of tuples.

        :return: DynamicArray of key/value tuples of every key/value pair
                 in the hash map
        """
        new_array = DynamicArray()
        for ind in range(self._buckets.length()):
            link = self._buckets.get_at_index(ind)
            if link.length() > 0:
                for node in link:
                    new_array.append((node.key, node.value))
        return new_array


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Finds the most often occurring value of a given DynamicArray.

    :param da: DynamicArray to determine mode of

    :return: a tuple of a DynamicArray of the most occurring value(s) and
             an integer declaring the frequency of the value(s)
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap(da.length(), hash_function_1)
    val = 0
    for ind in range(da.length()):
        key = da.get_at_index(ind)
        value = str(val)
        map.new_put(key, value)
        val += 1
    new_da = map.get_keys_and_values()
    # Initializes value count to 1
    count = 1
    # Count of most frequent value
    final_count = 0
    # Initializes first value of array as most frequent until another value
    # becomes more frequent
    final_object = new_da.get_at_index(0)[0]
    new_array = DynamicArray()
    new_array.append(final_object)
    for ind in range(0, new_da.length()):
        if ind+1 >= new_da.length() or new_da.get_at_index(ind)[0] != new_da.get_at_index(ind+1)[0]:
            if count > final_count:
                final_count = count
                final_object = new_da.get_at_index(ind)[0]
                new_array = DynamicArray()
                new_array.append(final_object)
            elif count == final_count:
                final_object = new_da.get_at_index(ind)[0]
                new_array.append(final_object)
            count = 1
        elif new_da.get_at_index(ind)[0] == new_da.get_at_index(ind+1)[0]:
            count += 1
    return (new_array, final_count)

# ------------------- BASIC TESTING ---------------------------------------- #


if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
