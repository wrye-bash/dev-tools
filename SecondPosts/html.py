# FORMATTING FUNCTIONS ========================================
COLOR_INTRO = 'orange'
COLOR_ASSIGNEE = '#00FF00'
COLOR_DONE = 'orange'

def color(text,color_=None):
    if color_:
        return '[color=' + color_ + ']' + text + '[/color]'
    else:
        return text

def url(url_,title):
    return '[url=' + url_ + ']' + title + '[/url]'

def bold(text):
    return '[b]' + text + '[/b]'

def strike(text):
    return '[s]' + text + '[/s]'

def li(text):
    return '[*]' + text

def h2(text):
    return '<h2>' + text + '</h2>'

def ul(items):
    yield '<ul>'
    for i in items:
        yield '<li>' + i + '</li>'
    yield' </ul>'

def formatIssue(issue,issueType):
    if issue.state == 'open':
        s = lambda x: x
    else:
        s = lambda x: color(strike(x),COLOR_DONE)
    if issue.assignee:
        assignee = issue.assignee
        assignee = ' ' + url(assignee.url,
            color('(' + assignee.login + ')',COLOR_ASSIGNEE))
    else:
        assignee = ''
    return li(s(url(issue.html_url,issueType + ' %i' % issue.number) +
                ': ' + issue.title)
              + assignee)
