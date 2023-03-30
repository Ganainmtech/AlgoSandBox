# Imported beaker as bk and pyteal as pt
import beaker as bk
import pyteal as pt

# Creating a class
class MyState:
    # Result variable set equal to global state value is a teal type number
    result = bk.GlobalStateValue(pt.TealType.unit64)

# Creating application from beaker, naming it calculator, assigning it to the app variable
app = bk.Application("Calculator", state = MyState()) # Has access to the class state

# Exposing add method to ABI so front end knows how to call this method
@app.external
# Method to store and take in two arguments(a, b), left is arg right is output
def add(a: pt.abi.Uint64, b: pt.abi.Uint64, *, output: pt.abi.Uint64) -> pt.Expr:
    # Get method used to get the value of arg a and b
    add_result = a.get() + b.get()
    # Creating a Sequence
    return pt.Seq (
        # Setting add_result to the result state in MyClass
        app.state.result.set(add_result),
        # Setting add_result as the output
        output.set(add_result)
    )

@app.external(read_only = True)
# Method to read the state and output a uint64 type
def read_result(*, output: pt.abi.Uint64) -> pt.Expr:
    # Going to return the application state result
    return output.set(app.state.result)
