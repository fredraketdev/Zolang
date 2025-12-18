- [CHANGELOG](CHANGELOG.md)
- [LICENSE](LICENSE.md)


**Table of contents**
- [Introduction](#introduction)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [How to run your code](#how-to-run-your-code)
  - [Hello World Example](#hello-world-example)
- [Syntax Overview](#syntax-overview)
  - [IMPORTANT! Overall code](#important-overall-code)
  - [Variables](#variables)
  - [Operators](#operators)
  - [Input](#input)
  - [Control Flow](#control-flow)
    - [Conditionals](#conditionals)
    - [Loops](#loops)
- [Custom Features](#custom-features)
- [Examples](#examples)

---

# Introduction
> This language currently has the simple functions like + and - find out how to use them in this documentation! More functions are comming!

# Getting Started
## Installation

- **Command panel version**
  - Download the command panel version
  - To run your code just run the script and type in the command panel.
  - **Only one line of code may be entered at a time.**

        verander x naar 10 // it will save 10 as x

        if x gelijk 10 dan { // wouldn't work and give an error
          toon "x is " plus x 
        }

        if x gelijk 10 dan { toon "x is " plus x } // would work


- **Text editor version**
  - Dowload the Text editor version.
  - To run your code just write it at the bottom of the file and run the script.

## How to run your code

1. Open own_lang.py in a text edditor
1. Replace the program_code string to your code
1. Run own_lang.py

## Hello World Example

### A simple example to get started:
    """toon "hello world" """

# Syntax Overview

### IMPORTANT! Overall code

- The code has to be inbetween quotes:

      """YOUR CODE HERE"""

- To use strings put the text that you want as a string between quotes:

        """ "YOUR TEXT HERE" """

- Variables can not start with numbers or _:

      """verander h_1 naar 10""" // h_1 will be 10
      """verander 1h naar 10""" // This will bring up errors because the variable number starts with a number
      """verander _hl naar 10""" // This will bring up errors because the variable name starts with a '_'

- comments start with // and go to the end of the line, no exceptions:

      """toon "look // this isn't a comment"""" // This would print "look ".
      """ton "look there is no comment here" // but this is a comment""" # this would print 'look there is no comment here'
      and ignore '// but this is a comment'.

## Variables

- Declare variables by using verander (variable name) naar (varriable vallue)
  Example:

      """verander x naar 10""" // The varriable x is now 10
      """verander x naar "hello""" // The varriable x is now "hello"

## Operators
- Arithmetic: plus, min, maal, gedeeld
  Example:

      """verander result naar (5 plus 3) maal 2""" // This will be 16
      """verander result naar "hello " plus 3""" // This will be "hello 3"
      """verander result naar "hello " plus "world"""" // This will be "hello world"

## Input
- vraag is always followed by a prompt
  example

      """verander user_input naar vraag "What is your name?" """ // This works beacause the prompt is 'What is your name?'
      """verander question naar vraag "" """" // Even if you have no prompt you need to type "" else there will be a crash.
      """verander x naar vraag """ // This does not work because there is no prompt.


## Control Flow

### Conditionals
- Syntax for als ... dan, anders.
  Example:

      """verander leeftijd naar 10
      als leeftijd gelijk 10 dan {
      toon "jij bent " plus leeftijd plus " jaar"
      }
      als leeftijd groter 10 dan {
      toon "jij bent ouder dan 10 jaar"
      }
      anders {
      toon "jij bent jonger dan 10 jaar"
      }"""

### Loops

- Supported zolang (while loop).
  Example:

      """verander i naar 0
      zolang i kleiner 5 dan {
        toon i
      }"""


## Custom Features
- Translate easter eggs.
  - `toon.translate`

## Examples
- Basic examples:

      """verander greetings naar "hello " // sets the variable to hello
      verander moregreetings naar greetings maal 3 // sets the variable to hello hello
      toon moregreetings""" // this will show "hello hello hello"

- Nested if statement:

      """verander leeftijd naar 16
      verander heeft_rijbewijs naar "nee"

      als leeftijd groter 17 dan {
      als heeft_rijbewijs gelijk "ja" dan {
        toon "Je mag autorijden!"
      } anders {
        toon "Je bent oud genoeg, maar hebt nog geen rijbewijs."
      }
      } anders {
        toon "Je bent nog te jong."
      }"""


  **⚠️ This is an experimental programming language.
  Expect bugs and rough edges.**
