R = GF(2)['x']
for i in range(1598,2001):
    for p in R.polynomials(i):
        if p.is_irreducible():
                print(i,":",p)
                break
