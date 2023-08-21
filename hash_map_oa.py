# Name: Blake Jennings
# Email: blakej94@gmail.com
# Description: A hash map that uses open addressing and its various methods.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        is 0.5 or greater, it calls resize to increase the HashMap capacity. If
        the intended index is already occupied, it uses quadratic probing to
        find the next available index.

        :param key:   string to assign to key of key/value pair
        :param value: object to assign to value of key/value pair

        :return:      None
        """
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity*2)
        step = 1
        hash = self._hash_function(key)
        ind = hash%self._capacity
        first_ind = ind
        new = HashEntry(key, value)
        while self._buckets.get_at_index(ind) is not None:
            if self._buckets.get_at_index(ind).key == new.key:
                if self._buckets.get_at_index(ind).is_tombstone is True:
                    self._buckets.get_at_index(ind).is_tombstone = False
                    self._size += 1
                self._buckets.get_at_index(ind).value = new.value
                return
            else:
                ind = (first_ind+step**2)%self._capacity
                step += 1
        self._buckets.set_at_index(ind, new)
        self._size += 1

    def table_load(self) -> float:
        """
        Returns the current load factor of the hash table.

        :return: float indicating load factor
        """
        return self._size/self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.

        :return: number of empty buckets
        """
        return self._capacity-self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the capacity of the hash table and rehashes the current
        key/value pairs in the table. If new_capacity is 1 or more,
        makes sure it is a prime number and changes it to the next highest
        prime number if it is not.

        :param new_capacity: new desired capacity for the hash table

        :return:             None
        """
        if new_capacity < self._size:
            return
        items = self.get_keys_and_values()
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)
        self._capacity = new_capacity
        self._buckets = DynamicArray()
        self._size = 0
        for ind in range(new_capacity):
            self._buckets.append(None)
        for item in range(items.length()):
            self.put(items.get_at_index(item)[0], items.get_at_index(item)[1])

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key.

        :param key: key to find value of

        :return:    value if the key exists in the hash map
                    None otherwise
        """
        step = 1
        hash = self._hash_function(key)
        ind = hash%self._capacity
        new_ind = ind
        while self._buckets.get_at_index(ind) is not None and self._buckets.get_at_index(ind).key != key:
            ind = (new_ind+step**2) % self._capacity
            step += 1
        if self._buckets.get_at_index(ind) is None:
            return None
        if self._buckets.get_at_index(ind).is_tombstone is True:
            return None
        return self._buckets.get_at_index(ind).value

    def contains_key(self, key: str) -> bool:
        """
        Determines if the given key is in the hash map.

        :param key: key to analyze if it exists in the hash map

        :return:    True if the key exists in the hash map
                    False otherwise
        """
        step = 1
        hash = self._hash_function(key)
        ind = hash%self._capacity
        new_ind = ind
        while self._buckets.get_at_index(ind) is not None and self._buckets.get_at_index(ind).key != key:
            ind = (new_ind+step**2)%self._capacity
            step += 1
        if self._buckets.get_at_index(ind) is None:
            return False
        if self._buckets.get_at_index(ind).is_tombstone is False:
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its value from the hash table by turning the objects
        tombstone to true. Does nothing if the key does not exist.

        :param key: key to remove from the hash map

        :return:    None
        """
        step = 1
        hash = self._hash_function(key)
        ind = hash%self._capacity
        new_ind = ind
        while self._buckets.get_at_index(ind) is not None and self._buckets.get_at_index(ind).key != key:
            ind = (new_ind+step**2)%self._capacity
            step += 1
        if self._buckets.get_at_index(ind) is None:
            return
        if self._buckets.get_at_index(ind).is_tombstone is False:
            self._buckets.get_at_index(ind).is_tombstone = True
            self._size -= 1

    def clear(self) -> None:
        """
        Clears the hash table without changing its capacity.

        :return: None
        """
        new = self._capacity
        self._buckets = DynamicArray()
        for ind in range(new):
            self._buckets.append(None)
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a DynamicArray of all the key/value pairs in the hash map
        in the form of tuples.

        :return: DynamicArray of key/value tuples of every key/value pair
                 in the hash map
        """
        new_array = DynamicArray()
        for ind in range(self._capacity):
            pair = self._buckets.get_at_index(ind)
            if pair is not None:
                if pair.is_tombstone is False:
                    new_array.append((pair.key, pair.value))
        return new_array

    def __iter__(self):
        """
        Enables self-iteration of the hash map.

        :return: the hash map
        """
        self._index = 0

        return self

    def __next__(self):
        """
        Returns the next item in the hash map, based on the current
        location of the iterator.

        :return: next item in the hash map
        """
        try:
            while self._buckets.get_at_index(self._index) is None or self._buckets.get_at_index(self._index).is_tombstone is True:
                self._index = self._index+1
        except DynamicArrayException:
            raise StopIteration
        try:
            value = self._buckets.get_at_index(self._index)
        except DynamicArrayException:
            raise StopIteration
        self._index = self._index+1
        return value

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
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
