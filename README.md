# First Principles Publishing take home task

## Requirements
- Creating a new blog post

- Retrieving a list of all blog posts

- Retrieving a single blog post by its ID

- Updating an existing blog post

- Deleting a blog post

- Creating a new blog post

- Users should be able to sign up, sign in
- Requests to create, update, or delete blog posts should be authenticated by the user that owns the post


## Running the application
First, clone or download the application onto your local machine. Once completed, `cd` into the directory containing the `Dockerfile` and the `run.sh` file. To run the app, enter `sh run.sh` to spin up the docker container running the app. The website should then be accessible at `http://127.0.0.1:5100/ `on your local machine. 

## Running migrations for the application

`flask db migrate -m "<migration_name>"`

## Interacting with the website

The website is a basic website that provides all the functionality described in the above requirements. Upon a user's first visit to the website, they will be greeted with a list of the blogs currently available. For simplicity, 10 blogs have been randomly generated and assigned to users. The exact implmenetation of this can be found in the `seed_db()` function in `blog_api/api.py`.

To test authentication behavior, you can signup as a new user on the home screen, or use one of the two provided user profiles.
To login to either of the provided accounts, you can login using the usernames and passwords `user1`, `password1` and `user2`, `password2` respectively for users 1 and 2.

Once logged in, a user is able to create, edit, and delete posts that they own, while still being allowed to view posts made by other users. To do this, click on a post that you own, as indicated by the username on the right side of a row. This will take you to the blog view page where you can edit or delete a pre-existing post. To create a post, you can click on the new post link found on the home page and profile page.

Upon signing up, users are redirected to their profile. There is not much distinction between the profile and homepage, so it's best differentiated by looking at the url. 

## Considerations and areas for improvement

The css could definitely be improved, but for a take home I was focused on delivering functinality over style. Were this in production, i would clearly spend more time perfecting the CSS.

Similarly, the passwords are currently stored as plain text. This is obviously a huge security flaw, but for a simple example it should do. In a production scenario, the passwords would need to be hashed/SALTed before being stored in the database to ensure plaintext passwords aren't at risk of being exposed should the system ever get hacked. 

Additionally, the system does not currently restrict a username to a single user, thus opening up another security vulnerability. To fix this, the username column should either be made unique, or the username should be made the primary key in general.
