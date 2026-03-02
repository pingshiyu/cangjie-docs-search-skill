# The Unit Type

For expressions that only concern side effects without caring about values, their type is `Unit`. For example, the `print` function, assignment expressions, compound assignment expressions, increment and decrement expressions, and loop expressions all have the `Unit` type.

The `Unit` type has only one value, which is also its literal: `()`. Apart from assignment, equality checks, and inequality checks, the `Unit` type does not support other operations.