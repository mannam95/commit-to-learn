# Constants in Go

- On the surface, constants are similar to variables.
- One of the main differences is that constants cannot be changed.
- Constants are declared using the `const` keyword.
- They can be character, string, boolean, or numeric values.
- Constants cannot be declared using the `:=` syntax.

```go
// single constant
const PI = 3.14
// multiple or grouped constants
const (
    A = 1
    B = 2
)
// constant expression (must be calculable at compile time)
const c = 1 + 2
// Cannot assign a function call to a constant
const d = someFunction() // This will not work
```

- iota is a special constant that can be used to generate a sequence of constants.
- It is a predefined constant that starts at 0 and increments by 1 for each constant.
- It is typically used in grouped constants.
- For example, see below:
  ```go
  // maybe here it is not clear what iota is doing
  // but it is used to generate a sequence of constants
  const (
    a = iota // 0
    b = iota // 1
    c = iota // 2
    d = 3 * iota // 9 (3 * 3)
  )
  ```
  - iota resets to 0 with each new grouped constant declaration and it resets to 0 at the first line of the grouped constants.
  - For example, see below:
    ```go
    const (
      a = 2*5
      b = 3*5
      c = 4*5
      d = iota // 3
    )
    ```
  - iota combined with constant expressions allows you to establish complex relationships/patterns between constants.
    - for example imagine a grouped constant expression which holds the memory size in KB, MB, GB, etc.
