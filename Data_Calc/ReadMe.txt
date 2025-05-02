The data used is 180 sample(3 hour) moving average to get rid of all the dynamics and get agood steady behavioir.

The set of data used for training on MT level is 2-8(winter) and 30/33 

Depending the data you train for your model gets better R2 score depending selected variable.

There are different ways to further improve it:

1-Make automated code for running with different variables
2-Make automated search inside different weeks for train and test and switch train and test sets
3-Make the variables of higher order: Psuc^2 Psuc^3 Psuc^2*Pdisch  and .... 
 

Some general rule based on experience:
The less variable used is and advantage(use minimum # of var)
Not adding variable unless its adding R2 score to all paairs of test and train and switch test train set
Adding 1 at a time of Var
Check if that var makes sense to add(dont add random shit just cause it gives better R2 score)
