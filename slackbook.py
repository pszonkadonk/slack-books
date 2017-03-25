import os
import time
from slackclient import SlackClient
from book import BookClient

class SlackBook:
    def __init__(self, bot_id, slack_client, watson_conversation, book_client):
        self.bot_id = bot_id
        self.slack_client = slack_client
        self.watson_conversation = watson_conversation
        self.book_client = book_client
        self.delay = 1
        self.workspace_id = 'c1a2722a-b334-4b16-a197-ec4e293d5fc9'

        self.bot_directed = "<@" + bot_id + ">"

        self.context = {}

    def format_book_info(self, selected_book, book_description):
        """ 
        Formatting book information that is sent to the user after
        a selection is made
        """
        response = "Here is some information on that book \n" +\
            "Title: " + selected_book['book_title'] + "\n" +\
            "Author: " + selected_book['author_name'] + "\n" +\
            "Description" + "\n" + \
            book_description + "\n" + \
            'Average Rating: ' + selected_book['average_rating'] + "\n" +\
            "Review Count: " + selected_book['review_count'] + "\n" + \
            "Would you like to revisit the list?"

        return response


    def handle_selection_message(self, selection):
        """
        Select and calls get_book_info_by_id to get the book description
        that the user chose in the selection menu.  Calls format_book_info 
        for formatting
        """
        selected_book = self.context['books'][selection-1]
        book_description = self.book_client.get_book_info_by_id(selected_book['book_id'])

        return self.format_book_info(selected_book, book_description)


    def handle_message(self, message, channel):
        """
        Function is called whenever an individual directs a message at bot.
        If the message is valid, the bot will act on the message.  If it is not,
        the bot will respond make, asking the user to rephrase their request.
        """
        print(message)
        watson_response = self.watson_conversation.message(
            workspace_id = self.workspace_id,
            message_input = {"text": message},
            context = self.context)
        
        # print(watson_response["context"])
        print(watson_response['entities'])
        self.context = watson_response["context"]

        print(watson_response['context'])


        #if author has chosen author,  get books.  If user is revisiting the list
        # for a different book by the same author, simply pull the book list from context
        
        if 'is_author' in self.context.keys() and self.context['is_author']:
            if 'books' in self.context: 
                message = self.context['books'][0]['author_name']
            response = self.handle_author_message(message)

        # if user has already chosen a genre previosuly, this grabs the books 
        # from context so that the user can revisit the list of books in genre

        if 'genre' in self.context.keys() and self.context['selection'] == 'None':
            if 'books' in self.context:  #check to see if book list is already in context
                message = self.context['genre']
            response = self.handle_genre_message(message)   # else get book list from goodreads

        # if user has made a numeric selection from the list.  I.E chooses book "4"    
            
        elif 'is_selection' in self.context.keys() and self.context['is_selection']:

            self.context['selection_valid'] = False
            response = "Invalid entry. Press any key to see your choices again..."

            if self.context['selection'].isdigit():
                selection = int(self.context['selection'])
                if selection >= 1 and selection <= 20:
                    self.context['selection_valid'] = True
                    response = self.handle_selection_message(selection)

        #if user is satisfied, and makes no selection
        
        elif 'selection' in self.context.keys() and self.context['selection'] == None:
            response = "Ok then, let me know if there is anything else you need." 

        #triggered when the user triggers an entity(genre) to search for
            
        elif watson_response['entities'] and watson_response['entities'][0]['entity'] == 'genre':
            genre = watson_response['entities'][0]['value']
            self.context['genre'] = genre
            response = self.handle_genre_message(genre)

        else:
            response = ''
            for text in watson_response['output']['text']:
                response += text + "\n"            
        
        self.respond_to_message(response, channel)

        

    def handle_author_message(self, message):
        """
        The user is looking for a particular author.  Makes a request to the book client,
        to pull an array of books from Goodreads and send to the context object.  Sends the list
        of books to the user
        """
        if self.context['get_books']:
            self.context['books'] = self.book_client.find_by_author(message)

        response = "Ive found the following books for that author: \n"

        for i, book in enumerate(self.context['books']):
            response += str(i+1) + ". " + book['book_title'] + "\n"
        response+= "Please enter the number of the book you would like to know more about"

        return response

    def handle_genre_message(self, message):
        """
        The user is looking for a particular genre.  Makes a request to the book client
        to pull an array of books from Goodreads and send to context object.  Sends list of
        books to the user
        """
        if self.context['get_genre'] and 'books' not in self.context.keys():
            self.context['books'] = self.book_client.find_by_genre(message)

        response = "The following are some recent books released in the " + message + " genre that have great reviews! \n"

        for(i, book) in enumerate(self.context['books']):
            response += str(i+1) + ". " + book['book_title'] + "\n"
        response+= "Enter the number of a book if you would like to know more about it"

        return response

    def parse_output(self, slack_rtm_output):
        """
            This parsing function listens to all communcications 
            in the slack channel and returns None unless a message 
            is directed at the bot, based upon its ID
        """
        output = slack_rtm_output
        if output and len(output) > 0:
            for message in output:
                if message and 'text' in message and self.bot_directed in message['text']:
                    return message['text'].split(self.bot_directed)[1].strip().lower(), \
                        message['channel']
        return None, None
    
    def respond_to_message(self, response, channel):
        """
        Sends message back to user
        """
        self.slack_client.api_call("chat.postMessage", channel = channel,
                                text = response, as_user = True)


    def run(self):
        DELAY = 1
        if self.slack_client.rtm_connect():
            print("slack-books-bot connected...")
            while True:
                command, channel = self.parse_output(self.slack_client.rtm_read())
                if(command and channel):
                    self.handle_message(command, channel)
                time.sleep(DELAY)
        else:
            print("Could not connect to slack.  Please check slack api token or bot id")


