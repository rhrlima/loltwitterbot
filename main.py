
from src import update_data as data
from src import bot

if __name__ == '__main__':
	
	data.get_updated_data(force=False)

	bot = bot.Bot()
	
	for _ in range(8):
		print(bot.get_formated_message())