USERS = dict(editor='editor', viewer='viewer')
GROUPS = dict(editor=['group:editors'])

def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])
