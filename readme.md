# Instructions to run the code base

## Download codebase from github

* Create a working directory (actual name does not matter). example: opa-test
* cd to the working directory
* clone the github repository

```
git clone git@github.com:satishrsdg/python_opa.git
note: this uses ssh to download git repository
```

## Launch codebase in visual studio

* Assumes visual studio is downloaded and set-up 
* From working directory, change directory to opa

```
cd python_opa #From the directory where git clone was executed.
code .
```

**_note:_**
* [Getting Started With Visual Studio Code](https://medium.com/codingthesmartway-com-blog/getting-started-with-visual-studio-code-5f56eef810e1)
* Refer the section "Adding Visual Studio Code To The Command Line" in the above article

## Launch the application using docker-compose

* Assumes docker is installed
* The code-base has two docker containers
* Python app for the api. The python app internally uses sqlite to load data. src/db folder shows the tables and data loaded into sqllite
* OPA server to run the policies
* Run the code-block below to check if application can be launched and shutdown 

```
source .evn.sh #sets the environment variables required by docker-compose
docker-compose config # checks if the docker-compose file can compile
docker-compose up #launches the multi-container application
ctrl + c or docker-compose down to shutdown the containers

note: src/app/requirements.txt has the below instruction which might be blocked by proxy. In such case proxy needs to be turned off before running the above block of code

git+http://github.com/open-policy-agent/rego-python

```

## Install opa

* Download OPA [OPA Download page](https://www.openpolicyagent.org/docs/latest/#1-download-opa)
* Set executable path to the OPA file. This is required only for interactive testing. Docker image is available and is used in the actual software

## Interactively test the policy data and rules

### Start opa in interactive mode
* Run the following code from command prompt. The -w switch ensures that any changes to the files are automatically reflected within the interactive environment

```
cd src/opa/rego
opa run -w  product_policy_data.json product_policy.rego input.rego
```

* Copy and paste the following commands in the interactive shell
```
## run the following commands (available in the file execution.rego) inside the interactive mode
package execution
import data.products
import data.roles
import data.authz.product_policy
###

```

note:
* product_policy_data.json -> contains data for the policy
* product_policy.rego -> contains rules for the policy
* input.json -> sets the input to test the policy

### Test the policy

* Test the policy for default behaviour

```
# should result in true
product_policy.allow_static 
```

* In `input.rego` change user_name to Jimmy and  re-run the policy. The result should result in false
```
# should result in false
product_policy.allow_static
```

### Run unit tests on the policy data and rules

Run test cases based on test file
```
opa test  product_policy_data.json product_policy.rego product_policy_test.rego
```

## Launch the application with docker-compose
```
docker-compose up
```

### To view unrestricted access to data

```
#In a browser
localhost:5000/api/products
```

### To view restricted access to data, shows image of Jimmy's resource

```
# Jimmy and Anne are authorized to view information on themselves
http://localhost:5000/api/products/Jimmy/?user_name=Jimmy
http://localhost:5000/api/products/Anne/?user_name=Anne
```

### Unauthorized  access
```
# Jimmy is not authorized to view Anne

http://localhost:5000/api/products/Anne/?user_name=Jimmy
```

### New user is not authorized
```
http://localhost:5000/api/products/New/?user_name=New
```

### Change policy to grant access. In the file product_policy_data.json, add new user to Staticresource
```
 "roles":{
      "Admin" : {"names": ["Fleur","Frank"]},
      "Manager":{"names": ["Will","Zara"]},
      "StaticResource": {"names":["Anne","Jimmy","Rhys", "New"]}
  }

```
### New user is now authorized
```
http://localhost:5000/api/products/New/?user_name=New
```

## Demonstrating partial compile

In addition to giving a concrete true or false decision, OPA also does partial evaluation, where the outcome is a new policy

```
# Run the interactive server
# cd to src/opa/rego from root directory
opa run -w  product_policy_data.json product_policy.rego input.rego

# copy and paste the following commands from execution.rego
package execution
import data.products
import data.roles
import data.authz.product_policy 

# change input.rego 
# set method = post
# changing GET to POST will automatically reflect in the interactive shell
# as the shell is started with -w parameter
package repl
input = {
    "method": "GET",
    "user_name": "Jimmy",
    "resource_name": "Jimmy",
    "path": ["api", "products", "Jimmy"]
  }

# type input to check change is reflected
input

# set data.products as unknown to evaluate to a partial compile
unknown data.products

# run a policy that results in a partial query
data.authz.product_policy.allow_lists

## result 
+-----------+-------------------------------------------------+
| Query 1   | data.partial.authz.product_policy.allow_list    |
+-----------+-------------------------------------------------+
| Support 1 | package partial.authz.product_policy            |
|           |                                                 |
|           | allow_list {                                    |
|           |   "Jimmy" = data.products[_].category_assistant |
|           | }                                               |
|           |                                                 |
|           | default allow_list = false                      |
+-----------+-------------------------------------------------+
```

As seen above the policy returns a new policy as a result

## Converting the partial compile query to SQL query

The partially compiled queries need to be converted to actual sql queries that will get executed at the time of call. This is implemented using visitor pattern. This demonstration uses a demo package from github for this purpose.

git+http://github.com/open-policy-agent/rego-python

## Demonstrating filtering data using partial compile

* Assuming postman installed
* Run the following call

```
# Demonstrating a resource has access to its own products
# Jimmy has access to Jimmy's reosource
POST http://localhost:5000/api/products/
Body
{

  "query": "data.authz.product_policy.allow_list == true",

  "input": {
    "method": "POST",
    "user_name": "Jimmy",
    "resource_name": "Jimmy"
  },

  "unknowns": ["data.products"]
}

# Demonstrating a admin resource has access to its other resource's products
# Fleur has access to Jimmy's reosource
POST http://localhost:5000/api/products/
Body
{

  "query": "data.authz.product_policy.allow_list == true",

  "input": {
    "method": "POST",
    "user_name": "Jimmy",
    "resource_name": "Jimmy"
  },

  "unknowns": ["data.products"]
}
```


