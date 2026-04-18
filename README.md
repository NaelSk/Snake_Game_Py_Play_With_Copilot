# Rock-Paper-Scissors Game

A simple command-line implementation of the classic Rock-Paper-Scissors game with comprehensive unit tests.

## Project Structure

```
.
├── game.py                         # Main game logic and implementation
├── test_game.py                    # Comprehensive unit tests (34 tests)
├── test.bat                        # Windows batch file to run tests
├── run.bat                         # Windows batch file to play the game
├── clean.bat                       # Windows batch file to clean cache files
├── Makefile                        # Unix/Linux build automation
├── README.md                       # This file
└── .github/
    └── workflows/
        └── tests.yml               # GitHub Actions CI/CD pipeline
```

## Features

- Play Rock-Paper-Scissors against the computer
- Input validation with error handling
- Play multiple rounds in sequence
- Separated game logic from I/O for testability

## How to Run the Game

### Option 1: Windows Batch File (Easiest)
Double-click **`run.bat`** in the project folder

### Option 2: Command Line
```bash
python game.py
```

Then follow the on-screen prompts:
1. Enter your choice: `rock`, `paper`, or `scissors`
2. The computer makes its choice
3. The result is displayed
4. Choose to play again or exit

## How to Run Tests

### Option 1: Windows Batch File (Recommended for Windows)
Double-click **`test.bat`** in the project folder
- Runs all 34 tests with detailed output
- Shows pass/fail for each test

### Option 2: Command Line
```bash
python -m unittest test_game.py -v
```

### Run specific test class:
```bash
python -m unittest test_game.TestDetermineWinner -v
python -m unittest test_game.TestInputValidation -v
python -m unittest test_game.TestPlayGameIntegration -v
python -m unittest test_game.TestComputerChoice -v
```

### Run specific test method:
```bash
python -m unittest test_game.TestDetermineWinner.test_tie_rock_vs_rock -v
```

### Using VS Code Testing:
1. Open the Test Explorer (left sidebar, flask/beaker icon)
2. Click the run icon next to test names or classes
3. View results in the Test Explorer panel

## Windows Batch Files

Three convenient batch files are included for Windows users:

### `test.bat`
Runs all unit tests with verbose output. Shows each test result and summary.

### `run.bat`
Starts the Rock-Paper-Scissors game. Follow on-screen prompts to play.

### `clean.bat`
Cleans up Python cache files (`__pycache__` directories and `.pyc` files).

**Usage:** Simply double-click any `.bat` file to execute

## Test Coverage

The test suite includes **34 tests** covering all game scenarios:

### TestDetermineWinner (14 tests)
- **Tie scenarios**: Rock vs Rock, Paper vs Paper, Scissors vs Scissors
- **User wins**: Rock beats Scissors, Paper beats Rock, Scissors beats Paper
- **Computer wins**: Scissors loses to Rock, Rock loses to Paper, Paper loses to Scissors
- **Invalid inputs**: Invalid strings, empty strings, uppercase inputs
- **CHOICES validation**: Verifies valid choice options

### TestInputValidation (10 tests)
- **Whitespace handling**: Leading space, trailing space, both sides
- **Case sensitivity**: Uppercase (ROCK), Capitalized (Paper), Mixed case (ScIssoRs)
- **Edge cases**: Numeric strings, special characters, None values, very long strings

### TestPlayGameIntegration (7 tests)
- **Game outcomes**: Tie, user win, computer win
- **Invalid choice handling**: Invalid input rejection
- **Computer choice display**: Verification of output
- **Play again functionality**: Multiple rounds in sequence
- **Goodbye message**: Exit message verification

### TestComputerChoice (1 test)
- **Valid choice validation**: Ensures computer chooses from valid options

## Code Changes

### game.py
- Refactored from inline logic to modular functions
- `determine_winner(user_choice, computer_choice)`: Core game logic function
- `play_game()`: Main game loop with user interaction
- Separated game logic from I/O for better testability

### test_game.py
- Added comprehensive unit test suite
- Uses `unittest` framework with `mock` for I/O testing
- Tests all game scenarios and edge cases
- All 34 tests passing ✅

## Test Results

```
Ran 34 tests in 0.011s

OK
```

All tests pass successfully with full coverage of:
- Game logic and rules
- Input validation
- User interface and feedback
- Game flow and replay functionality

## Game Logic

### Win Conditions
```
Rock beats Scissors
Paper beats Rock
Scissors beats Paper
```

### Return Values from determine_winner()
- `'tie'` - Both players chose the same
- `'user'` - User wins
- `'computer'` - Computer wins
- `None` - Invalid user input

## Requirements

- Python 3.6+
- Built-in libraries only (no external dependencies)

## Automation & CI/CD

### GitHub Actions
Automated tests run on every push and pull request against Python 3.8, 3.9, 3.10, and 3.11.
Configuration: `.github/workflows/tests.yml`

### Windows Batch Files
- `test.bat` - Quick test execution on Windows
- `run.bat` - Easy game launch on Windows
- `clean.bat` - Cache cleanup on Windows

### Makefile (Unix/Linux/Mac)
For non-Windows users, use:
```bash
make test          # Run tests
make run           # Play game
make clean         # Clean cache
make help          # Show all commands
```

### VS Code Tasks
Press `Ctrl+Shift+B` to run tests within VS Code

## Future Enhancements

Possible improvements:
- Statistics tracking (wins, losses, ties)
- Best of N rounds
- Difficulty levels
- GUI interface
