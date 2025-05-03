# Pointers in Go

- Pointers are a way to access and manipulate memory addresses in Go.
- They are a type of variable that holds the memory address of another variable.
- They are declared using the `*` symbol and assigned using the `&` symbol.
- For example, see below:
  ```go
  var a int = 10
  var b *int = &a // b is a pointer to a, b holds the memory address of a
  c := &a // c is a pointer to a, c holds the memory address of a
  fmt.Println(b) // prints the memory address of a
  fmt.Println(*c) // prints the value of a
  ```
- Pointers are used to share memory addresses between variables.
- Values are used to copy memory in Go or isolate our programs.
- For example, see below:
  ```go
  var a int = 10
  var b int = a // b is a copy of a
  ```

## Takeaways

- Pointers are used to share memory addresses between variables.
- Use copies whenever possible.
  - Why?
    - Imagine the Go app is running in highly concurrent environment.
    - Anytime we are sharing memory in a high-performance environment.
    - We will run into something called a race condition.
    - Race conditions are when two processes are trying to access the same memory at the same time.
    - This can cause the program to crash or behave unpredictably or in other words we create bugs
    - By using copies, we can avoid this race condition.
