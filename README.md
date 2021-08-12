# Variable Elimination Algorithm

- Performing probabilistic inference is challenging
  * Calculating hte posterior distribution of one or more query variables given some evidence is NP
  * No general efficient implementation available
- Exact and approximate inferences
- The variable elimination algorithm uses dynamic programming and exploits the conditional independence 
  * VEA = factor + operations on factors (restrict, sum out, multiply, normalize)

## Algorithm Skeleton 
1. Factors:
   - A function from some random variables to a number
   - A factor can represent a joint or a conditional distribution
   - Define a factor for every conditional probability distribution in the Bayes network
2. Restrict a factor:
   - Restrict a factor by assigning a value to the variable in the factor
3. Sum out a variable
   - Sum out a variable
   - Summing out X1 with domain {v1, · · · , vk} from factor f(X1, · · · , Xj ), produces a factor on X2, · · · , Xj

4. Multiplying factors:
   - Multiply two factors together
   - The product of factors f1(X, Y ) and f2(Y, Z), where Y are the variables in common

5. Normalize a factor:
   - Convert it to a probability distribution
   - Divide each value by the sum of all the values


Please visit https://donglinjia.github.io/angular-website/assets/files/AI.pdf at page 44 for more information explained.
