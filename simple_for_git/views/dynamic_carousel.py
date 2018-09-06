import sqlite3
import datetime

class CarouselDatabase:

    def __init__(self, connection, table_name):
        self.cursor = connection.cursor()
        self.featured_table = table_name
    
    # Creates a table (if DNE) with title, description, image path, url to content, and date added columns for content to be featured in the carousel
    def create_table_for_featured_content(self):
        table_query = "CREATE TABLE IF NOT EXISTS {table_name} (slide_title PRIMARY KEY, slide_description, image_filename, content_url, date_added)".format(table_name=self.featured_table)

        self.cursor.execute(table_query)

    # Inserts elements provided as a dictionary and inserts them into the appropriate columns.
    def insert_elements_into_table(self, elements):
        insertion_query = "INSERT OR REPLACE INTO {table_name} (slide_title, slide_description, image_filename, content_url, date_added)\
            VALUES (:slide_title, :slide_description, :image_filename, :content_url, :date_added);".format(table_name=self.featured_table)

        self.cursor.execute(insertion_query, elements)

    # Takes all elements stored in the database and packages them into a dictionary to be passed to main and displayed in html
    def package_elements_from_db(self):

        all_elements_query = "SELECT * FROM {table_name}".format(table_name=self.featured_table)
        executed_statement = self.cursor.execute(all_elements_query)

        # Get the column names from the database
        table_description = executed_statement.description
        filtered_col_from_description = [col_name[0] for col_name in table_description]

        # Fetch the results from the executed query 
        all_elements = executed_statement.fetchall()

        elements_dict = {}
        collection_of_all = {}

        # Go through the elements one by one, keeping count as go along
        for counter_key, element_package in enumerate(all_elements):
            # Go through every column for each element package from outer loop and add it to the dictionary        
            for index, col_name in enumerate(filtered_col_from_description):
                elements_dict.update({col_name: element_package[index]})

            # Update the final dictionary that will contain all element packages with the package created above
            collection_of_all.update({counter_key: elements_dict.copy()})
            # Clear so can be updated with new elements next loop
            elements_dict.clear()
        
        return collection_of_all

    # Deletes the table from the file but doesn't get rid of the file... another method to do this?
    def delete_table(self):
        deletion_query = "DROP TABLE IF EXISTS {table_name}".format(table_name=self.featured_table)

        self.cursor.execute(deletion_query)

# Create a connection to the database file specified by the user
def connect_to_db(user_filename):
    filename_w_ext = "{filename}{ext}".format(filename=user_filename, ext=".sqlite")
    connection = sqlite3.connect(filename_w_ext)

    return connection

# Commit any changes to the database and close the connection
def commit_and_close_connection(connection):
    print("Committing changes and closing connection...")
    connection.commit()
    connection.close()

# Collect all elements crucial to the carousel and package them to be returned
def collect_elements_to_be_added(filename_no_ext):

    collection_of_packages = []
    featured_elements_package = {}

    # These sequences are required to inform the start of a new slide, and the end of the current slide respectively
    new_slide_sequence = "###"
    stop_collection_sequence ="---"

    filename_w_ext = "{filename}.{ext}".format(filename=filename_no_ext, ext="txt")

    file = open(filename_w_ext, "r")
    for line in file:
        try:
            if line.startswith(new_slide_sequence): # New content incoming...
                # Get the slide number to be output to command in print statement
                slide_num = line.split("###")[1].rstrip("\n")
                print("Now reading info for {slide_num}...".format(slide_num=slide_num))
            elif line.startswith(stop_collection_sequence): # End of current content...

                # Get the date/time and add that to the dictionary as well
                date_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                featured_elements_package.update({'date_added' : date_added})

                # Output the results of the file read to user so can confirm whether correct
                for key, value in featured_elements_package.items():
                    print("\t{key}: {value}".format(key=key, value=value))

                # Add this package to the collection and clear for next chunk of content
                collection_of_packages.append(featured_elements_package.copy())
                featured_elements_package.clear()

            else:
                # Get the key for the dictionary from the left side of the equals sign (in txt file)
                key_from_text = line.split("=")[0]
                # Get the actual value from the right side of the equals sign
                value_from_text = line.split("=")[1].rstrip("\n")

                # Add the extracted elements to the dictionary
                featured_elements_package.update({key_from_text : value_from_text})

        # Handle any exceptions and let user know of the issue
        except Exception as e:
            print("Something went wrong: {exception}".format(exception=e))
            return 0

    return collection_of_packages

# Add the collected elements to the database specified by user
def add_elements_to_database(elements, carousel_database):
    carousel_database.create_table_for_featured_content()
    carousel_database.insert_elements_into_table(elements)

# Get the user's desired action on the database (ie. adding, editing, deleting elements)
def get_user_action(possible_actions):
    valid_response = 0

    while valid_response == 0:
        print("Which action would you like to perform on the carousel database? (numeric answer)")

        # Output the dictionary of possible actions to user
        for key, action in possible_actions.items():
            print("{num}. {action}".format(num=key, action=action))

        try:
            user_action = int(input("Action: "))

            # Depending on user's response, output the value belonging to that key (integer value corresponding to index (+1))
            if user_action in range(1, len(possible_actions)+1):
                print("Okay, we gon {action}".format(action=possible_actions[user_action]))
                valid_response = 1

            # Inform user that program expects a certain data type if don't provide acceptable input
            else:
                print("Expecting integer input corresponding to list position of possible actions.\n")

        # Handle any errors and output error message to user
        except Exception as error_message:
            print("Something went wrong: {message}".format(message=error_message))
            print("Expecting integer input corresponding to list position of possible actions.\n")

    return possible_actions[user_action]

def get_filename():
    print("What is the name of the file? (no extensions)")
    filename = input("Filename: ")

    return filename

def confirm_additions_to_database():

    ready_to_add = "-"

    while True:
        print("Are these elements ready to add to the database?")
        ready_to_add = input("(Y)es or (N)o: ")

        if ready_to_add.upper() == "N":
            print("Elements will not be added to the database. Returning to action select...\n")
            return 0
        elif ready_to_add.upper() == "Y":
            print("Elements will be added to the database... Let's continue.\n")
            return 1
        else:
            print("I'm expecting either 'Y' or 'N' as input to confirm/deny the addition of the above content.\n")

def main():

    # Returns the dict value corresponding to user's desired action on the database
    while True:
        possible_actions = {1: 'add', 2: 'edit', 3: 'delete', 4: 'exit'}
        user_action_on_db = get_user_action(possible_actions)

        if user_action_on_db == possible_actions[1]:
            print("First, we need to know where the content is coming from...")
            filename_of_info = get_filename()

            # Get all of the database contents (col names and field values for each row)
            collection_of_packages = collect_elements_to_be_added(filename_of_info)
            
            user_confirmation = confirm_additions_to_database()

            # If user approves of database additions...
            if user_confirmation == 1:
                print("Let's add the elements, commit changes, and return to action select.")
                db_filename = input("what is the filename of the database to which you'd like to add? (no extensions please!) ")
                connection = connect_to_db(db_filename)
                print("What is the name of the table you would like to add to?")
                #table_name = input("Table name: ")
                table_name = "CarouselTable"

                for package in collection_of_packages:
                    carousel_database = CarouselDatabase(connection, table_name)
                    add_elements_to_database(package, carousel_database)

                carousel_database.package_elements_from_db()

                commit_and_close_connection(connection)

            # If user does not want to add the collected elements...
            elif user_confirmation == 0:
                print("Abandoning changes and returning to action select...\n")

            # Handle weird stuff...
            else:
                print("Something went wrong. Restart the program and try again...\n")

        # Still developing... Not sure if will let edit, or force them to edit txt file themself?
        # OR... offer to write to text file?
        elif user_action_on_db == possible_actions[2]:
            print("To edit the database, I suggest you alter its corresponding .txt file.")
            print("This way, if anything happens to your table, your changes are not lost.")
        
        # Not sure if this works yet... Just add stuff for now
        elif user_action_on_db == possible_actions[3]:
            db_filename = input("what is the filename of the database that contains the table you'd like to delete? (no extensions please!) ")
            connection = connect_to_db(db_filename)
            print("What is the name of the table you would like to delete?")
            table_name = input("Table name: ")
            carousel_database = CarouselDatabase(connection, table_name)

            print("WARNING!\nTHIS WILL DELETE THE ENTIRE TABLE.")
            user_delete_confirm = "-"
            while True:
                print("Would you like to proceed?")
                user_delete_confirm = input("(Y)es or (N)o: ")

                if user_delete_confirm.upper() == "N":
                    print("Table WILL NOT be deleted. Returning to action select...\n")
                    return 0
                elif user_delete_confirm.upper() == "Y":
                    print("Table is being deleted...\n")
                    carousel_database.delete_table()
                    return 1
                else:
                    print("I'm expecting either 'Y' or 'N' as input to confirm/deny the deletion of the table.\n")

            print("Table has been successfully deleted. Returning to action menu...")

        # Exit the program if the user is finished with altering the database
        elif user_action_on_db == possible_actions[4]:
            print("Alright, see ya later!")
            exit()

if __name__ == '__main__':
    main()