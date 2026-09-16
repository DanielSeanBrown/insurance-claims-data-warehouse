import pandas as pd 
from faker import Faker
from loguru import logger
import random

POLICY_TYPES = [
    "Life Insurance",
    "Health Insurance",
    "Car Insurance",
    "Home Insurance"
]

def customer_data(num_customers=1000):
    """Simulate customer data.

    Args:
        num_customers (int): Number of customers to simulate.

    Returns:
        pd.DataFrame: DataFrame containing simulated customer data.
            Columns include:
                - customer_id (str): Unique identifier for the customer.
                - first_name (str): Customer's first name.
                - last_name (str): Customer's last name.
                - postcode (str): Customer's postcode.
                - date_of_birth (str): Customer's date of birth.
                - join_date (str): Date the customer joined.
    """

    customer_dict = {
        "customer_id": [],
        "first_name": [],
        "last_name": [],
        "postcode": [],
        "date_of_birth": [],
        "join_date": [],
    }

    fake = Faker("en_GB")

    for i in range(num_customers):
        customer_dict["customer_id"].append("C" + str(i).zfill(8))
        customer_dict["first_name"].append(fake.first_name())
        customer_dict["last_name"].append(fake.last_name())
        customer_dict["postcode"].append(fake.postcode())
        customer_dict["date_of_birth"].append(f"{fake.date_of_birth(minimum_age=18, maximum_age=90)}")
        customer_dict["join_date"].append(fake.date_between(start_date="-10y", end_date="today"))

    logger.info(f"Simulated {num_customers} customers")

    return pd.DataFrame(customer_dict)

def policy_data(customers):
    """Simulate policy data.

    Args:
        customers (pd.DataFrame): DataFrame containing customer data.

    Returns:
        pd.DataFrame: DataFrame containing simulated policy data.
            Columns include:
                - policy_id (str): Unique identifier for the policy.
                - customer_id (str): Unique identifier for the customer.
                - policy_type (str): Type of insurance policy.
                - start_date (str): Policy start date.
                - end_date (str): Policy end date (if any).
                - monthly_premium (float): Monthly premium for the policy.
                - status (str): Status of the policy (Active/Cancelled).
    """

    policy_dict = {
        "policy_id": [],
        "customer_id": [],
        "policy_type": [],
        "start_date": [],
        "end_date": [],
        "monthly_premium": [],
        "status": [],
    }

    for index, row in customers.iterrows():
        num_policies = random.randint(1, 3)  # Each customer can have 1 to 3 policies
        for _ in range(num_policies):
            policy_dict["policy_id"].append("P" + str(index).zfill(8) + str(_).zfill(2))
            policy_dict["customer_id"].append(row["customer_id"])
            policy_dict["policy_type"].append(POLICY_TYPES[random.randint(0, len(POLICY_TYPES) - 1)])
            policy_dict["start_date"].append(row["join_date"])
            policy_dict["end_date"].append(pd.to_datetime(row["join_date"]) + pd.DateOffset(years=random.randint(1, 5)) if random.random() < 0.8 else None)
            policy_dict["monthly_premium"].append(random.uniform(50, 500))
            policy_dict["status"].append("Active" if random.random() <= 0.78 else "Cancelled")

    logger.info(f"Simulated {len(policy_dict['policy_id'])} policies")

    return pd.DataFrame(policy_dict)


def claim_data(policies):
    """Simulate claim data.

    Args:
        policies (pd.DataFrame): DataFrame containing policy data.

    Returns:
        pd.DataFrame: DataFrame containing simulated claim data.
            Columns include:
                - claim_id (str): Unique identifier for the claim.
                - policy_id (str): Unique identifier for the policy.
                - claim_date (str): Date the claim was made.
                - claim_amount (float): Amount claimed.
                - claim_status (str): Status of the claim (Approved/Under Review/Denied).
    """

    claims_dict = {
        "claim_id": [],
        "policy_id": [],
        "claim_date": [],
        "claim_amount": [],
        "claim_status": [],
    }

    for index, row in policies.iterrows():
        if row["status"] == "Active" and random.random() < 0.1:  # 10% chance of a claim for active policies
            claims_dict["claim_id"].append("CL" + str(index).zfill(8))
            claims_dict["policy_id"].append(row["policy_id"])
            claims_dict["claim_date"].append(pd.to_datetime(row["start_date"]) + pd.DateOffset(days=random.randint(1, 365)))
            claims_dict["claim_amount"].append(random.randint(100, 5000))
            claims_dict["claim_status"].append("Approved" if random.random() < 0.8 else "Under Review" if random.random() < 0.5 else "Denied")

    logger.info(f"Simulated {len(claims_dict['claim_id'])} claims")

    return pd.DataFrame(claims_dict)

def payment_data(claims):
    """Simulate payment data.
    Args:
        claims (pd.DataFrame): DataFrame containing claim data.

    Returns:
        pd.DataFrame: DataFrame containing simulated payment data.
            Columns include:
                - payment_id (str): Unique identifier for the payment.
                - policy_id (str): Unique identifier for the policy.
                - outstanding_amount (float): Outstanding amount for the payment.
                - schedule (str): Payment schedule (Single ,Monthly, Quarterly, Annually).
    """

    payments_dict = {
        "payment_id": [],
        "policy_id": [],
        "outstanding_amount": [],
        "schedule": [],
    }

    for index, row in claims.iterrows():
        payments_dict["payment_id"].append("PM" + str(index).zfill(8))
        payments_dict["policy_id"].append(row["policy_id"])
        payments_dict["outstanding_amount"].append(row["claim_amount"] // random.randint(1, 36) if "claim_amount" in row else 0)
        payments_dict["schedule"].append(random.choice(["Single", "Monthly", "Quarterly", "Annually"]))

    logger.info(f"Simulated {len(payments_dict['payment_id'])} payments")

    return pd.DataFrame(payments_dict)

def transaction_data(payments):
    """Simulate transaction data.

    Args:
        payments (pd.DataFrame): DataFrame containing payment data.

    Returns:
        pd.DataFrame: DataFrame containing simulated transaction data.
            Columns include:
                - transaction_id (str): Unique identifier for the transaction.
                - policy_id (str): Unique identifier for the policy.
                - transaction_date (str): Date the transaction was made.
                - transaction_amount (float): Amount of the transaction.
    """

    transactions_dict = {
        "transaction_id": [],
        "policy_id": [],
        "transaction_date": [],
        "transaction_amount": [],
    }

    for index, row in payments.iterrows():
        transactions_dict["transaction_id"].append("TX" + str(index).zfill(8))
        transactions_dict["policy_id"].append(row["policy_id"])
        transactions_dict["transaction_date"].append(pd.to_datetime(row["outstanding_amount"]))
        transactions_dict["transaction_amount"].append(row["outstanding_amount"])

    logger.info(f"Simulated {len(transactions_dict['transaction_id'])} transactions")

    return pd.DataFrame(transactions_dict)

def main(num_customers=10000, save_path="data/simulated_data.csv"):

    logger.info(f"Simulating data for data warehouse")

    customers = customer_data(num_customers)
    policies = policy_data(customers)
    claims = claim_data(policies)
    payments = payment_data(claims)
    transactions = transaction_data(payments)

    customers.to_csv(save_path.replace(".csv", "_customers.csv"), index=False)
    policies.to_csv(save_path.replace(".csv", "_policies.csv"), index=False)
    claims.to_csv(save_path.replace(".csv", "_claims.csv"), index=False)
    payments.to_csv(save_path.replace(".csv", "_payments.csv"), index=False)
    transactions.to_csv(save_path.replace(".csv", "_transactions.csv"), index=False)   




if __name__ == "__main__":
    random.seed(19)
    main()