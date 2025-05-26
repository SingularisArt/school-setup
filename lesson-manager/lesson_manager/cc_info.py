import utils
from lesson_manager import config


info = utils.load_data(f"{config.current_course}/info.yaml", "yaml")

title = info["title"]
topic = info["topic"]
crn = info["class_number"]
short = info["short"]
author = info["author"]
term = info["term"]
faculty = info["faculty"]
college = info["college"]
location = info["location"]
year = info["year"]
start_date = info["start_date"]
end_date = info["end_date"]
start_time = info["start_time"]
end_time = info["end_time"]
professor_name = info["professor"]["name"]
professor_email = info["professor"]["email"]
professor_phone_number = info["professor"]["phone_number"]
professor_office = info["professor"]["office"]
