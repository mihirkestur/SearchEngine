"""
Processes wild card query
Returns:
    PosnPostinglist for all relevant terms
"""
def WildCard(query, PermList, PostList):
    ans_token = []
    first, second = query.split("*")
    check = second[::-1] + "$" + first
    for token in PermList.keys():
        # See if token is matching with first and second
        if(token.startswith(check)):
            ans_token.append(PermList[token])
            
    return [PostList[i][0] for i in ans_token]