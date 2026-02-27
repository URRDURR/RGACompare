import sys
import os

def asset_path(relative_path: str) -> str:
    """returns the 

    Args:
        relative_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    if hasattr(sys, '_MEIPASS'):
        base_path =sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
    # base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname((os.path.abspath(__file__)))))

    asset_path = os.path.join(base_path, relative_path)

    return asset_path