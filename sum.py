__author__ = 'Yang'

def func(x, n):
    y=[i for i in str(x)]
    target=y[0:len(y)-n]
    index= len(y)-n
    ret=[]
    def findn(x,i):
        for a,b in enumerate(x):
            if b==i:
                return a
    while n>0 and index<len(y):
        t=min(target)
        ret.append(t)
        i=findn(target,t)
        n=n-i
        target=target[i+1:len(target)]
        index_next = min(len(y),index+i+1)
        target.extend(y[index:index_next])
        index = index_next
    if target:
        ret.extend(target)
    return ret


def minmaxheap():
    arr = [3,2,5,7,4,1,100]
    import heapq
    heapq.heapify(arr)
    print heapq.nlargest(4,arr)
    return heapq.nlargest(4,arr)

def main():
    #print func(111224198, 3)
    setup = '''
    arr=[3,2,5,7,4,1,100]
    '''
    import timeit
    timeit.timeit('char in text', setup='text = "sample string"; char = "g"')
    #print timeit.Timer('a= [3,2,5,7,4,1,100]; minmaxheap(a)').repeat(10)
    #t = timeit.Timer('char in text', setup='text = "sample string"; char = "g"')
    print(timeit.repeat(stmt='minmaxheap()', setup="from __main__ import minmaxheap", repeat=3))

main()
