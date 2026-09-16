import pandas as pd 
from faker import Faker
from loguru import logger
import random

def customer_data(num_customers=1000):

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
            policy_dict["policy_id"].append("P" + str(index).zfill(8) + ("A" if _ == 0 else "B" if _ == 1 else "C"))
            policy_dict["customer_id"].append(row["customer_id"])
            policy_dict["policy_type"].append("Type A" if index % 2 == 0 else "Type B")
            policy_dict["start_date"].append(row["join_date"])
            policy_dict["end_date"].append(pd.to_datetime(row["join_date"]) + pd.DateOffset(years=random.randint(1, 5)))
            policy_dict["monthly_premium"].append(50 if index % 2 == 0 else 75)
            policy_dict["status"].append("Active" if index % 3 != 0 else "Cancelled")

    logger.info(f"Simulated {len(policy_dict['policy_id'])} policies")

    return pd.DataFrame(policy_dict)


def claim_data(policies):
    # Simulate claim data

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
            claims_dict["claim_status"].append("Approved" if random.random() < 0.8 else "Denied")

    logger.info(f"Simulated {len(claims_dict['claim_id'])} claims")

    return pd.DataFrame(claims_dict)

def main(num_customers=10000, save_path="data/simulated_data.csv"):

    logger.info(f"Simulating data for data warehouse")

    customers = customer_data(num_customers)
    policies = policy_data(customers)
    claims = claim_data(policies)

    customers.to_csv(save_path.replace(".csv", "_customers.csv"), index=False)
    policies.to_csv(save_path.replace(".csv", "_policies.csv"), index=False)
    claims.to_csv(save_path.replace(".csv", "_claims.csv"), index=False)




if __name__ == "__main__":
    random.seed(19)
    main()