from typing import Optional, Literal, List, Any, AnyStr


def categorize_contents(
        contents: List[str], 
        identifiers: Optional[List[str]] = None

    ) -> List[List[str]]:
    """
    Categorize a list of contents by assigning an identifier to each content item.
    
    Args:
        contents (List[str]): A list of strings representing the content to be categorized.
        identifiers (Optional[List[str]]): A list of strings representing identifiers for each content item.
                                           If not provided, identifiers will be generated as incremental numbers
                                           starting from 1.
    
    Returns:
        List[List[str]]: A list of lists, where each inner list contains an identifier and the corresponding content.
                        The format is [[identifier1, content1], [identifier2, content2], ...].
    """

    # If 'identifiers' isn't provided.
    if not identifiers:

        identifiers = []
        for n in range(1, len(contents) + 1):
            # Assign default 'identifiers' based on the indices of 'contents', starting from 1
            identifiers.append(str(n))
        

    # Initialize an empty list to store the categorized contents.
    categorized_contents: List = []
    for i, content in enumerate(contents): 

        # Append a list containing the identifier and the content.
        categorized_contents.append([identifiers[i], str(content)])


    return categorized_contents 


def match_parity(
        *,
        value: int, 
        target_parity: Literal["even", "odd"],
        decrease: Optional[bool] = False,
    ) -> int:
    """
    Adjusts an integer to match a specified parity (even or odd).

    Parameters:
    value (int): The integer value to be adjusted.
    target_parity (Literal["even", "odd"]): The desired parity of the result.
    decrease (Optional[bool]): If True and adjustment is needed, decrease the value by 1 
                               to achieve the desired parity. If False or not specified, 
                               increase the value by 1 to achieve the desired parity.

    Returns:
    int: The adjusted integer with the specified parity.
    """

    # Determine the current parity of 'value'.
    current_parity = "even" if value % 2 == 0 else "odd"

    # If the current parity does not match the target parity, adjust the value.
    if current_parity != target_parity:
        if decrease:
            return value - 1  # Decrease the value by 1 to change its parity.
        
        return value + 1  # Increase the value by 1 to change its parity.

    
    return value  # 'value' already has the desired parity.


def assign_distributed_list(value: int, size: int, assign_at_end: bool = False) -> list[int]:

    # If 'value' is to be placed at the last index
    if assign_at_end:
        distributed_list = [0] * size  # Initialize 'distributed_list' with zeros
        distributed_list[-1] = value   # Assign the value to the last index

    # If 'value' is to be distributed evenly across the list
    else:
        distributed_value = value // size  # Calculate the value to be distributed
        distributed_list = [distributed_value] * size  # Assign list with 'distributed_value'

    return distributed_list 