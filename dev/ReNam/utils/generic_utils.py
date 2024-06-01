from typing import List, Any


def categorize_contents(list_to_categorize: list[Any], identifier: list[Any] = []) -> list[list[Any]]:
    """
    Categorizes elements of a list into sublists with identifiers.
    
    Args:
        list_to_categorize (List[Any]): The list to categorize.
        identifier (List[str], optional): List of identifiers for each element. If not provided, 
                        elements will be identified by their indices, starting from 1.
    
    Returns:
        List[List[Any]]: A list of sublists where each sublist contains an identifier and an element from the original list.
    """
    categorized_list: list[list[Any]] = []

    if not identifier: # If 'identifier' isn't provided. Iterate over the elements of 'list_to_categorize'
        identifier = []
        for n in range(len(list_to_categorize)):
            identifier.append(str(n + 1)) # Assign identifiers based on indices starting from 1

    for i in range(len(list_to_categorize)): # Iterate over elements of 'list_to_categorize'

        list_to_categorize[i].insert(0, identifier[i])
        
        categorized_list.append(list_to_categorize[i]) # Create sublists pairing identifiers with corresponding elements


    return categorized_list 


def ensure_value_parity(value: int, *, target_parity: str = None, decrease: bool = False) -> int:
    current_parity = "even" if value % 2 == 0 else "odd"

    if current_parity != target_parity:
        if decrease:
            return value - 1
        else:
            return value + 1

    return value  # 'value' already has the desired parity


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
