# Instructions to run the code base

## Download codebase from github

* Create a working directory (actual name does not matter). example: opa-test
* cd to the working directory
* clone the github repository

```
git clone git@github.com:satish-ganesan-sainsbury/opa.gits
note: this uses ssh to download git repository
```

## Launch codebase in visual studio

* Assumes visual studio is downloaded and set-up 
* From working directory, change directory to opa

```
cd opa #From the directory where git clone was executed.
code .
```

**_note:_**

* [Getting Started With Visual Studio Code](https://medium.com/codingthesmartway-com-blog/getting-started-with-visual-studio-code-5f56eef810e1)
* Refer the section "Adding Visual Studio Code To The Command Line" in the above article

## Launch the application using docker-compose

* Assumes docker is installed
* The code-base has two docker containers
  * Python app for the api
  * OPA server to run the policies
* Run the code-block below to check if application can be launched and shutdown 

```
source .evn.sh #sets the environment variables required by docker-compose
docker-compose config # checks if the docker-compose file can compile
docker-compose up #launches the multi-container application
ctrl + c or docker-compose down to shutdown the containers
```

## Independently test the policy data and rules

* Start opa in interactive mode

```
cd src/opa/rego
opa run -w  product_policy_data.json product_policy.rego input.json

note:
product_policy_data.json -> contains data for the policy
product_policy.rego -> contains rules for the policy
input.json -> sets the input to test the policy
```

* Execute commands in the interactive mode

```

## Following set of commands are available in the file execution.rego
package execution
import data.products
import data.roles
import data.authz.product_policy
###


```