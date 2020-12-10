# Coffee Shop Full Stack

## Full Stack Nano

The application has the following features:

1) Displays graphics representing the ratios of ingredients in each drink.
2) Allows public users to view drink names and graphics.
3) Allows the shop baristas to see the recipe information.
4) Allows the shop managers to create new drinks and edit existing drinks.

## About the Stack

It is desiged with some key functional areas:

### Backend

The `./backend` directory contains a Flask server with a SQLAlchemy module for data needs.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server. Update the environment variables found within (./frontend/src/environment/environment.ts) to reflect the Auth0 configuration details set up for the backend app. 

[View the README.md within ./frontend for more details.](./frontend/README.md)
