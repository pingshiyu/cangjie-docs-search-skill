# ArkTS Third-Party Module Generation Rules for Cangjie Glue Code

## Top-Level Declarations

| .d.ts    | Supported Scope                                              | Specifications                                               |
| -------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Namespace | None                                                         | Not supported                                               |
| Global Functions | Supports overloading, supports generic functions             |                                                              |
| Global Variables | Requires manual modification to correct initialization values | Does not support generic type global variables              |
| Interfaces | Supports basic type interfaces, optional properties, readonly properties, member functions, generics, function overloading, array types, inheritance, nested objects | Does not support index signatures, dynamic properties, function types, constructors, declaration merging |
| Type Aliases | Supports enum type aliases, class type aliases, function type aliases, union type aliases | Does not support object literal type aliases, type aliases within namespaces, intersection type aliases, generic type aliases |
| Classes | Supports constructors, static members, private members, protected members, private properties, generic members, abstract classes, class implementing interfaces, class inheritance, overloaded methods | Does not support decorated classes, types with namespaces   |
| Enums | Supports string enums, numeric enums, const enums, heterogeneous enums | Does not support computed value enums. In heterogeneous enums, enum values will be uniformly converted to string type, requiring manual conversion during usage |
| Imports | Supported                                                    |                                                              |
| Exports | None                                                         | Not supported                                               |

### Namespace

Currently not supported

### Global Functions

- Supports overloading.
- Parameter and return value types supported: basic types, function types, tuple types, optional types, generic functions.
- Union types (parameters of union type will be mapped to multiple type overloads).

Example:

.d.ts code:

```typescript
declare function greeter(fn: (a: string) => void): void;
declare function printToConsole(s: string): void;
```

Generated Cangjie code:

```cangjie
import ohos.ark_interop.*
import ohos.ark_interop_helper.*
import ohos.base.*

/***********METHOD***********/
/**
* @brief greeter(fn: (a: string) => void): void
*/
public func greeter(fn: (a: String) -> Unit): Unit {
    hmsGlobalApiCall < Unit >( "_ark_interop_api", "greeter", { ctx =>[ctx.function({ ctx, info =>
            let p0 = String.fromJSValue(ctx, info[0])
            fn(p0)
            ctx.undefined().toJSValue()
        }).toJSValue()] })
}

/**
* @brief printToConsole(s: string): void
*/
public func printToConsole(s: String): Unit {
    hmsGlobalApiCall < Unit >( "_ark_interop_api", "printToConsole", { ctx =>[s.toJSValue(ctx)] })
}

```

Generic function example:

.d.ts code:

```typescript
declare function testMultiGenericT<T, M>(t: T, m: M): T;
```

Generated Cangjie code:

```cangjie
/**
  * @brief testMultiGenericT(t: T, m: M): T
  */
public func testMultiGenericT < T, M >(t: T, m: M): T where T <: JSInteropType<T>, M <: JSInteropType<M> {
    hmsGlobalApiCall < T >( "my_module_genericFunction", "testMultiGenericT", { ctx =>[t.toJSValue(ctx), m.toJSValue(ctx)] }) {
        ctx, info => T.fromJSValue(ctx, info)
    }
}

```

### Global Variables

- Since global variable declarations do not include initial values, the generated Cangjie code requires users to complete the initialization values.

Example:

.d.ts code:

```typescript
declare var foo: number;
declare const goo: number;
declare let qoo: number;
```

Generated Cangjie code:

```cangjie
public const foo = !!!!!check in dts!!!!!

public const goo = !!!!!check in dts!!!!!

public const qoo = !!!!!check in dts!!!!!
```

### Interfaces

- Supports basic types, optional properties, readonly properties, member functions, generics, function overloading, array types.
- Does not support index signatures, inheritance, dynamic properties, nested objects, function types, constructors, declaration merging.

#### Basic Types

.d.ts code:

```typescript
interface GreetingSettings {
  greeting: string;
  duration?: number;
  color?: string;
}
```

Generated Cangjie code:

```cangjie
public class GreetingSettings {

    protected GreetingSettings(public var greeting: String,
    public var duration!: Option<Float64> = None,
    public var color!: Option<String> = None) {}


    public func toJSValue(context: JSContext): JSValue {
        let obj = context.object()
        obj["greeting"] = greeting.toJSValue(context)
        if(let Some(v) <- duration) {
            obj["duration"] = v.toJSValue(context)
        }
        if(let Some(v) <- color) {
            obj["color"] = v.toJSValue(context)
        }
        obj.toJSValue()
    }

    public static func fromJSValue (context: JSContext, input: JSValue): GreetingSettings {
        let obj = input.asObject()
        GreetingSettings(
        String.fromJSValue(context, obj["greeting"]),
        duration: if(obj["duration"].isUndefined()) {
            None
        } else {
            Float64.fromJSValue(context, obj["duration"])
        },
        color: if(obj["color"].isUndefined()) {
            None
        } else {
            String.fromJSValue(context, obj["color"])
        }
        )
    }

}
```

#### Optional Properties

.d.ts code:

```typescript
// product.d.ts
interface Product {
  price?: number; // Optional property
}
```

Generated Cangjie code:

```cangjie
public class Product {

    protected Product(public var price!: Option<Float64> = None) {}


    public func toJSValue(context: JSContext): JSValue {
        let obj = context.object()
        if(let Some(v) <- price) {
            obj["price"] = v.toJSValue(context)
        }
        obj.toJSValue()
    }

    public static func fromJSValue (context: JSContext, input: JSValue): Product {
        let obj = input.asObject()
        Product(
        price: if(obj["price"].isUndefined()) {
            None
        } else {
            Float64.fromJSValue(context, obj["price"])
        }
        )
    }

}
```

#### Readonly Properties

.d.ts code:

```typescript
// point.d.ts
interface Point {
  readonly x: number;
  readonly y: number;
}
```

Generated Cangjie code:

```cangjie
public class Point {

    protected Point(public let x: Float64,
    public let y: Float64) {}


    public func toJSValue(context: JSContext): JSValue {
        let obj = context.object()
        obj["x"] = x.toJSValue(context)
        obj["y"] = y.toJSValue(context)
        obj.toJSValue()
    }

    public static func fromJSValue (context: JSContext, input: JSValue): Point {
        let obj = input.asObject()
        Point(
        Float64.fromJSValue(context, obj["x"]),
        Float64.fromJSValue(context, obj["y"])
        )
    }

}
```

#### Function Types

.d.ts code:

```typescript
// callback.d.ts
interface Callback {
  (data: string): void;
}
```

Currently not supported

#### Member Functions

.d.ts code:

```typescript
// person.d.ts
interface Person {
  name: string;
  greet(): string;
}
```

Generated Cangjie code:

```cangjie
public class Person {

    protected Person(let arkts_object: JSObject) {}


    public mut prop name: String {
        get() {
            checkThreadAndCall < String >(getMainContext()) {
                ctx: JSContext => String.fromJSValue(ctx, arkts_object["name"])
            }
        }
        set(v) {
            checkThreadAndCall < Unit >(getMainContext()) {
                ctx: JSContext => arkts_object["name"] = v.toJSValue(ctx)
            }
        }

    }

    /**
    * @brief greet(): String
    */
    public func greet(): String {
        jsObjApiCall < String >( arkts_object, "greet", emptyArg)
    }

    func toJSValue(context: JSContext): JSValue {
        arkts_object.toJSValue()
    }

    static func fromJSValue (context: JSContext, input: JSValue): Person {
        Person(input.asObject())
    }
}
```

#### Function Overloading

.d.ts code:

```typescript
// calculator.d.ts
interface Calculator {
  add(x: number, y: number): number;
  add(x: string, y: string): string;
}
```

Generated Cangjie code:

```cangjie
public class Calculator {

    protected Calculator(let arkts_object: JSObject) {}


    /**
    * @brief add(x: number,y: number): number
    */
    public func add(x: Float64, y: Float64): Float64 {
        jsObjApiCall < Float64 >( arkts_object, "add", { ctx =>[x.toJSValue(ctx), y.toJSValue(ctx)] })
    }
    /**
    * @brief add(x: string,y: string): String
    */
    public func add(x: String, y: String): String {
        jsObjApiCall < String >( arkts_object, "add", { ctx =>[x.toJSValue(ctx), y.toJSValue(ctx)] })
    }

    func toJSValue(context: JSContext): JSValue {
        arkts_object.toJSValue()
    }

    static func fromJSValue (context: JSContext, input: JSValue): Calculator {
        Calculator(input.asObject())
    }
}
```

#### Array Types

.d.ts code:

```typescript
// list.d.ts
interface List {
  items: string[];
  add(item: string): void;
}
```

Generated Cangjie code:

```cangjie
public class List {

    protected List(let arkts_object: JSObject) {}


    public mut prop items: Array<String> {
        get() {
            checkThreadAndCall < Array<String> >(getMainContext()) {
                ctx: JSContext => Array<String>.fromJSValue(ctx, arkts_object["items"])
            }
        }
        set(v) {
            checkThreadAndCall < Unit >(getMainContext()) {
                ctx: JSContext => arkts_object["items"] = v.toJSValue(ctx)
            }
        }

    }

    /**
    * @brief add(item: string): void
    */
    public func add(item: String): Unit {
        jsObjApiCall < Unit >( arkts_object, "add", { ctx =>[item.toJSValue(ctx)] })
    }

    func toJSValue(context: JSContext): JSValue {
        arkts_object.toJSValue()
    }

    static func fromJSValue (context: JSContext, input: JSValue): List {
        List(input.asObject())
    }
}
```

#### Inheritance

.d.ts code:

```typescript
interface A {
    p: number;
}

interface B extends A {
    p1: number
}

interface C {
    f(): void
}

interface D extends C {
}

interface E extends A {
}

interface F extends C {
    g(): void
}
```

Generated Cangjie code:

```cangjie
public open class A {
    
    protected A(public var p: Float64) {}
    
    
    public open func toJSValue(context: JSContext): JSValue {
        let obj = context.object()
        obj["p"] = p.toJSValue(context)
        obj.toJSValue()
    }
    
    public static func fromJSValue(context: JSContext, input: JSValue): A {
        let obj = input.asObject()
        A(
        Float64.fromJSValue(context, obj["p"])
        )
    }
    
}

/*interface B {
    p1: number;
    }*/

public open class B <: A {
    
    protected B(p: Float64,
    public var p1: Float64) { super(p) }
    
    
    public open func toJSValue(context: JSContext): JSValue {
        let obj = context.object()
        obj["p"] = p.toJSValue(context)
        obj["p1"] = p1.toJSValue(context)
        obj.toJSValue()
    }
    
    public static func fromJSValue(context: JSContext, input: JSValue): B {
        let obj = input.asObject()
        B(
        Float64.fromJSValue(context, obj["p"]),
        Float64.fromJSValue(context, obj["p1"])
        )
    }
    
}

/*interface C {
    f(): void
    }*/

public open class C {
    
    protected C(public var arkts_object: JSObject) {}
    
    
    /**
     * @brief f(): void
     */
    public func f(): Unit {
        jsObjApiCall < Unit >( arkts_object, "f", emptyArg)
    }
    
    public open func toJSValue(context: JSContext): JSValue {
        arkts_object.toJSValue()
    }
    
    static func fromJSValue(context: JSContext, input: JSValue): C {
        C(input.asObject())
    }
}

/*interface D {
    }*/

public open class D <: C {
    
    protected D(arkts_object: JSObject) { super(arkts_object) }
    
    
    
    public open func toJSValue(context: JSContext): JSValue {
        arkts_object.toJSValue()
    }
    
    static func fromJSValue(context: JSContext, input: JSValue): D {
        D(input.asObject())
    }
}

/*interface E {
    }*/

public open class E <: A {
    
    protected E(p: Float64) { super(p) }
    
    
    public open func toJSValue(context: JSContext): JSValue {
        let obj = context.object()
        obj["p"] = p.toJSValue(context)
        obj.toJSValue()
    }
    
    public static func fromJSValue(context: JSContext, input: JSValue): E {
        let obj = input.asObject()
        E(
        Float64.fromJSValue(context, obj["p"])
        )
    }
    
}

/*interface F {
    g(): void
    }*/

public open class F <: C {
    
    protected F(arkts_object: JSObject) { super(arkts_object) }
    
    
    /**
     * @brief g(): void
     */
    public func g(): Unit {
        jsObjApiCall < Unit >( arkts_object, "g", emptyArg)
    }
    
    public open func toJSValue(context: JSContext): JSValue {
        arkts_object.toJSValue()
    }
    
    static func fromJSValue(context: JSContext, input: JSValue): F {
        F(input.asObject())
    }
}
```

#### Nested Objects

.d.ts code:

```typescript
// userProfile.d.ts
interface UserProfile {
  id: number;
  name: string;
  address: {
    city: string;
    zipCode: string;
  };
}
```

Generated Cangjie code:

```cangjie

public open class AutoGenType0 {
    
    protected AutoGenType0(public var : String,
    public var : String) {}
    
    
    public open func toJSValue(context: JSContext): JSValue {
        let obj = context.object()
        obj["city"] = .toJSValue(context)
        obj["zipCode"] = .toJSValue(context)
        obj.toJSValue()
    }
    
    public static func fromJSValue(context: JSContext, input: JSValue): AutoGenType0 {
        let obj = input.asObject()
        AutoGenType0(
        String.fromJSValue(context, obj["city"]),
        String.fromJSValue(context, obj["zipCode"])
        )
    }
    
}


public open class UserProfile {
    
    protected UserProfile(public var id: Float64,
    public var name: String,
    public var address: AutoGenType0) {}
    
    
    public open func toJSValue(context: JSContext): JSValue {
        let obj = context.object()
        obj["id"] = id.toJSValue(context)
        obj["name"] = name.toJSValue(context)
        obj["address"] = address.toJSValue(context)
        obj.toJSValue()
    }
    
    public static func fromJSValue(context: JSContext, input: JSValue): UserProfile {
        let obj = input.asObject()
        UserProfile(
        Float64.fromJSValue(context, obj["id"]),
        String.fromJSValue(context, obj["name"]),
        AutoGenType0.fromJSValue(context, obj["address"])
        )
    }
    
}
```

Currently not supported

#### Index Signatures

.d.ts code:

```typescript
// dictionary.d.ts
interface Dictionary {
  [key: string]: string;
}
// Usage
const dict: Dictionary = {
  name: 'Alice',
  job: 'Developer',
};
console.log(dict['name']); // Alice
```

Currently not supported

#### Dynamic Properties

.d.ts code:

```typescript
// config.d.ts
interface Config {
  [key: string]: string | number;
}
```

Currently not supported

#### Constructors

.d.ts code:

```typescript
interface ClockConstructor {
  new (hour: number, minute: number): ClockInterface;
}
```

Currently not supported

### Type Aliases

- Supports enum type aliases, class type aliases, function type aliases, and union type aliases.
- Does not support object literal type aliases, type aliases for types within namespaces, intersection type aliases, or generic type aliases.

#### Object Literal Type Aliases

.d.ts code:

```typescript
  type AppConfig = {
    apiUrl: string;
    timeout: number;
  };

  declare const config: AppConfig;
```

Currently not supported

#### Enum Type Aliases

.d.ts code:

```typescript
declare enum Colors {
  Red = 'RED',
  Green = 'GREEN',
  Blue = 'BLUE',
}

type ColorAlias = Colors;
```

Generated Cangjie code:

```cangjie
public type ColorAlias = Colors
```

#### Class Type Aliases

.d.ts code:

```typescript
  declare class Animal {
    name: string;
    constructor(name: string);
    speak(): void;
  }

  type AnimalAlias = Animal;
```

Generated Cangjie code:

```cangjie
public type AnimalAlias = Animal
```

#### Type Aliases for Types Within Namespaces

.d.ts code:

```typescript
declare namespace Shapes {
  type Circle = { radius: number };
  type Rectangle = { width: number; height: number };
}

type CircleAlias = Shapes.Circle;
type RectangleAlias = Shapes.Rectangle;
```

Currently not supported

#### Function Type Aliases

.d.ts code:

```typescript
type MathOperation = (a: number, b: number) => number;
```

Generated Cangjie code:

```cangjie
public type MathOperation = (a: Float64, b: Float64) -> Float64
```

#### Union Type Aliases

.d.ts code:

```typescript
type GreetingLike = string | number;
```

Generated Cangjie code:

```cangjie
public enum GreetingLike {
    | STRING(String)
    | NUMBER(Float64)

    public func toJSValue(context: JSContext): JSValue {
        match(this) {
            case STRING(x) => context.string(x).toJSValue()
            case NUMBER(x) => context.number(x).toJSValue()
        }
    }
}
```

#### Intersection Type Aliases

.d.ts code:

```typescript
// point.d.ts
interface Point {
  readonly x: number;
  readonly y: number;
}
```

Currently not supported

#### Generic Type Aliases

.d.ts code:

```typescript
// point.d.ts
interface Point {
  readonly x: number;
  readonly y: number;
}
```

Currently not supported

### Classes

- Supports constructors, static members, private members, protected members, private properties, generic members, abstract classes, class implementation of interfaces, class inheritance, and method overloading.
- Does not support index signatures, inheritance, dynamic properties, nested objects, function types, or constructors.

#### Constructors

.d.ts code:

```typescript
declare class Greeter {
  constructor(greeting: string);
  greeting: string;
  showGreeting(): void;
}
```

Generated Cangjie code:

```cangjie
public class Greeter {

    protected Greeter(let arkts_object: JSObject) {}
    /**
    * @brief constructor(greeting: string): void
    */
    public init(greeting: String) {
        arkts_object = checkThreadAndCall < JSObject >(getMainContext()) {
            __ctx =>
            let clazz = __ctx.global["Greeter"].asClass(__ctx)
            clazz.new(greeting.toJSValue(__ctx)).asObject()
        }
    }

    public mut prop greeting: String {
        get() {
            checkThreadAndCall < String >(getMainContext()) {
                ctx: JSContext => String.fromJSValue(ctx, arkts_object["greeting"])
            }
        }
        set(v) {
            checkThreadAndCall < Unit >(getMainContext()) {
                ctx: JSContext => arkts_object["greeting"] = v.toJSValue(ctx)
            }
        }

    }

    /**
    * @brief showGreeting(): void
    */
    public func showGreeting(): Unit {
        jsObjApiCall < Unit >( arkts_object, "showGreeting", emptyArg)
    }

    func toJSValue(context: JSContext): JSValue {
        arkts_object.toJSValue()
    }

    static func fromJSValue (context: JSContext, input: JSValue): Greeter {
        Greeter(input.asObject())
    }
}


```

#### Static Members

.d.ts code:

```typescript
// MathUtils.d.ts
declare class MathUtils {
  // Static property
  static PI: number;
  // Static method
  static square(x: number): number;
}
```

Generated Cangjie code:

```cangjie
public class MathUtils {

    protected MathUtils(let arkts_object: JSObject) {}

    // Static property
    public mut prop PI: Float64 {
        get() {
            checkThreadAndCall < Float64 >(getMainContext()) {
                ctx: JSContext => Float64.fromJSValue(ctx, getClassConstructorObj("test", "MathUtils")["PI"])
            }
        }
        set(v) {
            checkThreadAndCall < Unit >(getMainContext()) {
                ctx: JSContext => getClassConstructorObj("test", "MathUtils")["PI"] = v.toJSValue(ctx)
            }
        }

    }

    /**
    * @brief square(x: number): number
    */
    public static func square(x: Float64): Float64 {
        jsObjApiCall < Float64 >(getClassConstructorObj("test", "MathUtils"),  "square", { ctx =>[x.toJSValue(ctx)] })
    }

    func toJSValue(context: JSContext): JSValue {
        arkts_object.toJSValue()
    }

    static func fromJSValue (context: JSContext, input: JSValue): MathUtils {
        MathUtils(input.asObject())
    }
}
```

#### Private Members

.d.ts code:

```typescript
declare class Person {
    // Private property
    private age: number;

  }
```

Generated Cangjie code:

```cangjie
public class Person {
    // No need to generate private member properties
    protected Person(let arkts_object: JSObject) {}

    func toJSValue(context: JSContext): JSValue {
        arkts_object.toJSValue()
    }

    static func fromJSValue (context: JSContext, input: JSValue): Person {
        Person(input.asObject())
    }
}
```

#### Protected Members

.d.ts code:

```typescript
declare class AnimalProtect {
    // Protected property
    protected name: string;

    // Protected method
    protected makeSound(): void;
}
```

Generated Cangjie code:

```cangjie
public class AnimalProtect {

    protected AnimalProtect(let arkts_object: JSObject) {}

    // Protected property
    public mut prop name: String {
        get() {
            checkThreadAndCall < String >(getMainContext()) {
                ctx: JSContext => String.fromJSValue(ctx, arkts_object["name"])
            }
        }
        set(v) {
            checkThreadAndCall < Unit >(getMainContext()) {
                ctx: JSContext => arkts_object["name"] = v.toJSValue(ctx)
            }
        }

    }

    /**
    * @brief makeSound(): void
    */
    public func makeSound(): Unit {
        jsObjApiCall < Unit >( arkts_object, "makeSound", emptyArg)
    }

    func toJSValue(context: JSContext): JSValue {
        arkts_object.toJSValue()
    }

    static func fromJSValue (context: JSContext, input: JSValue): AnimalProtect {
        AnimalProtect(input.asObject())
    }
}
```

#### Readonly Properties

.d.ts code:

```typescript
declare class Car {
    // Readonly property
    readonly brand: string;
    name: string
  }
```

Generated Cangjie code:

```cangjie
public class Car {

    protected Car(let arkts_object: JSObject) {}

    // Readonly property
    public prop brand: String {
        get() {
            checkThreadAndCall < String >(getMainContext()) {
                ctx: JSContext => String.fromJSValue(ctx, arkts_object["brand"])
            }
        }
    }

    public mut prop name: String {
        get() {
            checkThreadAndCall < String >(getMainContext()) {
                ctx: JSContext => String.fromJSValue(ctx, arkts_object["name"])
            }
        }
        set(v) {
            checkThreadAndCall < Unit >(getMainContext()) {
                ctx: JSContext => arkts_object["name"] = v.toJSValue(ctx)
            }
        }

    }


    func toJSValue(context: JSContext): JSValue {
        arkts_object.toJSValue()
    }

    static func fromJSValue (context: JSContext, input: JSValue): Car {
        Car(input.asObject())
    }
}
```

#### Generic Members

.d.ts code:

```typescript
declare class Box<T> {
    // Property
    value: T;
    // Method
    getValue(): T;
  }
```

Generated Cangjie code:

```cangjie
public class Box<T> {

    protected Box(let arkts_object: JSObject) {}

    // Property
    public mut prop value: T {
        get() {
            checkThreadAndCall < T >(getMainContext()) {
                ctx: JSContext => T.fromJSValue(ctx, arkts_object["value"])
            }
        }
        set(v) {
            checkThreadAndCall < Unit >(getMainContext()) {
                ctx: JSContext => arkts_object["value"] = v.toJSValue(ctx)
            }
        }

    }

    /**
    * @brief getValue(): T
    */
    public func getValue(): T {
        jsObjApiCall < T >( arkts_object, "getValue", emptyArg) {
            ctx, info => T.fromJSValue(ctx, info)
        }
    }

    func toJSValue(context: JSContext): JSValue {
        arkts_object.toJSValue()
    }

    static func fromJSValue <T>(context: JSContext, input: JSValue): Box<T> {
        Box(input.asObject())
    }
}
```

#### Abstract Classes

.d.ts code:

```typescript
declare abstract class Shape {
    // Abstract method
    abstract getArea(): number;
  }
```

Generated Cangjie code:

```cangjie
public open class Shape {

    protected Shape(let arkts_object: JSObject) {}

    /**
    * @brief getArea(): number
    */
    public func getArea(): Float64 {
        jsObjApiCall < Float64 >( arkts_object, "getArea", emptyArg)
    }

    func toJSValue(context: JSContext): JSValue {
        arkts_object.toJSValue()
    }

    static func fromJSValue (context: JSContext, input: JSValue): Shape {
        Shape(input.asObject())
    }
}
```

#### Class Implementation of Interfaces

.d.ts code:

```typescript
interface Drivable {
  start(): void;
  stop(): void;
}

declare class Car implements Drivable {
  start(): void;
  stop(): void;
}
```

Generated Cangjie code:

```cangjie
public class Drivable {

    protected Drivable(let arkts_object: JSObject) {}


    /**
    * @brief start(): void
    */
    public func start(): Unit {
        jsObjApiCall < Unit >( arkts_object, "start", emptyArg)
    }
    /**
    * @brief stop(): void
    */
    public func stop(): Unit {
        jsObjApiCall < Unit >( arkts_object, "stop", emptyArg)
    }

    func toJSValue(context: JSContext): JSValue {
        arkts_object.toJSValue()
    }

    static func fromJSValue (context: JSContext, input: JSValue): Drivable {
        Drivable(input.asObject())
    }
}
public class Car1 <: Drivable {

    protected Car1(arkts_object: JSObject) {}


    /**
    * @brief start(): void
    */
    public func start(): Unit {
        jsObjApiCall < Unit >( arkts_object, "start", emptyArg)
    }
    /**
    * @brief stop(): void
    */
    public func stop(): Unit {
        jsObjApiCall < Unit >( arkts_object, "stop", emptyArg)
    }

    func toJSValue(context: JSContext): JSValue {
        arkts_object.toJSValue()
    }

    static func fromJSValue (context: JSContext, input: JSValue): Car1 {
        Car1(input.asObject())
    }
}
```

#### Class Inheritance

.d.ts code:

```typescript
// Animal.d.ts
declare class Animal {
  name: string;
  constructor(name: string);
  move(distance: number): void;
}

// Dog.d.ts
declare class Dog extends Animal {
  bark(): void;
}
```

Generated Cangjie code:

```cangjie
public class Animal1 {

    protected Animal1(let arkts_object: JSObject) {}
    /**
    * @brief constructor(name: string): void
    */
    public init(name: String) {
        arkts_object = checkThreadAndCall < JSObject >(getMainContext()) {
            __ctx =>
            let module = getJSModule(__ctx, "test", None)
            let clazz = module["Animal1"].asClass(__ctx)
            clazz.new(name.toJSValue(__ctx)).asObject()
        }
    }

    public mut prop name: String {
        get() {
            checkThreadAndCall < String >(getMainContext()) {
                ctx: JSContext => String.fromJSValue(ctx, arkts_object["name"])
            }
        }
        set(v) {
            checkThreadAndCall < Unit >(getMainContext()) {
                ctx: JSContext => arkts_object["name"] = v.toJSValue(ctx)
            }
        }

    }

    /**
    * @brief move(distance: number): void
    */
    public func move(distance: Float64): Unit {
        jsObjApiCall < Unit >( arkts_object, "move", { ctx =>[distance.toJSValue(ctx)] })
    }

    func toJSValue(context: JSContext): JSValue {
        arkts_object.toJSValue()
    }

    static func fromJSValue (context: JSContext, input: JSValue): Animal1 {
        Animal1(input.asObject())
    }
}
public class Dog <: Animal1 {

    protected Dog(arkts_object: JSObject) {}


    /**
    * @brief bark(): void
    */
    public func bark(): Unit {
        jsObjApiCall < Unit >( arkts_object, "bark", emptyArg)
    }

    func toJSValue(context: JSContext): JSValue {
        arkts_object.toJSValue()
    }

    static func fromJSValue (context: JSContext, input: JSValue): Dog {
        Dog(input.asObject())
    }
}
```

#### Method Overloading

.d.ts code:

```typescript
declare class Calculator {
    // Method overloading
    add(x: number, y: number): number;
    add(x: string, y: string): string;

    // Implementation
    add(x: any, y: any): any;
  }
```

Generated Cangjie code:

```cangjie
public class Calculator {

    protected Calculator(let arkts_object: JSObject) {}


    /**
    * @brief add(x: number,y: number): number
    */
    public func add(x: Float64, y: Float64): Float64 {
        jsObjApiCall < Float64 >( arkts_object, "add", { ctx =>[x.toJSValue(ctx), y.toJSValue(ctx)] })
    }
    /**
    * @brief add(x: string,y: string): String
    */
    public func add(x: String, y: String): String {
        jsObjApiCall < String >( arkts_object, "add", { ctx =>[x.toJSValue(ctx), y.toJSValue(ctx)] })
    }
    /**
    * @brief add(x: any,y: any): any
    */
    public func add(x: Any, y: Any): any {
        jsObjApiCall < any >( arkts_object, "add", { ctx =>[x.toJSValue(ctx), y.toJSValue(ctx)] }) {
            ctx, info => any.fromJSValue(ctx, info)
        }
    }

    func toJSValue(context: JSContext): JSValue {
        arkts_object.toJSValue()
    }

    static func fromJSValue (context: JSContext, input: JSValue): Calculator {
        Calculator(input.asObject())
    }
}
```

#### Classes with Decorators

.d.ts code:

```typescript
// LogClass.d.ts
declare function logClass(target: any): void;

@logClass
declare class MyClass {
  name: string;
  constructor(name: string);
}
```

Currently not supported

#### Classes with Namespaces

.d.ts code:

```typescript
// Shapes.d.ts
declare namespace Shapes {
  class Circle1 {
    radius: number;
    constructor(radius: number);
    getArea(): number;
  }
}
```

Currently not supported

### Enumerations

- Supports string enums, numeric enums, const enums, and heterogeneous enums. In Cangjie glue code, all enum values in heterogeneous enums will be converted to string type. Therefore, when developers invoke the glue code, they need to manually convert non-string type enum members (e.g., `number` type) in heterogeneous enums to their original types as defined in ArkTS.
- Computed value enums are not supported.

#### String Enums

.d.ts code:

```typescript
// colors.d.ts
declare enum Colors {
  Red = 'RED',
  Green = 'GREEN',
  Blue = 'BLUE',
}
```

Generated Cangjie code:

```cangjie
public enum Colors <: ToString & Equatable < Colors > {
    | Red
    | Green
    | Blue

    func get(): String {
        match(this) {
            case Red => "RED"
            case Green => "GREEN"
            case Blue => "BLUE"
        }
    }

    static func parse(val: String): Colors {
        match(val) {
            case "RED" => Red
            case "GREEN" => Green
            case "BLUE" => Blue
            case _ => throw IllegalArgumentException("unknown value ${val}")
        }
    }

    static func tryParse(val: ?String): ?Colors {
        match(val) {
            case Some(v) => parse(v)
            case None => None
        }
    }

    public func toString(): String {
        get()
    }

    public override operator func ==(that: Colors): Bool {
        match((this, that)) {
            case(Red, Red) => true
            case(Green, Green) => true
            case(Blue, Blue) => true
            case _ => false
        }
    }

    public override operator func !=(that: Colors): Bool {
        !(this == that)
    }
}
```

#### Numeric Enums

.d.ts code:

```typescript
// status.d.ts
declare enum Status {
  Pending,    // 0
  Approved,   // 1
  Rejected,   // 2
}
```

Generated Cangjie code:

```cangjie
public enum Status <: ToString & Equatable < Status > {
    | Pending
    | Approved
    | Rejected

    func get(): Int32 {
        match(this) {
            case Pending => 0  //todo: please check the value
            case Approved => 1  //todo: please check the value
            case Rejected => 2  //todo: please check the value
        }
    }

    static func parse(val: Int32): Status {
        match(val) {
            case 0 => Pending  //todo: please check the value
            case 1 => Approved  //todo: please check the value
            case 2 => Rejected  //todo: please check the value
            case _ => throw IllegalArgumentException("unknown value ${val}")
        }
    }

    static func tryParse(val: ?Int32): ?Status {
        match(val) {
            case Some(v) => parse(v)
            case None => None
        }
    }

    public func toString(): String {
        match(this) {
            case Pending => "Pending"
            case Approved => "Approved"
            case Rejected => "Rejected"
        }
    }

    public override operator func ==(that: Status): Bool {
        match((this, that)) {
            case(Pending, Pending) => true
            case(Approved, Approved) => true
            case(Rejected, Rejected) => true
            case _ => false
        }
    }

    public override operator func !=(that: Status): Bool {
        !(this == that)
    }
}
```

#### Const Enums

.d.ts code:

```typescript
// constants.d.ts
declare const enum Status {
  Pending = 3,
  Approved = 4,
  Rejected = 5
}
```

Generated Cangjie code:

```cangjie
public enum Status <: ToString & Equatable < Status > {
    | Pending
    | Approved
    | Rejected

    func get(): Int32 {
        match(this) {
            case Pending => 3
            case Approved => 4
            case Rejected => 5
        }
    }

    static func parse(val: Int32): Status {
        match(val) {
            case 3 => Pending
            case 4 => Approved
            case 5 => Rejected
            case _ => throw IllegalArgumentException("unknown value ${val}")
        }
    }

    static func tryParse(val: ?Int32): ?Status {
        match(val) {
            case Some(v) => parse(v)
            case None => None
        }
    }

    public func toString(): String {
        match(this) {
            case Pending => "Pending"
            case Approved => "Approved"
            case Rejected => "Rejected"
        }
    }

    public override operator func ==(that: Status): Bool {
        match((this, that)) {
            case(Pending, Pending) => true
            case(Approved, Approved) => true
            case(Rejected, Rejected) => true
            case _ => false
        }
    }

    public override operator func !=(that: Status): Bool {
        !(this == that)
    }
}
```

#### Heterogeneous Enums

.d.ts code:

```typescript
// response.d.ts
declare enum Response {
  No = 0,
  Yes = 'YES',
}
```

Generated Cangjie code:

```cangjie
public enum Response <: ToString & Equatable < Response > {
    | No
    | Yes

    func get(): String {
        match(this) {
            case No => "0"
            case Yes => "YES"
        }
    }

    static func parse(val: String): Response {
        match(val) {
            case "0" => No
            case "YES" => Yes
            case _ => throw IllegalArgumentException("unknown value ${val}")
        }
    }

    static func tryParse(val: ?String): ?Response {
        match(val) {
            case Some(v) => parse(v)
            case None => None
        }
    }

    public func toString(): String {
        get()
    }

    public override operator func ==(that: Response): Bool {
        match((this, that)) {
            case(No, No) => true
            case(Yes, Yes) => true
            case _ => false
        }
    }

    public override operator func !=(that: Response): Bool {
        !(this == that)
    }
}
```

## Type Mapping Relationships

The conversion of ArkTS `.d.ts` interfaces to interoperable Cangjie code supports the following type conversions: basic types, Array types, function types, Optional types, Object types, tuple types, Union types, and Promise types.

For unsupported types, they will default to the `JSValue` type, accompanied by a `FIXME` comment (containing the original type from the `.d.ts` declaration). A warning message will also be printed in the command line indicating the unsupported type.

- Comment format:

  .d.ts code:

  ```typescript
  type TA80 = undefined;
  ```

  Corresponding Cangjie code:

  ```typescript
  // The corresponding Cangjie code type is JSValue, with a FIXME comment containing the original .d.ts declared type
  public type TA80 = JSValue/* FIXME: `undefined` */
  ```

- Warning message format:

  ```typescript
  WARNING: type is not supported - undefined
  ```

### Basic Types

Supported data types:

| ArkTS Type | Cangjie Type |
| ---------- | ------------ |
| string     | String       |
| number     | Float64      |
| boolean    | bool         |
| bigint     | BigInt       |
| object     | JSValue      |
| symbol     | JSValue      |
| void       | Unit         |
| undefined  | JSValue      |
| any        | Any          |
| unknown    | JSValue      |
| never      | JSValue      |

Example:

.d.ts code:

```typescript
interface BasicTypes {
    numberKeyword: number;
    stringKeyword: string;
    booleanKeyword: boolean;
    bigintKeyword: bigint;
    objectKeyword: object;
    symbolKeyword: symbol;
    voidKeyword: void;
    undefinedKeyword: undefined;
    anyKeyword: any;
    unknownKeyword: unknown;
    neverKeyword: never;
}
```

Generated Cangjie code:

```cangjie
public class BasicTypes {

    protected BasicTypes(public var numberKeyword: Float64,
    public var stringKeyword: String,
    public var booleanKeyword: Bool,
    public var bigintKeyword: BigInt,
    public var objectKeyword: JSValue/* FIXME: `object` */,
    public var symbolKeyword: JSValue/* FIXME: `symbol` */,
    public var voidKeyword: Unit,
    public var undefinedKeyword: JSValue/* FIXME: `undefined` */,
    public var anyKeyword: Any,
    public var unknownKeyword: JSValue/* FIXME: `unknown` */,
    public var neverKeyword: JSValue/* FIXME: `never` */) {}


    public func toJSValue(context: JSContext): JSValue {
        let obj = context.object()
        obj["numberKeyword"] = numberKeyword.toJSValue(context)
        obj["stringKeyword"] = stringKeyword.toJSValue(context)
        obj["booleanKeyword"] = booleanKeyword.toJSValue(context)
        obj["bigintKeyword"] = context.bigint(bigintKeyword).toJSValue(context)
        obj["objectKeyword"] = objectKeyword
        obj["symbolKeyword"] = symbolKeyword
        obj["voidKeyword"] = voidKeyword.toJSValue(context)
        obj["undefinedKeyword"] = undefinedKeyword
        obj["anyKeyword"] = anyKeyword.toJSValue(context)
        obj["unknownKeyword"] = unknownKeyword
        obj["neverKeyword"] = neverKeyword
        obj.toJSValue()
    }

    public static func fromJSValue (context: JSContext, input: JSValue): BasicTypes {
        let obj = input.asObject()
        BasicTypes(
        Float64.fromJSValue(context, obj["numberKeyword"]),
        String.fromJSValue(context, obj["stringKeyword"]),
        Bool.fromJSValue(context, obj["booleanKeyword"]),
        obj["bigintKeyword"].asBigInt(context).toBigInt(),
        JSValue/* FIXME: `object` */.fromJSValue(context, obj["objectKeyword"]),
        JSValue/* FIXME: `symbol` */.fromJSValue(context, obj["symbolKeyword"]),
        Unit.fromJSValue(context, obj["voidKeyword"]),
        JSValue/* FIXME: `undefined` */.fromJSValue(context, obj["undefinedKeyword"]),
        Any.fromJSValue(context, obj["anyKeyword"]),
        JSValue/* FIXME: `unknown` */.fromJSValue(context, obj["unknownKeyword"]),
        JSValue/* FIXME: `never` */.fromJSValue(context, obj["neverKeyword"])
        )
    }

}
```

### Array

Currently supports four types of array conversions:

| ArkTS Type                   | Cangjie Type      |
| ---------------------------- | ----------------- |
| Uint8Array                   | Array\<UInt8>     |
| ArrayBuffer                  | Array\<UInt8>     |
| Float32Array                 | Array\<Float32>   |
| Basic type arrays (e.g., `number[]`) | Array\<Float64>   |

Example:

.d.ts code:

```typescript
interface arrayInterface {
  arrayType1: number[];
  arrayType2: Uint8Array;
  arrayType3: ArrayBuffer;
  arrayType4: Float32Array;
}
```

Generated Cangjie code:

```cangjie
public class arrayInterface {

    protected arrayInterface(public var arrayType1: Array<Float64>,
    public var arrayType2: Array<UInt8>,
    public var arrayType3: Array<UInt8>,
    public var arrayType4: Array<Float32>) {}


    public func toJSValue(context: JSContext): JSValue {
        let obj = context.object()
        obj["arrayType1"] = toJSArray(context, arrayType1)
        obj["arrayType2"] = toJSArray(context, arrayType2, { ctx: JSContext, val: UInt8 => val.toJSValue(ctx) })
        obj["arrayType3"] = toJSArray(context, arrayType3, { ctx: JSContext, val: UInt8 => val.toJSValue(ctx) })
        obj["arrayType4"] = toJSArray(context, arrayType4, { ctx: JSContext, val: Float32 => val.toJSValue(ctx) })
        obj.toJSValue()
    }

    public static func fromJSValue (context: JSContext, input: JSValue): arrayInterface {
        let obj = input.asObject()
        arrayInterface(
        fromJSArray < Float64 >(context, obj["arrayType1"]),
        fromJSArray(context, obj["arrayType2"], { ctx: JSContext, val: JSValue => UInt8.fromJSValue(ctx, val) }),
        fromJSArray(context, obj["arrayType3"], { ctx: JSContext, val: JSValue => UInt8.fromJSValue(ctx, val) }),
        fromJSArray(context, obj["arrayType4"], { ctx: JSContext, val: JSValue => Float32.fromJSValue(ctx, val) })
        )
    }

}
```

### Function Types

- Supports interface properties and function parameters.
- The `Function` type does not support conversion.

#### Interface Properties

Example:

.d.ts code:

```typescript
interface TestListener {
    "onStart"?: () => void;
    "onDestroy"?: () => void;
    onError?: (code: ErrorCode, msg: string) => void;
    onTouch?: () => void;
    onEvent?: (e: EventType) => void;
}
```

Generated Cangjie code:

```cangjie
public class TestListener {

    protected TestListener(public var onStart!: Option<() -> Unit> = None,
    public var onDestroy!: Option<() -> Unit> = None,
    public var onError!: Option<(code: ErrorCode, msg: String) -> Unit> = None,
    public var onTouch!: Option<() -> Unit> = None,
    public var onEvent!: Option<(e: EventType) -> Unit> = None) {}


    public func toJSValue(context: JSContext): JSValue {
        let obj = context.object()
        if(let Some(v) <- onStart) {
            obj["onStart"] = context.function({ ctx, _ =>
                v()
                ctx.undefined().toJSValue()
            }).toJSValue()
        }
        if(let Some(v) <- onDestroy) {
            obj["onDestroy"] = context.function({ ctx, _ =>
                v()
                ctx.undefined().toJSValue()
            }).toJSValue()
        }
        if(let Some(v) <- onError) {
            obj["onError"] = context.function({ ctx, info =>
                let p0 = ErrorCode.fromJSValue(ctx, info[0])
                let p1 = String.fromJSValue(ctx, info[1])
                v(p0, p1)
                ctx.undefined().toJSValue()
            }).toJSValue()
        }
        if(let Some(v) <- onTouch) {
            obj["onTouch"] = context.function({ ctx, _ =>
                v()
                ctx.undefined().toJSValue()
            }).toJSValue()
        }
        if(let Some(v) <- onEvent) {
            obj["onEvent"] = context.function({ ctx, info =>
                let p0 = EventType.parse(Int32.fromJSValue(ctx, info[0]))
                v(p0)
                ctx.undefined().toJSValue()
            }).toJSValue()
        }
        obj.toJSValue()
    }

    public static func fromJSValue (context: JSContext, input: JSValue): TestListener {
        let obj = input.asObject()
        TestListener(
        onStart: if(obj["onStart"].isUndefined()) {
            None
        } else {
            { =>
                checkThreadAndCall < Unit >(context, { _ =>
                    obj["onStart"].asFunction().call()
                })
            }
        },
        onDestroy: if(obj["onDestroy"].isUndefined()) {
            None
        } else {
            { =>
                checkThreadAndCall < Unit >(context, { _ =>
                    obj["onDestroy"].asFunction().call()
                })
            }
        },
        onError: if(obj["onError"].isUndefined()) {
            None
        } else {
            { code: ErrorCode, msg: String =>
                checkThreadAndCall < Unit >(context, { ctx =>
                    let arg0 = code.toJSValue(ctx)
                    let arg1 = msg.toJSValue(ctx)
                    obj["onError"].asFunction().call([arg0, arg1])
                })
            }
        },
        onTouch: if(obj["onTouch"].isUndefined()) {
            None
        } else {
            { =>
                checkThreadAndCall < Unit >(context, { _ =>
                    obj["onTouch"].asFunction().call()
                })
            }
        },
        onEvent: if(obj["onEvent"].isUndefined()) {
            None
        } else {
            { e: EventType =>
                checkThreadAndCall < Unit >(context, { ctx =>
                    let arg0 = e.get().toJSValue(ctx)
                    obj["onEvent"].asFunction().call([arg0])
                })
            }
        }
        )
    }

}
```

#### Function Parameters

Example:

.d.ts code:

```typescript
interface MyListener {
    on(key: string, param: boolean, cb: (r: Record<string, string>) => void);
}
```

Generated Cangjie code:

```cangjie
public class MyListener {
    let callbackManager = CallbackManager < String, JSValue >()
    protected MyListener(let arkts_object: JSObject) {}

    /**
    * @brief on(key: string,param: boolean,cb: (r: Record<string, string>) => void): void
    */
    public func on(key: String, param: Bool, cb: Callback1Argument<Record>): Unit {
        let key = key.toString()
        if(callbackManager.findCallbackObject(key, cb).isSome()) {
            return
        }
        let jsCallback = checkThreadAndCall < JSValue >(getMainContext()) {
            __ctx => __ctx.function {
                __ctx: JSContext, info: JSCallInfo =>
                let arg0 = Record<stringstring>.fromJSValue(__ctx, info[0])
                cb.invoke(arg0)
                __ctx.undefined().toJSValue()
            }.toJSValue()
        }
        callbackManager.put(key,(cb, jsCallback))
        jsObjApiCall < Unit >( arkts_object, "on", { __ctx =>[key.toJSValue(__ctx), param.toJSValue(__ctx), jsCallback] })
    }

    func toJSValue(context: JSContext): JSValue {
        arkts_object.toJSValue()
    }

    static func fromJSValue (context: JSContext, input: JSValue): MyListener {
        MyListener(input.asObject())
    }
}
```

### Optional Types

Example:

.d.ts code:

```typescript
interface Optionals {
    optionalField1?: number;
    optionalParam10: (a: number, b?: string) => void;
}
```

Generated Cangjie code:

```cangjie
public class Optionals {

    protected Optionals(public var optionalParam10: (a: Float64, b: ?String) -> Unit,
    public var optionalField1!: Option<Float64> = None) {}


    public func toJSValue(context: JSContext): JSValue {
        let obj = context.object()
        obj["optionalParam10"] = context.function({ ctx, info =>
            let p0 = Float64.fromJSValue(ctx, info[0])
            let p1 = String.fromJSValue(ctx, info[1])
            optionalParam10(p0, p1)
            ctx.undefined().toJSValue()
        }).toJSValue()
        if(let Some(v) <- optionalField1) {
            obj["optionalField1"] = v.toJSValue(context)
        }
        obj.toJSValue()
    }

    public static func fromJSValue (context: JSContext, input: JSValue): Optionals {
        let obj = input.asObject()
        Optionals(
        { a: Float64, b:?String =>
            checkThreadAndCall < Unit >(context, { ctx =>
                let arg0 = a.toJSValue(ctx)
                let arg1 = b?.toJSValue(ctx)
                obj["optionalParam10"].asFunction().call([arg0, arg1])
            })
        },
        optionalField1: if(obj["optionalField1"].isUndefined()) {
            None
        } else {
            Float64.fromJSValue(context, obj["optionalField1"])
        }
        )
    }

}
```

### Object Types

Example:

.d.ts code:

```typescript
interface ObjectTypes<U, T> {
    typeLiteral10: { x: number; y: U; };
    typeLiteral20: { [p: number]: string; [p: symbol]: T };
    typeLiteral30: { (): void; (number): string };
}
```

Current type is not supported and will be converted to JSValue by default.

Generated Cangjie code:

```cangjie
public class ObjectTypes<U, T> {

    protected ObjectTypes(public var typeLiteral10: JSValue/* FIXME: `{ x: number; y: U }` */,
    public var typeLiteral20: JSValue/* FIXME: `{ [number]: string; [symbol]: T }` */,
    public var typeLiteral30: JSValue/* FIXME: `{ () => void; (number: any) => string }` */) {}


    public func toJSValue(context: JSContext): JSValue {
        let obj = context.object()
        obj["typeLiteral10"] = typeLiteral10
        obj["typeLiteral20"] = typeLiteral20
        obj["typeLiteral30"] = typeLiteral30
        obj.toJSValue()
    }

    public static func fromJSValue <U, T>(context: JSContext, input: JSValue): ObjectTypes<U, T> {
        let obj = input.asObject()
        ObjectTypes(
        JSValue/* FIXME: `{ x: number; y: U }` */.fromJSValue(context, obj["typeLiteral10"]),
        JSValue/* FIXME: `{ [number]: string; [symbol]: T }` */.fromJSValue(context, obj["typeLiteral20"]),
        JSValue/* FIXME: `{ () => void; (number: any) => string }` */.fromJSValue(context, obj["typeLiteral30"])
        )
    }

}
```

### Tuple Types

Example:

.d.ts code:

```typescript
tupleType: [number, number, string];
```

Generated Cangjie code:

```cangjie
public var tupleType: Tuple<Float64, Float64, String>
```

### Union Types

- Currently only supports union types as type aliases and function parameters.

Example:

.d.ts code:

```typescript
type ARK1 = null | number | string | boolean | Uint8Array | Float32Array | bigint;
```

Generated Cangjie code:

```cangjie
public enum ARK1 {
    | NULL
    | NUMBER(Float64)
    | STRING(String)
    | BOOLEAN(Bool)
    | BYTEARRAY(Array<UInt8>)
    | FLOAT32ARRAY(Array<Float32>)
    | BIGINT(BigInt)

    public func toJSValue(context: JSContext): JSValue {
        match(this) {
            case NULL => context.null().toJSValue()
            case NUMBER(x) => context.number(x).toJSValue()
            case STRING(x) => context.string(x).toJSValue()
            case BOOLEAN(x) => context.boolean(x).toJSValue()
            case BYTEARRAY(x) => context.global["Uint8Array"].asClass().new(x.toJSValue(context))
            case FLOAT32ARRAY(x) => let buffer = context.arrayBuffer(acquireArrayRawData(x), x.size, { pt => releaseArrayRawData(pt)})
context.global["Float32Array"].asClass().new(buffer.toJSValue())
            case BIGINT(x) => context.bigint(x).toJSValue()
        }
    }
}

public enum ARK2 {
    | ARK1(x)
    | VOID(Unit)

    public func toJSValue(context: JSContext): JSValue {
        match(this) {
            case ARK1(x) => x.toJSValue(context)
        }
    }
}
```

### Promise Types

.d.ts code:

```typescript
typeReference21: Promise<T>;
```

Generated Cangjie code:

```cangjie
public var typeReference21: Promise<T>,
```

### Intersection Types

.d.ts code:

```typescript
interface IntersectionTypes<U, T> {
  intersectionType: object & Record<U, T>;
}
```

Current type is not supported and will be converted to JSValue by default.

Generated Cangjie code:

```cangjie
public class IntersectionTypes<U, T> {

    protected IntersectionTypes(public var intersectionType: JSValue/* FIXME: `object & HashMap<U, T>` */) {}


    public func toJSValue(context: JSContext): JSValue {
        let obj = context.object()
        obj["intersectionType"] = intersectionType
        obj.toJSValue()
    }

    public static func fromJSValue <U, T>(context: JSContext, input: JSValue): IntersectionTypes<U, T> {
        let obj = input.asObject()
        IntersectionTypes(
        JSValue/* FIXME: `object & HashMap<U, T>` */.fromJSValue(context, obj["intersectionType"])
        )
    }

}
```

### Imports

- Currently imports will be translated, but manual confirmation and modification by users is still required.

.d.ts code:

```typescript
import { a } from '@umeng/common';
import buffer from '@ohos.buffer';
import { e } from "../g/h";

import { MyStringEnum, MyNumericEnum } from './exportAlias'; // Type Imports
declare const value1: MyStringEnum;
declare const value2: MyNumericEnum;

import * as Inheritances from './inheritances'; // Module Import
declare function createSub(): Inheritances.SubClass;

import { ExportedInterface } from './exportAlias'; // Module Augmentation
declare module './exportAlias' {
    interface ExportedInterface {
        myOption?: string;
    }
}
```

Generated Cangjie Code:

```cangjie
/***********IMPORT***********/
/*FIXME: Import details need to be verified and rewritten by user.*/
/*import { a } from '@umeng/common';*/

/*FIXME: Import details need to be verified and rewritten by user.*/
/*import buffer from '@ohos.buffer';*/

/*FIXME: Import details need to be verified and rewritten by user.*/
/*import { e } from "../g/h";*/

/*FIXME: Import details need to be verified and rewritten by user.*/
/*import { MyStringEnum, MyNumericEnum } from './exportAlias';*/

/*FIXME: Import details need to be verified and rewritten by user.*/
/*import * as Inheritances from './inheritances';*/

/*FIXME: Import details need to be verified and rewritten by user.*/
/*import { ExportedInterface } from './exportAlias';*/


/*

public const value1 = 0/* FIXME: Initialization is required */
*/
/*

public const value2 = 0/* FIXME: Initialization is required */
*/

/***********METHOD***********/
/**
  * @brief createSub(): Inheritances.SubClass
  */
public func createSub(): JSValue/* FIXME: `Inheritances.SubClass` */ {
    hmsGlobalApiCall < JSValue/* FIXME: `Inheritances.SubClass` */ >( "my_module_imports", "createSub", emptyArg) {
        ctx, info => info
    }
}


/***********OBJECT***********/

/*interface ExportedInterface {
    myOption?: String;
    }*/

public open class ExportedInterface {
    
    protected ExportedInterface(public var myOption!: Option<String> = None) {}
    
    
    public open func toJSValue(context: JSContext): JSValue {
        let obj = context.object()
        if(let Some(v) <- myOption) {
            obj["myOption"] = v.toJSValue(context)
        }
        obj.toJSValue()
    }
    
    public static func fromJSValue(context: JSContext, input: JSValue): ExportedInterface {
        let obj = input.asObject()
        ExportedInterface(
        myOption: Option < String >.fromJSValue(context, obj["myOption"])
        )
    }
    
}
```