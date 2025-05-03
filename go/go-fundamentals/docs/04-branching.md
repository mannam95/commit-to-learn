# Branching

## Types

    - If statements
    - Switch statements
    - Deferred functions
    - Panic and recover
    - Goto statements

### If statements

- If statements are used to execute code based on a condition.
- For example:

```go
if age >= 18 {
    fmt.Println("You are an adult")
}
else if age >= 13 {
    fmt.Println("You are a teenager")
}
else {
    fmt.Println("You are a child")
}
```

### Switch statements

- Switch statements can be considered as specialized form of if statements.
- For example:

```go
switch age {
    case 18:
        fmt.Println("You are an adult")
    case 13:
        fmt.Println("You are a teenager")
    default:
        fmt.Println("You are a child")
}
```

- A logical switch statement looks like this:

```go
switch age {
    case age >= 18:
        fmt.Println("You are an adult")
    case age >= 13:
        fmt.Println("You are a teenager")
    default:
        fmt.Println("You are a child")
}
```

### Deferred functions

- Deferred functions are functions that are called when the function returns.
- The flow will look like this:

  - Invocation -> Execute statements -> Exit -> Execute deferred statements -> return focus to the caller
  - For example:

    ```go
    func main() {
        fmt.Println("main 1")
        defer fmt.Println("defer 1")
        fmt.Println("main 2")
        defer fmt.Println("defer 2")
    }

    // Outputs:
    // main 1
    // main 2
    // defer 2
    // defer 1
    ```

- Deferred functions are executed in LIFO (Last In First Out) or FILO (First In Last Out) order.
- For example:

```go
// real world example
func main() {
    db, _ := sql.Open("mysql", "user:password@tcp(127.0.0.1:3306)/mydb")
    defer db.Close()
    rows, _ := db.Query("SELECT * FROM users")
    defer rows.Close()

    // Now because of LIFO
    // The deferred rows.Close() will be executed after the rows,
    // Finally the deferred db.Close() will be executed
    // This is useful to ensure that the resources are released in the correct order
}
```

### Panic and recover

- Panic is a built-in function that stops the normal execution of a function and starts panicking.
- For example:

```go
//func1
func func1() {
    // do your things
    func2()
    // do your things
}

//func2
func func2() {
    // do your things
    panic("Something went wrong") // This is panic
    // do your things
}

// Now because of panic in func2, Go will recognize this as the executing environment is unstable, so Go destroys func2
// Because of this, func1 is also destroyed (No recovery option is present in func1)

```

- Recover is a built-in function that stops the panicking sequence and returns the focus to the caller of the function.
- For example:

```go
//func1
func func1() {
    // do your things
    func2()
    // do your things
}

//func2
func func2() {
    defer func() {
        // this is the recovery function from panic
    }()
    // do your things
    panic("Something went wrong")
    // do your things
}

// Now no matter what when exiting func2, the recovery function will be executed
// This is useful to ensure that the program does not crash
```

### Goto statements

- It is very likely you will never use `goto` statements in your Go programming.
- Goto statements are used to jump to a specific label in the code.
- For example:

```go
func main() {
	for i := 0; i < 10; i++ {
		fmt.Println(i)
		if i == 5 {
			goto myLabel
		}
	}

myLabel:
	fmt.Println("Hello")
}
```
