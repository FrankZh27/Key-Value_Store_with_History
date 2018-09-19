# Key-Value_Store_with_History

Think of a social network model, whenever we add a friend, it has a corresponding timestamp and so do we delete a friend. The goal of this program is to realize retriving the information according a specific timestamp.

### Approach 1: Dictionary with a list of value

### Approach 2: MongoDB

Think of the item like:

{

"name":  "A",

"friends": {

​		   "B" : [{"add": ["0", "3"]}, {"remove": ["1", "4"]}], 

​		   "D": [{"add": ["1", "3"]}, {"remove": ["2", "4"]}]

​		   }

}