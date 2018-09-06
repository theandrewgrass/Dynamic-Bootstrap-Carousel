# Dynamic-Bootstrap-Carousel
A flask website that uses elements from a database to populate contents in a bootstrap carousel.

## First
Download all the dependencies listed in the requirements.txt file

## Second
Run dynamic_carousel.py (*in views*) and **add** the elements from **projects**. Confirm the addition of the contents (**y**) and use the filename, **featured_projects** for the database (if you do not use this filename, the program will not work -- this will be fixed later on). Do the same for blogs, but use  **blogs** as the input file, and **featured_blogs** as the database filename.

## Third
You are now ready to nagivate to main.py and run it. You should see "*Serving Flask app "main" (lazy loading)...*" come up in the command line.

## Fourth
Open your browser of choice and enter the following into the address bar: http://localhost:5000/

## Fifth
Enjoy the content that was dynamically loaded into the web page from a database.
> You're a lizard, Harry.

### You can add more content to each carousel by editing the provided .txt files (projects, blogs). Make sure that you maintain the proper format (ie. *'###'* to begin a new slide, etc.) or else it will not function properly. Keep in mind the current content that is present in the database -- if you don't delete it, it will still be there. So, if you deleted items from the .txt file and are still seeing them in the webpage, it's because they are still in the database.
*Deletion feature in dynamic_carousel.py will drop the table, but will not delete the file for you. This will be added later.*

*Note: If you would like to add more carousels, you would need to make an additional file (.txt) containing all of the relevant information (model from the provided .txt files), and you would need to edit main.py on line 24 to include another dictionary entry with the to-be database's name as the key, and the title of the content as the value.*
