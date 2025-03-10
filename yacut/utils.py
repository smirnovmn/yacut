import string

valid = (string.ascii_letters + string.digits)


def check(shortlink):
    if len(shortlink) < 16:
        for letter in shortlink:
            if letter not in valid:
                return False
        return True
    return False
