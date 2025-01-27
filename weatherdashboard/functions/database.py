import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import logging


class WeatherDatawarehouse:
    def __init__(
        self,
    ) -> None:
        self.credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"]
        )
        self.db_client = self.init_connection(credentials=self.credentials)

    def init_connection(self, credentials):
        """Create the datawarehouse connection using the right credentials
        Args:
            credentials
        Returns:
            Bigquery client connection object

        """
        # Create BIgQuery API client.
        client = bigquery.Client(credentials=credentials)
        logging.info("Big Query client successfully created")

        return client
