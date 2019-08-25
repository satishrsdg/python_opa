#Implementing Authorization using Open Policy Agent

## Introduction

CORE team provides an authorization look-up service, which based on an authenticated user returns a token and the list of permission the user has to the different resources. With this approach, the onus is on the product teams to implement authorization to their respective resources. The usual technique is to implement the authorization rules inside code. This leads to a situation where it is cumbersome to audit the permissions. This paper discusses an approach whereby authorization can be converted into rules and maintained outside of the main code base using Open Policy Agent

## Approach

The paper below discusses the importance of each micro-service executing authorization checks for even chained calls originating from outside of the service boundary.[Micro-services Authorization](https://sainsburys-confluence.valiantys.net/x/mWVCAw)

Implementing would lead to high frequency of authorization calls. Hence, the architecture contour of a solution would contain the following features:
* Low latency
* Running in a side-car set-up along side applications of each micro-service
* Rules based
* Outside of main code base

![](https://miro.medium.com/max/826/1*CrFdCcWgaFT2EqGV2tds3w.png)

[Image source:](https://blog.openpolicyagent.org/write-policy-in-opa-enforce-policy-in-sql-d9d24db93bf4)

As the image above displays, a call from the microservice is sent to the authorization service, which in turns sends a decision if the call can be approved. Only if the call is approved the micro-service supplies the relevant data from within its boundary

## Two broad problems

There are two main broad problem areas:
* Authorizing a particular user to a specific resource
* Filtering dataset based on user's permission without making any changes to the main code base

### *Authorizing to a specific resource*

```
/api/products/<category_assistant>
/api/products/Jim
```

Access to be a call such as above is relatively easy to restrict

```
### Rules
#check the the method is post
input.method == "POST"

#check if the api-path follows required construct ending with variable user_name
["api","products", user_name] = input.path 

#check if the user name in the path is same as the
input.user_name == user_name
```
This ensures that only the authenticated user can access the resource associated with him. 

### *Filtering data*

Solution to the above problem is valid in our context, if the resource can be supplied for each user without any specific filtering mechanisms. The above solution can be extended and generalized to solve for filtering

```
### Rules
input.method == "POST"
  # use unification: user_name is copied from input. path
  ["api","products", user_name] = input.path 
  input.user_name == user_name

  #This additional rules filters the category_assistant to a specific user
  products[_].category_assistant == input.user_name
```

OPA allows for unknown execution. Instead of returning a boolean decision, when used as unknown the program returns in another rule. For the above rule set if we set-up 
```
unknown data.products
```
we get back another rule

```
+---------+---------------------------------------------+
| Query 1 | "Jim" = data.products[_].category_assistant |
+---------+---------------------------------------------+
````

This rule is then translated into the relevant sql query to filter out the data. This is explained very well in this article [OPA Partial Evaluation](https://blog.openpolicyagent.org/partial-evaluation-162750eaf422)