from chatterbot import ChatBot
import chatterbot
#from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer


# Create a new instance of a ChatBot
bot = ChatBot(
    'Example Bot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.90,
            #"statement_comparison_function": chatterbot.comparisons.levenshtein_distance,
            "response_selection_method": chatterbot.response_selection.get_first_response
        }
    ]
)

# trainer = ChatterBotCorpusTrainer(bot)
# trainer.train("chatterbot.corpus.english")
#with the below lines:
bot.set_trainer(ChatterBotCorpusTrainer)
bot.train("chatterbot.corpus.BotTemp1")
#trainer = ListTrainer(bot)

# Train the chat bot with a few responses
#trainer.train(['How can I help you?','I want to create a chat bot','Have you read the documentation?','No, I have not','This should help get you started: http://chatterbot.rtfd.org/en/latest/quickstart.html'])

# Get a response for some unexpected input
response = bot.get_response('dress code')
print(response)