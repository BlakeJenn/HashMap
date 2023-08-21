# HashMap
A Hash Map data structure in Python, incorporating linked lists and dynamic arrays for efficient memory management and key-value storage.

Chaining Hash Map Methods:

put(self, key: str, value: object) -> None:
This method updates the key/value pair in the hash map. If the given key already exists in
the hash map, its associated value is replaced with the new value. If the given key is
not in the hash map, a new key/value pair is added.

empty_buckets(self) -> int:
This method returns the number of empty buckets in the hash table.

table_load(self) -> float:
This method returns the current hash table load factor.

clear(self) -> None:
This method clears the contents of the hash map. It does not change the underlying hash
table capacity.

resize_table(self, new_capacity: int) -> None:
This method changes the capacity of the internal hash table. All existing key/value pairs
remain in the new hash map, and all hash table links are rehashed.
First checks that new_capacity is not less than 1; if so, the method does nothing.
If new_capacity is 1 or more, it makes sure it is a prime number. If not, it changes it to the next
highest prime number.

get(self, key: str) -> object:
This method returns the value associated with the given key. If the key is not in the hash
map, the method returns None.

contains_key(self, key: str) -> bool:
This method returns True if the given key is in the hash map, otherwise it returns False. An
empty hash map does not contain any keys.

remove(self, key: str) -> None:
This method removes the given key and its associated value from the hash map. If the key
is not in the hash map, the method does nothing (no exception needs to be raised).

get_keys_and_values(self) -> DynamicArray:
This method returns a dynamic array where each index contains a tuple of a key/value pair
stored in the hash map. The order of the keys in the dynamic array does not matter.

find_mode(arr: DynamicArray) -> tuple[DynamicArray, int]:
A standalone function outside of the HashMap class that receives a dynamic array,
which is not guaranteed to be sorted. This function returns a tuple containing, in this
order, a dynamic array comprising the mode (most occurring) value(s) of the given array,
and an integer representing the highest frequency of occurrence for the mode value(s).
If there is more than one value with the highest frequency, all values at that frequency
are included in the array being returned (the order does not matter). If there is only
one mode, the dynamic array will only contain that value.


Open Addressing Hash Map Methods:

put(self, key: str, value: object) -> None:
This method updates the key/value pair in the hash map. If the given key already exists in
the hash map, its associated value is replaced with the new value. If the given key is
not in the hash map, a new key/value pair is added.

table_load(self) -> float:
This method returns the current hash table load factor.

empty_buckets(self) -> int:
This method returns the number of empty buckets in the hash table.

resize_table(self, new_capacity: int) -> None:
This method changes the capacity of the internal hash table. All existing key/value pairs
remain in the new hash map, and all hash table links are rehashed.
First it checks that new_capacity is not less than the current number of elements in the hash
map; if so, the method does nothing.
If new_capacity is valid, it makes sure it is a prime number; if not, it changes it to the next
highest prime number.

get(self, key: str) -> object:
This method returns the value associated with the given key. If the key is not in the hash
map, the method returns None.

contains_key(self, key: str) -> bool:
This method returns True if the given key is in the hash map, otherwise it returns False. An
empty hash map does not contain any keys.

remove(self, key: str) -> None:
This method removes the given key and its associated value from the hash map. If the key
is not in the hash map, the method does nothing (no exception needs to be raised).

clear(self) -> None:
This method clears the contents of the hash map. It does not change the underlying hash
table capacity.

get_keys_and_values(self) -> DynamicArray:
This method returns a dynamic array where each index contains a tuple of a key/value pair
stored in the hash map. The order of the keys in the dynamic array does not matter.

__iter__():
This method enables the hash map to iterate across itself.

__next__():
This method returns the next item in the hash map, based on the current location of the
iterator.
