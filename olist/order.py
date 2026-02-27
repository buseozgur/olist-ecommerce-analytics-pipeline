import pandas as pd
import numpy as np
from olist.utils import haversine_distance
from olist.data import Olist


class Order:
    '''
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        self.data = Olist().get_data()

    def get_wait_time(self, is_delivered=True):
        """
        Returns a DataFrame with:
        [order_id, wait_time, expected_wait_time, delay_vs_expected, order_status]
        and filters out non-delivered orders unless specified
        """
        # Hint: Within this instance method, you have access to the instance of the class Order in the variable self, as well as all its attributes
        orders = self.data["orders"].copy()

        # Filter the delivered orders and change the date_cols to datetime
        if is_delivered:
            wait_df = orders[orders["order_status"]=="delivered"].copy()

        date_cols = [
            "order_purchase_timestamp",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
            ]
        wait_df[date_cols] = wait_df[date_cols].apply(pd.to_datetime)

        # Creating the wait_time, expected_wait_time and delay_vs_expected columns
        wait_df["wait_time"] = (wait_df["order_delivered_customer_date"] - wait_df["order_purchase_timestamp"]) /np.timedelta64(1, "D")
        wait_df["expected_wait_time"] = (wait_df["order_estimated_delivery_date"] - wait_df["order_purchase_timestamp"]) /np.timedelta64(1, "D")
        wait_df["delay_vs_expected"] = (
            wait_df["wait_time"] - wait_df["expected_wait_time"]
            )
        wait_df["delay_vs_expected"] = wait_df["delay_vs_expected"].clip(lower=0)

        wait_df = wait_df[["order_id",
                  "wait_time",
                  "expected_wait_time",
                  "delay_vs_expected",
                  "order_status"]]

        return wait_df


    def get_review_score(self):
        """
        Returns a DataFrame with:
        order_id, dim_is_five_star, dim_is_one_star, review_score
        """
        reviews = self.data['order_reviews'].copy()

        # Create review_score DataFrame
        review_score = reviews[["order_id", "review_score"]].copy()
        review_score["dim_is_five_star"] = np.where(review_score["review_score"]==5,1,0)
        review_score["dim_is_one_star"] = np.where(review_score["review_score"]==1,1,0)

        return review_score

    def get_number_items(self):
        """
        Returns a DataFrame with:
        order_id, number_of_items
        """
        pass  # YOUR CODE HERE

    def get_number_sellers(self):
        """
        Returns a DataFrame with:
        order_id, number_of_sellers
        """
        pass  # YOUR CODE HERE

    def get_price_and_freight(self):
        """
        Returns a DataFrame with:
        order_id, price, freight_value
        """
        pass  # YOUR CODE HERE

    # Optional
    def get_distance_seller_customer(self):
        """
        Returns a DataFrame with:
        order_id, distance_seller_customer
        """
        pass  # YOUR CODE HERE

    def get_training_data(self,
                          is_delivered=True,
                          with_distance_seller_customer=False):
        """
        Returns a clean DataFrame (without NaN), with the all following columns:
        ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
        'order_status', 'dim_is_five_star', 'dim_is_one_star', 'review_score',
        'number_of_items', 'number_of_sellers', 'price', 'freight_value',
        'distance_seller_customer']
        """
        # Hint: make sure to re-use your instance methods defined above
        pass  # YOUR CODE HERE
