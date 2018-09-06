from views.dynamic_carousel import CarouselDatabase, connect_to_db, commit_and_close_connection
from flask import Flask, request, render_template, redirect, url_for

def package_featured_content(featured_id, title, content, num_elems):
    
    package = {
        'featured_id': featured_id,
        'featured_title': title,
        'featured_content': content,
        'featured_num_elems': num_elems
    }

    return package

def main():
    app = Flask(__name__, template_folder='templates')

    @app.route('/')
    def index():

        all_featured_packages = []

        # This is the featured content I'd like to show -- could make this dynamic later (ie. read from file)
        featured_content_info = {'featured_projects': "Featured Projects", 'featured_blogs': "Featured Blogs"}

        for db_name, featured_content_title in featured_content_info.items():
            db_filename = "views/{}".format(db_name)

            connection = connect_to_db(db_filename)
            table_name = "CarouselTable" # This will change later... just for now
            carousel_database = CarouselDatabase(connection, table_name)

            # Gets all elements (ie. title, description, etc.) from the database and return as dictionary
            featured_content_from_db = carousel_database.package_elements_from_db()

            num_elems_in_featured_content = len(featured_content_from_db)

            # Package up all of the featured content elements that have been collected
            featured_content_packaged = package_featured_content(db_name, featured_content_title, featured_content_from_db, num_elems_in_featured_content)

            # Add the final package to a list that contains all the other featured content packages
            all_featured_packages.append(featured_content_packaged)

        commit_and_close_connection(connection)

        return render_template('homepage.html', all_featured_packages=all_featured_packages)

    app.run(debug=True, port=5000)

if __name__ == '__main__':
    main()