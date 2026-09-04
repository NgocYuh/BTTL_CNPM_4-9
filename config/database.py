"""SQL Server connection configuration for QuanLyGearCongNghe."""

import os


DEFAULT_CONNECTION_STRING = (
	"DRIVER={ODBC Driver 17 for SQL Server};"
	"SERVER=localhost;"
	"DATABASE=QuanLyGearCongNghe;"
	"Trusted_Connection=yes;"
	"TrustServerCertificate=yes;"
)


def get_connection_string() -> str:
	"""Return the configured connection string."""
	return os.getenv("GEAR_DB_CONNECTION_STRING", DEFAULT_CONNECTION_STRING)


def get_connection():
	"""Open and return a new pyodbc connection."""
	try:
		import pyodbc
	except ImportError as error:
		raise RuntimeError(
			"Chua cai dat pyodbc. Hay chay: pip install -r requirements.txt"
		) from error

	return pyodbc.connect(get_connection_string())
