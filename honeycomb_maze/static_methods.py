"""
Static Methods

"""

def pause(bool = True):
    """
    Function to pause the code
    :param bool: True = will pause, False = Will not be used. Default value set to True
    :return: Will pause the code
    """
    if bool:
        pause = input('Would you like to continue?')
    else:
        pass