# terraform-infra
This repo is used for creating infrastructure as code by using terraform

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes

### Prerequisites

* AWS, Cloud cencepts
* Terraform installed
* Infrastructure as code concept

### Installing

* Clone the repository or download and unzip it.
* `modules` folder contains the services that will be deployed in AWS.
* `dev`, `prod` are the multiple environments.
* To Customise, below explained for dev environment. Same goes with other environments
  ```
    - new files to be create: auto.tfvars, secrets.tf
    - the content for these files can be found in override.template.tfvars, override.template.secrets.tf
    - The above files contains sensitive information so do not check into version history.
  ```
* Run the following command to create the infrastructure
  ```
    - navigate to the respective folder (cd dev/prod)
    - terraform init
    - terraform validate (validates the config)
    - terraform plan (gives the plan of the infrastructure)
    - terraform apply (creates the infrastructure)
    - terraform destroy (destroys the entire created infrastructure)
  ```


## Authors

* **Venkata Srinath Mannam**