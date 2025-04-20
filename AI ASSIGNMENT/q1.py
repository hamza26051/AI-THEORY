def query(x):
    return -1 * (x - 7)**2 + 49  

def find_peak(N: int) -> int:
    x = 0
    while x < N:
        if query(x + 1) > query(x):
            x += 1
        else:
            break
    return x
N = 14
peak_index = find_peak(N)
print("Peak index:", peak_index)
print("Peak elevation:", query(peak_index))
