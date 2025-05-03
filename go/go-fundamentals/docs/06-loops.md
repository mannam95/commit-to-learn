# Loops in Go

## Types of loops:

- Infinite loops
- Conditional loops - Loop till a condition is met
- Counter loops - Loop a certain number of times
- Loops with arrays, slices, and maps

### Infinite loops

- An infinite loop is a loop that runs indefinitely because the condition is always true.
- For example:

  ```go
  i := 1
  for {
    // Outputs as long as the loop is running
    // Maybe error will be thrown when we run out of integer range
    fmt.Println(i)
    i += 1
  }
  ```

### Conditional loops

- A conditional loop is a loop that runs until a condition is met.
- For example:

  ```go
  i := 1
  for i <= 10 {
    fmt.Println(i)
    i += 1
  }
  ```

### Counter loops

- A counter loop is a loop that runs a certain number of times.
- For example:

  ```go
  for i := 1; i <= 10; i++ {
    fmt.Println(i)
  }
  ```

### Loops with arrays, slices, and maps

- Loops can be used to iterate over arrays, slices, and maps.
- For example:

  ```go
  arr := []int{1, 2, 3, 4, 5}
  for i, v := range arr {
    fmt.Println(i, v)
  }
  ```
