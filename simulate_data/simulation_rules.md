# Data Simulation Rules
This markdown file sets out the defining rules by which data was simulated.

## Customer Data
### Customer IDs
* Any customer can be identified by a unique Customer ID.
* Customer ID is generated using list comprehension with the first customer
being C000000000, the second as C000000001, etc.

### Remaining Customer Data
Remaining customer features include:
* *first_name*
* *last_name*
* *postcode*
* *date_of_birth*
* *join_date*

These are all simulated using the faker library where:
* *date_of_birth* ranges from 18 to 90 years old using the current date 
* *join_date* ranges from today to maximum 10 years ago


## Policy Data

### Customer ID
* Customer ID is copied from the generated customer data

### Policy ID
* Any policy can be identified by a unique Policy ID.
* Policy ID is copied from the customer ID with the C ammended for a P and with added trailing digits for distinction.
* A customer can have multiple insurance policies.
* The number of policies per customer is selected using a discrete uniform distribution over (1, 3).

### Policy Type
Available policy types are:
* Life Insurance
* Health Insurance
* Car Insurance
* Home Insurance

The policy type is selected as a discrete uniform distribution over the defined policy types.

### Policy Dates

* A policy's start date is selected as the customers join date.
* A policy is indefinete (has no end date) 20% of the time.
* A policy's end date is selected as a discrete uniform distribution over (1, 5) number of years after the start date 80% of the time.

### Monthly Premium
A policy's monthly premium rate is selecetd as a discrete uniform distribution over (50, 500).

### Policy Status
A policy's status is either active or cancelled with ratio (7:2) using dicrete random uniform sampling.


## Claims Data


## Payment Data


## Transaction Data