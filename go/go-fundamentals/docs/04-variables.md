# Variables in Go

- Variables are used to store values in a program.
- They can be of different types, as we saw in the previous section.

## Strongly typed

- In go all variables are _strongly typed_.

  - A language that does not allow implicit type conversion is called _strongly typed_.
    - For example, see below:
      ```go
      var a int = 10
      var b float64 = 20.5
      var c int = a + b // This will not work because a and b are of different types.
      ```
  - Type conversions possible in Go are explicit.

    - For example, see below:

      ```go
      var a int = 10
      var b float64 = 20.5
      var c int = a + int(b) // This will work because we are converting b to an int.
      ```

  - One of Go's principles is to be clear than clever.
    - Intent is never have Go make an assumption that might go wrong.
    - This is why Go is not a dynamically typed language.

## Static typing

- In go all variables are _statically typed_.

  - When you write code in Go, you're telling the compiler:
    - "Hey, this variable is always going to hold a number (or a string, or a boolean, etc.)."
    - The compiler checks your types before the program runs, and if there's a mismatch, it throws an error.

## Declaration

- Variables are declared using the `var` keyword.
- For example, see below:
  ```go
  var a int  // declaration
  var a int = 10 // declaration and initialization
  ```
- The type of the variable can also be inferred from the value assigned to it.
- For example, see below:
  ```go
  var a = 10 // initialization with type inference
  a := 10 // short declaration
  ```
