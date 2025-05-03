# Data Types in Go

## Simple Data Types

- String
- Numeric - Integers, Floats, Complex Numbers
- Boolean
- Error

## Aggregate Data Types

- Arrays

  - An array is a fixed sized collection of data elements that all have the same type.
  - For example:

    ```go
    var arr1 [3]int // Declare an array of 3 integers
    arr1[0] = 1     // Assign the value 1 to the first element
    arr1[1] = 2     // Assign the value 2 to the second element
    arr1[2] = 3     // Assign the value 3 to the third element
    fmt.Println(arr1) // Output: [1 2 3]
    fmt.Println(len(arr1)) // Output: 3

    // assigning arrays to another array
    var arr2 [3]int = arr1 // copies the values of arr1 to arr2
    fmt.Println(arr2) // Output: [1 2 3]

    // when passed to a function, an array is passed by value
    func modifyArray(arr [3]int) {
      arr[0] = 100
    }
    modifyArray(arr1)
    fmt.Println(arr1) // Output: [1 2 3]

    ```

- Slices

  - A slice is a dynamically-sized(can grow and shrink) collection of data elements of the same type.
  - Slices are declared like arrays, but without a size.
  - For example:

    ```go
    var sl1 []int // Declare a slice of integers
    sl1 = []int{1, 2, 3} // Assign the values 1, 2, 3 to the slice
    fmt.Println(sl1) // Output: [1 2 3]
    fmt.Println(len(sl1)) // Output: 3

    // assigning slices to another slice
    sl2 := sl1 // copies the values of sl1 to sl2

    // when passed to a function, a slice is passed by reference
    func modifySlice(slice []int) {
      slice[0] = 100
    }
    modifySlice(sl1)
    fmt.Println(sl1) // Output: [100 2 3]

    ```

- Maps

  - A map is an unordered collection of key-value pairs.
  - For example:

    ```go
    var m1 map[string]int // Declare a map of strings to integers
    m1 = map[string]int{"key1": 1, "key2": 2, "key3": 3} // Assign the values 1, 2, 3 to the map
    fmt.Println(m1) // Output: map[key1:1 key2:2 key3:3]

    fmt.Println(m1["key1"]) // Output: 1

    // adding a new key-value pair to the map
    m1["key4"] = 4
    fmt.Println(m1) // Output: map[key1:1 key2:2 key3:3 key4:4]

    // deleting a key-value pair from the map
    delete(m1, "key1")
    fmt.Println(m1) // Output: map[key2:2 key3:3 key4:4]

    // when passed to a function, a map is passed by reference
    func modifyMap(m map[string]int) {
      m["key1"] = 100
    }
    modifyMap(m1)
    ```

- Structs

  - A struct is an aggregate data type that groups together zero or more values of different types.
  - For example:

    ```go
    var st struct { // declare a anonymous struct
      Name string
      Age int
    }
    st.Name = "John"
    st.Age = 20
    fmt.Println(st) // Output: {John 20}

    // Better create a type for the struct
    type Person struct {
      Name string
      Age int
    }
    var p Person
    p.Name = "John"
    p.Age = 20
    fmt.Println(p) // Output: {John 20}

    // When passed to a function, a struct is passed by value
    func modifyStruct(p Person) {
      p.Name = "Jane"
    }
    modifyStruct(p)
    fmt.Println(p) // Output: {John 20}

    ```
