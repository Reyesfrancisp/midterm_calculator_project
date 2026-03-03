"""Facade pattern, REPL, Decorators, and Colorama UI."""
import sys
from colorama import init, Fore, Style
from app.input_validators import validate_number
from app.calculation import OperationFactory
from app.history import HistoryManager, AutoSaveObserver
from app.logger import LoggingObserver
from app.exceptions import CalculatorException

init(autoreset=True)

class CalculatorFacade:
    """Facade to manage the subsystems of the calculator."""
    def __init__(self):
        self.history = HistoryManager()
        self.history.add_observer(AutoSaveObserver())
        self.history.add_observer(LoggingObserver())

    def calculate(self, op_name: str, a_str: str, b_str: str):
        try:
            a = validate_number(a_str)
            b = validate_number(b_str)
            strategy = OperationFactory.get_strategy(op_name)
            result = strategy.execute(a, b)
            self.history.add_record(op_name, a, b, result)
            
            display_result = int(result) if result.is_integer() else result
            print(Fore.GREEN + f"  🟢 Result: {display_result}")
            
        except CalculatorException as e:
            print(Fore.RED + f"  🔴 Error: {e}")
        except Exception as e:
            print(Fore.RED + f"  🔴 Unexpected Error: {e}")

def dynamic_help(func):
    """Decorator Design Pattern: Dynamically generates the help menu."""
    def wrapper(*args, **kwargs):
        available_ops = ", ".join(OperationFactory._operations.keys())
        print(Fore.CYAN + "\n=== HELP MENU ===")
        print(Fore.YELLOW + "📌 Type an operation and two numbers (e.g., 'add 5 10')")
        print(Fore.GREEN + f"📌 Math commands: {available_ops}")
        print(Fore.MAGENTA + "📌 Data commands: history, clear, undo, redo, save, load")
        print(Fore.CYAN + "=================\n")
        return func(*args, **kwargs)
    return wrapper

@dynamic_help
def show_help():
    pass

def repl():
    """Starts the REPL session."""
    calc = CalculatorFacade()
    
    print(Fore.CYAN + "\n" + "="*45)
    print(Fore.WHITE + Style.BRIGHT + " 🚀  ENHANCED PROFESSIONAL CALCULATOR")
    print(Fore.CYAN + "="*45)
    print(Fore.YELLOW + " Type 'help' for commands or 'exit' to quit.")
    print(Fore.CYAN + "-" * 45)

    while True:
        try:
            user_input = input(Fore.BLUE + "\n[Calculator] ➜ " + Style.RESET_ALL).strip().lower()
        except EOFError:
            break

        if not user_input:
            continue

        parts = user_input.split()
        command = parts[0]

        if command == 'exit':
            print(Fore.YELLOW + "  👋 Goodbye!\n")
            break
        elif command == 'help':
            show_help()
        elif command == 'history':
            calc.history.display()
        elif command == 'clear':
            calc.history.clear()
            print(Fore.YELLOW + "  🧹 History cleared.")
        elif command == 'undo':
            if calc.history.undo():
                print(Fore.YELLOW + "  ⏪ [Undo] Reverted to previous state.")
            else:
                print(Fore.RED + "  ⚠️  [Undo] Cannot undo. You are at the beginning of your history.")
        elif command == 'redo':
            if calc.history.redo():
                print(Fore.YELLOW + "  ⏩ [Redo] Restored state.")
            else:
                print(Fore.RED + "  ⚠️  [Redo] Cannot redo. You are at the latest state.")
        elif command == 'save':
            if calc.history.save_history():
                print(Fore.GREEN + "  💾 History manually saved to CSV.")
            else:
                print(Fore.RED + "  🔴 Error saving history.")
        elif command == 'load':
            if calc.history.load_history():
                print(Fore.GREEN + "  📂 History manually loaded from CSV.")
            else:
                print(Fore.RED + "  ⚠️  No existing history found to load.")
        elif command in OperationFactory._operations.keys():
            if len(parts) == 3:
                calc.calculate(command, parts[1], parts[2])
            elif len(parts) == 1:
                a = input("    ↳ Enter first number: ")
                b = input("    ↳ Enter second number: ")
                calc.calculate(command, a, b)
            else:
                print(Fore.RED + "  ⚠️  Usage: <operation> <x> <y>")
        else:
            print(Fore.RED + f"  ❓ Unknown command '{command}'. Type 'help' for options.")