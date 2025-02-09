import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import logging

class WeatherDataWarehouse:
    def __init__(self) -> None:
        """
        """
        self.db_client = self.init_connection(
            _credentials=service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"]
        )
    )

    @st.cache_resource(ttl=3600)
    def init_connection(_self, _credentials):
        """Create the datawarehouse connection using the right credentials
        Args:
            credentials
        Returns:
            Bigquery client connection object
        """
        # Create BIgQuery API client.
        client = bigquery.Client(credentials=_credentials)
        logging.info("Big Query client successfully created")

        return client
