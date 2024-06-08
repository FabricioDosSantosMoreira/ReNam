from typing import Union


def read_str(*, msg: str) -> Union[str, int]:
    """
    Prompts the user for a string input, ensuring the input is valid and non-empty.

    Args:
        msg (str): The message to display when prompting the user for input.

    Returns: 
        Union[str, int]: The string value if it is valid. 
        -1 if the user interrupts the program or if any other error occurs.
        
    Raises:
        None. All exceptions are handled within the function.
    """
    
    while True:
        
        try:
            value = str(input(msg))

            if not value or value.isspace():
                raise ValueError

            return value

        except ValueError:
            print("\nValueError - - -> Invalid input, string expected. Please, try again.\n")

        except KeyboardInterrupt:
            print("\nKeyboardInterrupt - - -> Program interrupted by user.\n")
            return -1
        
        except Exception as e:
            print(f"\nException - - -> An error occurred: {e}\n")
            return -1


def read_int(*, msg: str) -> Union[str, int]:
    """
    Prompts the user for a integer input, ensuring the input is valid.

    Args:
        msg (str): The message to display when prompting the user for input.

    Returns: 
        Union[str, int]: The integer value if it is valid. 
        -1 if the user interrupts the program or if any other error occurs.
        
    Raises:
        None. All exceptions are handled within the function.
    """

    while True:

        try:
            value = int(input(msg))
            return value

        except ValueError:
            print("\nValueError - - -> Invalid input, integer expected. Please, try again.\n")

        except KeyboardInterrupt:
            print("\nKeyboardInterrupt - - -> Program interrupted by user.\n")
            return -1
        
        except Exception as e:
            print(f"\nException - - -> An error occurred: {e}\n")
            return -1
