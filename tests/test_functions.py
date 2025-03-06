import pytest
import tomli
from pathlib import Path
from weatherdashboard.functions.database import WeatherDataWarehouse
from google.cloud import bigquery
from google.oauth2 import service_account
import streamlit as st
import logging
from openai import OpenAI
import os
from unittest.mock import MagicMock

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")


@pytest.fixture
def mock_st_secrets(mocker):
    """
    mock st.secrets for test achievement.
    """
    secrets_path = Path(".streamlit/secrets.toml")
    with open(secrets_path, "rb") as f:
        mock_secrets = tomli.load(f)

    mocker.patch("streamlit.secrets.__getitem__", lambda _, key: mock_secrets[key])


def test_init_connection(mock_st_secrets, mocker): # mock_st_secrets
    """
    Test client BigQuery object .
    """
    # mock bigquery.Client avoiding real connection to BigQuery database
    mock_bigquery_client = mocker.patch("google.cloud.bigquery.Client", autospec=True)

    warehouse = WeatherDataWarehouse()
    assert warehouse.db_client is not None
    mock_bigquery_client.assert_called_once()

    # checkout the whether the correct credentials are used
    expected_credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )

    assert mock_bigquery_client.call_args[1]['credentials'].service_account_email == expected_credentials.service_account_email, "Actual and expected service_account_email are different"
    assert mock_bigquery_client.call_args[1]['credentials']._token_uri == expected_credentials._token_uri, "Actual and expected token_uri are different"
    assert mock_bigquery_client.call_args[1]['credentials'].project_id == expected_credentials.project_id, "Actual and expected project_id are different"


def test_init_connection_logging(mock_st_secrets, mocker, caplog): # mock_st_secrets
    """
    Test client BigQuery creation to be logged.
    """
    # mock bigquery.Client
    mocker.patch("google.cloud.bigquery.Client", autospec=True)
    with caplog.at_level(logging.INFO):
        warehouse = WeatherDataWarehouse()

    # checkout whether log is correct
    assert any("Big Query client successfully created" in record.message for record in caplog.records), \
            "Operation failed //{} //".format(caplog.text)


@pytest.fixture
def mock_openai_client(mocker):
    """
    Fixture that mocks OpenAI client with .chat.completions.create attribute.
    """
    # Mock OpenAI class
    mock_OpenAI = mocker.patch("openai.OpenAI", autospec=True)
    mock_client = mock_OpenAI.return_value

    # Mock client 'chat' and 'completions.create' attributes
    mock_chat = MagicMock()
    mock_create = MagicMock()
    mock_client.chat = mock_chat
    mock_chat.completions.create = mock_create

    # Mock response from completions.create
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content='Mocked response from deepseek-r1:free'))]
    mock_create.return_value = mock_response

    return mock_OpenAI  # Return the mock class, not the instance

def test_ai_connection(mock_openai_client):
    """
    Test AI connection to model='deepseek/deepseek-r1:free' with a mocked client.
    """
    # Call OpenAI to create a client instance
    client = mock_openai_client(base_url="https://openrouter.ai/api/v1",
                                api_key=OPENROUTER_API_KEY)

    # Call completions.create on the client instance
    completion = client.chat.completions.create(
        model="deepseek/deepseek-r1:free",
        messages=[]
    )

    # Check if OpenAI was called correctly
    mock_openai_client.assert_called_once_with(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY
    )

    # Check if completions.create was called correctly
    mock_openai_client.return_value.chat.completions.create.assert_called_once_with(
        model="deepseek/deepseek-r1:free",
        messages=[]
    )

    # Check the response
    assert completion.choices[0].message.content == 'Mocked response from deepseek-r1:free', \
        f"Expected mocked response, but got {completion.choices[0].message.content}"
