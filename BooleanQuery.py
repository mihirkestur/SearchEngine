def performQuery(query, PostList):

    if 'OR' in query:
        partition_t = query.split('OR')
        partition = []
        
        for s in partition_t:
            partition.append(s.strip())
        # print(partition)
        postings = []

        for s in partition:
            l = performQuery(s, PostList)
            postings.append(l)

        final = list(set.union(*map(set,postings)))
        return final


    elif 'AND' in query:
        partition_t = query.split('AND')
        partition = []
        for s in partition_t:
            partition.append(s.strip())
        
        postings = []

        for s in partition:
            l = performQuery(s, PostList)
            postings.append(l)

        
        final = list(set.intersection(*map(set,postings)))



        return final
    else :
        
        return [i[0] for i in PostList[query]]#PostList[query]


    
# print(performQuery('day'))
# print(performQuery('cambridge'))
# print(performQuery('subject'))

# query = 'day OR cambridge AND subject'

# l = performQuery(query)
# print(l)