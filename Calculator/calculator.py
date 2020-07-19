from tkinter import *
import math  # need to import this for my eval function to work.


class CalculatorFunctions:
    """
    I think this function could be optimised more, just need to figure it out. Working on other projects though so
    I don't think it will happen soon. Also, hi!
    """
    def eval(self, expression):
        """ given an expression, this function will calculate its value and return the value """

        """
        error message to be displayed on failure. Easier to define it here and use this than have this block of
        text each time i need to use it
        """
        err_msg = "ERROR. Please ensure that the expression"\
                  "you entered is valid. See the readme \n"\
                  "file to check which functions are \n" \
                  "supported."

        # In the readme, it says that this is case insensitive, this line does that
        expression = expression.lower()

        # replacing brackets so any kind can be used
        expression = expression.replace("{", "(")
        expression = expression.replace("}", ")")
        expression = expression.replace("[", "(")
        expression = expression.replace("]", ")")

        """ checking for inequality is fine, just need = to be == for equality comparison to work """
        expression = expression.replace("=", "==")

        # special cases
        if expression == "k":
            # for some reason expression = k returns ^, but we want it to return an error message instead
            return err_msg
        if expression == "":
            return "Please enter an expression"

        function_dict = {"^": "**", "sin": "math.sin", "cos": "math.cos", "tan": "math.tan", "asin": "math.asin",
                         "acos": "math.acos", "atan": "math.atan", "exp": "math.exp", "ln": "math.log"}
        constant_dict = {"e": "math.e", "pi": "math.pi"}
        # go through the expression and find +,-,*,/,^,(,); and see if expression between them operators is valid
        exempt_chars = "1234567890.+-*/()"
        new_expression = ""
        fn_str = ""
        for i in expression:
            if i in exempt_chars:
                if fn_str in function_dict:
                    new_expression += function_dict[fn_str]
                    fn_str = ""
                new_expression += i
            else:
                fn_str += i
            """ 
            normally two consecutive functions are separated by parentheses, but for power there are no separators
            so we need to check specifically for one char operators which need replacing
            """
            if fn_str == "^":
                new_expression += "**"
                fn_str = ""
            # checking for constants like pi or e
            if fn_str in constant_dict:
                new_expression += constant_dict[fn_str]
                fn_str = ""

        try:
            return str(eval(new_expression))
        except:
            """ just to catch any error which happens, need to make this more specific so I can give better information
             to the user so they can fix the error easier """
            return err_msg


class CalculatorWindow:
    def __init__(self):
        # setting up the window
        self.app = Tk()
        # self.app.geometry("256x256")  # make a 256 px^2 box
        self.app.geometry()  # wraps edges to be adjacent to furthest out widget
        self.app.wm_title("Calculator")  # Want the window title to be "Calculator"

        """ 
        I want the answer box cover entire width ofthe bottom of the  window, with entry box and keypad on top, so 
        these 2 windows will handle that.
        The following are instance attributes as well as widgets. PEP8 says to define instance attributes in ctor, and 
        tkinter requires definition at declaration, so these are not initialised in widget_init()
        """
        self.top_frame = Frame(self.app)
        self.bottom_frame = Frame(self.app)

        # frames to store widgets
        self.buttons_frame = Frame(self.top_frame)  # for fn buttons and 0-9 buttons
        self.box_frame = Frame(self.top_frame)  # for answerbox, entry box and calculate button

        # should define instance attributes in constructor, per PEP8
        self.entry = Entry(self.box_frame, width=28)
        self.answerbox = Text(self.bottom_frame, width=40, height=6)  # put answers and error messages in here
        self.calculator = CalculatorFunctions()

        # call functions which initialise the widgets
        self.widget_init()

    def widget_init(self):
        """ initialises all of the widgets in the calculator"""
        self.box_frame.grid(row=0, column=0)
        self.buttons_frame.grid(row=0, column=1)
        self.top_frame.grid(row=0, column=0)
        self.bottom_frame.grid(row=1, column=0)

        # Entry box. To enter expressions into
        self.entry.grid(row=0, column=0)

        # Text box for answers. Can type in here, so should change that.
        self.answerbox.pack()

        # Numbers and decimal point
        (Button(self.buttons_frame, text="0", command=lambda: self.btnclick(0), height=1, width=1)).grid(row=3, column=1)
        (Button(self.buttons_frame, text="1", command=lambda: self.btnclick(1), height=1, width=1)).grid(row=0, column=0)
        (Button(self.buttons_frame, text="2", command=lambda: self.btnclick(2), height=1, width=1)).grid(row=0, column=1)
        (Button(self.buttons_frame, text="3", command=lambda: self.btnclick(3), height=1, width=1)).grid(row=0, column=2)
        (Button(self.buttons_frame, text="4", command=lambda: self.btnclick(4), height=1, width=1)).grid(row=1, column=0)
        (Button(self.buttons_frame, text="5", command=lambda: self.btnclick(5), height=1, width=1)).grid(row=1, column=1)
        (Button(self.buttons_frame, text="6", command=lambda: self.btnclick(6), height=1, width=1)).grid(row=1, column=2)
        (Button(self.buttons_frame, text="7", command=lambda: self.btnclick(7), height=1, width=1)).grid(row=2, column=0)
        (Button(self.buttons_frame, text="8", command=lambda: self.btnclick(8), height=1, width=1)).grid(row=2, column=1)
        (Button(self.buttons_frame, text="9", command=lambda: self.btnclick(9), height=1, width=1)).grid(row=2, column=2)
        (Button(self.buttons_frame, text=".", command=lambda: self.btnclick("."), height=1, width=1)).grid(row=3,column=2)

        # Operators
        (Button(self.buttons_frame, text="+", command=lambda: self.btnclick("+"), height=1, width=1)).grid(row=0, column=4)
        (Button(self.buttons_frame, text="-", command=lambda: self.btnclick("-"), height=1, width=1)).grid(row=1, column=4)
        (Button(self.buttons_frame, text="*", command=lambda: self.btnclick("*"), height=1, width=1)).grid(row=2, column=4)
        (Button(self.buttons_frame, text="/", command=lambda: self.btnclick("/"), height=1, width=1)).grid(row=3, column=4)

        # Backspace and Clear
        (Button(self.buttons_frame, text="Backspace", command=lambda: self.btnclick("Backspace"))).grid(row=0, column=5)
        (Button(self.buttons_frame, text="Clear", command=lambda: self.btnclick("Clear"))).grid(row=1, column=5)

        # Calculate. Evaluates the expression
        (Button(self.box_frame, text="Calculate!", command=lambda: self.btnclick("Calculate"))).grid(row=1, column=0)

    def btnclick(self, a):
        """
        When a button is clicked, this function will do one of the following:
        if button is for a number or operator: add number or operator to entry box
        if button is backspace: delete last character of entry box
        if button is clear: clear entry box
        if button is calculate: calculate answer and print it into answerbox
        """

        special_buttons = {"Calculate", "Backspace", "Clear"}
        """ since these buttons require special processing, as opposed to checking if a button is not calculate and so 
        on just check that the button is not in this list """

        # if button pressed is operator or number, add it to text box
        if a not in special_buttons:
            self.entry.insert(END, "{}".format(a))  # put the character into the text box at the end
        else:
            if a == "Calculate":  # get text and calculate it then return it
                expr = self.entry.get()  # get text from entry box as string
                # process it, eval(expr_str)
                self.answerbox.delete("1.0", END)  # clear the answerbox
                self.answerbox.insert("1.0", "{}".format(self.calculator.eval(expr)))  # put answer into answer box
            elif a == "Clear":  # clear the entry box (make it = "")
                self.entry.delete(0, END)  # delete everything in the text box
            else:  # if they press backspace button (the one in the app not on the keyboard)
                self.entry.delete(len(self.entry.get())-1, END)  # only get rid of last character


calc = CalculatorWindow()
# make it so that pressing enter will calculate the function
calc.app.bind("<Return>", lambda x: calc.btnclick("Calculate"))
calc.app.mainloop()
