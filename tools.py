def coloredText(s, color='green'):
    colors = {
        'green': 32,
        'red':   31,
        'yellow': 33,
    }
    template = '\033[%dm%s\033[0m' % (colors[color], s)
    return template


def newton2kgs(n):
    return n / 9.807

def kgs2newton(kgs):
    return kgs * 9.807
