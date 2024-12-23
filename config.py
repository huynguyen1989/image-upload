from os.path import join, dirname
from dotenv import load_dotenv, dotenv_values

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

settings = dotenv_values(".env")