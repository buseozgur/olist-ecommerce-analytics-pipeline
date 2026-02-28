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
        # Create number_items DataFrame
        order_items = self.data["order_items"].copy()
        number_items = order_items[["order_id","order_item_id"]].copy()
        number_items = (number_items.groupby("order_id")["order_item_id"].count().reset_index(name="number_of_items"))

        return number_items

    def get_number_sellers(self):
        """
        Returns a DataFrame with:
        order_id, number_of_sellers
        """
        # Create number_seller DataFrame
        order_items = self.data["order_items"].copy()

        number_seller = order_items[["order_id","seller_id"]].copy()
        number_seller = (number_seller.groupby("order_id")["seller_id"].nunique().reset_index(name="number_of_sellers"))

        return number_seller

    def get_price_and_freight(self):
        """
        Returns a DataFrame with:
        order_id, price, freight_value
        """
        order_items = self.data["order_items"]
        price_freight = (
            order_items
            .groupby("order_id")[["price", "freight_value"]]
            .sum()
            .reset_index()
            )
        return price_freight

    # Optional
    def get_distance_seller_customer(self):
        """
        Returns a DataFrame with:
        order_id, distance_seller_customer
        """
        # Load data
        orders = self.data["orders"]
        customers = self.data["customers"]
        order_items = self.data["order_items"]
        sellers = self.data["sellers"]
        geo = self.data["geolocation"]

        # 1) Deduplicate geolocation by zip prefix (avoid many-to-many explosion)
        geo_uniq = (
            geo[["geolocation_zip_code_prefix", "geolocation_lat", "geolocation_lng"]]
            .copy()
            .groupby("geolocation_zip_code_prefix", as_index=False)
            .mean()
        )

        # 2) Order -> Customer -> Customer geo
        order_customer = (
            orders[["order_id", "customer_id"]]
            .merge(
                customers[["customer_id", "customer_zip_code_prefix"]],
                on="customer_id",
                how="left",
            )
            .merge(
                geo_uniq,
                left_on="customer_zip_code_prefix",
                right_on="geolocation_zip_code_prefix",
                how="left",
            )
            .rename(columns={"geolocation_lat": "cust_lat", "geolocation_lng": "cust_lng"})
            [["order_id", "cust_lat", "cust_lng"]]
        )

        # 3) Order_items -> Seller -> Seller geo
        item_seller = (
            order_items[["order_id", "seller_id"]]
            .merge(
                sellers[["seller_id", "seller_zip_code_prefix"]],
                on="seller_id",
                how="left",
            )
            .merge(
                geo_uniq,
                left_on="seller_zip_code_prefix",
                right_on="geolocation_zip_code_prefix",
                how="left",
            )
            .rename(columns={"geolocation_lat": "sell_lat", "geolocation_lng": "sell_lng"})
            [["order_id", "seller_id", "sell_lat", "sell_lng"]]
        )

        # 4) Pair sellers with their order's customer coords
        pairs = item_seller.merge(order_customer, on="order_id", how="left")

        # 5) Drop rows with missing coords (can't compute distance)
        pairs = pairs.dropna(subset=["sell_lat", "sell_lng", "cust_lat", "cust_lng"]).copy()

        # 6) Compute haversine distance (lon, lat order!)
        pairs["distance_km"] = pairs.apply(
            lambda row: haversine_distance(
                row["sell_lng"], row["sell_lat"], row["cust_lng"], row["cust_lat"]
            ),
            axis=1,
        )

        # 7) Average distance per order (since an order can have multiple sellers)
        distance_df = (
            pairs.groupby("order_id", as_index=False)["distance_km"]
            .mean()
            .rename(columns={"distance_km": "distance_seller_customer"})
        )

        return distance_df

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

        wait_df = self.get_wait_time()
        review_score = self.get_review_score()
        number_items = self.get_number_items()
        number_seller = self.get_number_sellers()
        price_freight = self.get_price_and_freight()

        training_data = wait_df.merge(review_score, on="order_id", how="inner")
        training_data = training_data.merge(number_items, on="order_id", how="left")
        training_data = training_data.merge(number_seller, on="order_id", how="left")
        training_data = training_data.merge(price_freight, on="order_id", how="left")

        if with_distance_seller_customer:
            distance_df = self.get_distance_seller_customer()
            training_data = training_data.merge(distance_df, on="order_id", how="left")

        training_data.dropna(inplace=True)

        return training_data
