def coloredText(s, color='green'):
    colors = {
        'green':    32,
        'red':      31,
    }
    template = '\033[%dm%s\033[0m' % (colors[color], s)
    return template
