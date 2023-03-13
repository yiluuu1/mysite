import multiprocessing.dummy as multiprocessing

def square(x):
    return x ** 2

if __name__ == '__main__':
    inputs = [1, 2, 3, 4, 5]
    with multiprocessing.Pool(4) as pool:
        results = pool.map(square, inputs)
    print(results)