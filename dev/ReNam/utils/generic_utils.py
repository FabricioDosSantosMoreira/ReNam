from typing import Optional, Literal, List


def categorize_contents(
        *,
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
        
        #TODO: nem me pergunta
        if isinstance(content, list):
            content.insert(0, identifiers[i])
            categorized_contents.append(content)

        else:
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


def evenly_assign_value_to_list(
        *,
        value: int, 
        size: int, 
        assign_at_end: Optional[bool] = False
    
    ) -> List[int]:
    """
    Generate a list where a specified value is evenly distributed among its elements.

    Args:
        value (int): The value to be distributed among the list elements.
        size (int): The size of the list.
        assign_at_end (Optional[bool]): If True, the value is assigned at the end of the list. 
            If False, the value is evenly distributed among the list elements. Defaults to False.

    Returns:
        List[int]: A list where the value is evenly distributed or assigned at the end.
    """

    # If 'value' is to be assigned at the end.
    if assign_at_end:
        evenly_list = [0] * size  # Initialize 'evenly_list' with zeros.
        evenly_list[-1] = value   # Assign 'value' to the last index.


    # If 'value' is to be evenly assigned to list
    else:
        evenly_value = value // size  # Calculate the value to be distributed
        evenly_list = [evenly_value] * size  # Assign 'evenly_value' to the list


    return evenly_list 
