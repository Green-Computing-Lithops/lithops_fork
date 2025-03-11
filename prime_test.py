
def prime_function(x=4):
    x=4
    print(f"Processing input: {x}")
    print(f"MAP FUNCTION PRIME")
    
    # CPU-intensive operations to consume energy
    aux = x
    primes = []

    # Calculate prime numbers (very CPU intensive)
    for i in range(1, 50 ** x): # 500000 ** x --> abortamos mision 5050505050
        # Check if i is prime using trial division
        if i > 1:
            for j in range(2, int(i**0.5) + 1): #optimiza la division --> 1/2 
                if i % j == 0:
                    break
            else:
                # This is a prime number, do some work with it
                primes.append(i)
                aux = i

    print(f"MAX PRIME {aux} ")
    # print("Found", len(primes), "prime numbers.")
    # print("Scenario 'prime calculation' completed.")

    return aux

prime_function(x=4)