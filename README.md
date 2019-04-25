# The Global Online Cookbook
## Project by Alex Thirlwell

The Global Online Cookbook is a Data Driven, Flask application that has been built using Python, HTML and CSS, as well as some JQuery to provide a simple application that will enable a range of users to effectively manage their recipes online. Once you have registered your username and password, you will be able to browse a range of different recipes that have been submitted by other users, as well as create your own and interact with recipes by ‘Liking’ or ‘Disliking’ them. The recipes have been split into different categories to enable the user to find a recipe based on ‘Food Type’ or ‘Continent’.  

Each recipe has two views: one view will give you an overview of the ingredients and cooking instructions and an indication of the recipes popularity from the ‘Likes’ and ‘Dislikes’ it has received. The other will give you more detailed information about the recipe, such as, cooking time and any allergens it contains. The user can also ‘Like’ or ‘Dislike’ the recipe by clicking the buttons at the bottom of the view page. Users can also submit their own recipes, and they can track their recipes by navigating to the ‘My Profile’ section of the application.  

## UX

For this project I identified three user stories, each involving a hypothetical user who represented one of three different demographics: a ‘Home Cook’, a ‘Professional Chef’, and a ‘Busy Parent’.

### User 1 - A ‘Home Cook’ who cooks as a hobby and enjoys trying new recipes and flavours.

This user is someone who likes to experiment while they cook, try different flavours, as well as provide meals for friends and relatives. They will want an experience that allows them to find new and exotic dishes that will test their skills, while providing an enjoyable cooking experience. They will also want to catalogue their favorite recipes so they can quickly reference any recipes that they want to revisit.

I met this user’s needs by developing the application to quickly navigate between different cuisines and ingredients. If the ‘Home Cook’ wants to try a ‘South American’ dish, for example, they can navigate to the relevant page and scroll through the overview and get a sense of the complexity and the ingredients needed for the recipe. The ease of readability when looking at full recipe will enable the user to have the instructions open on any device and read the recipe whilst attempting to make the dish they have selected.




### User 2 - A ‘Professional Chef’ who likes to investigate new cuisines to expand their skills and provide new and exciting dishes to the public.

This user is someone who works as a chef and needs to keep up to date with flavour combinations and styles to make sure they are providing an exciting dining experience to their patrons. They will want to explore flavours easily, and they will also need to document their creations so that they can recreate them and refine them until they are perfect.

I met this user’s needs by enabling an easy filter between ‘Continent’ and ‘Food Type’. This enables the user to take what they know already and combine that with new flavours from a different region, or a new way of seasoning a particular ‘Food Type’. They will also be able to add their own recipes to the system, see the user feedback on the recipes, and edit the recipe until it is perfect and ready to be sold in their restaurant.

### User 3 - A ‘Busy Parent’ who needs quick and easy recipes that can be found by searching for a specific ingredient so they can make tasty and nutritious meals for their children.

This user is someone who does not have much time to cook elaborate meals and they also need to be able to judge that the meals will be healthy and nutritious. They will need to be able to add a recipe to the cookbook so that they can quickly reference the recipes. This will allow them to plan the meals they will create in advance and therefore minimize the times spent preparing meals for hungry and impatient children. They will also need to be aware of any allergens within the recipes to avoid young children accidentally consuming an allergen by mistake.

I have met this user’s requirements by creating a page that gives them important information such as: a cooking time, so that they can understand the amount of time that will be invested in cooking the meal. The ingredients list is included on both the simple overview, and full view of each recipe. This will allow busy parents to see the ingredients so they can avoid recipes that contain ingredients that their children do not like, and the online nature allows them to access the cookbook at any time and refer to the recipes they want to make. On the view of the recipes it will clearly show whether the recipe has an allergen within it or not.

## The Design Process

I designed the project using the wireframes that are available here: https://drive.google.com/open?id=13XeuSf7rnc4y5ugOBmQDoJWjpyIEZpIb

The Database Schema can be seen here – https://github.com/KillTheDJ94/global-cookbook-application/blob/master/global_cookbook_design_documents/Global%20Cookbook%20Database%20Schema.pdf 

This file shows the basic structure of the database and shows how the application stores user-submitted data. The file reflects the exact structure of the MongoDB database.
All of the features and design elements referred to in this document correspond with the annotations used on the wireframes. This was done deliberately to make my design and development process easy to understand for anyone who wants to develop an online cookbook.

I wanted to add in some basic authentication as I could see a range of features that could be added to help make the user experience cleaner. To start authentication, I needed to implement a login form (see Login Form Page Design wireframes) that was easy and intuitive to use, and the registration page was designed with a similar mindset. For each user the login and registration process is made as easy as possible to allow all users to register, and login whenever they need to visit use the application. Users who have a login for the cookbook can like/ dislike a recipe, upload/edit/delete their own unique recipes and see the likes/ dislikes that other users have given to all the recipes within the Global Online Cookbook. This is particularly useful for User 1 and User 2 who will be able to view the likes and dislikes on the recipes they have created.

When designing the Global Online Cookbook I designed each individual recipe to include a simplified view (see “All Recipe” Page Design wireframes) and a detailed view (see Recipe Page Design wireframes). This was chosen because it focuses on the needs of all of the identified user types as outlined above. Each user will get a direct benefit from the differing views. User 1 will be able to quickly refer to the instructions and ingredients while cooking, User 2 will be able to get an overview of the flavour combinations in the recipe to expand the dishes they can offer to their customers and User 3 will be able to quickly understand the ingredients to make sure the meal is healthy and nutritious for their children.

The homepage was a later addition to the design process, and was added as a way of tying together the whole theme of the application. The idea of a Global Online Cookbook came from the classification of ‘Continent’ as a way to group together recipes. This then led to having a home page (see Home Page Design wireframes) that allows the user to navigate to one of the ‘Continent’ pages by clicking on an image that relates to the continent itself. User 1 would be able to use this as an entry point into looking for their next recipe. User 2 will be able to select which region they want to take inspiration from, and User 3 can search for recipes quickly by selecting the continent or can also navigate to other pages using the Navigation Bar at the top of the page.

The design of the recipe form was built by recognising all of the information a user would need to record a complete recipe that is useful to other users. With this in mind, I created a form that requires the key information, while also being simple and informative to follow ( see “New Recipe” Form Design wireframes). By requiring the ‘Continent’ and ‘Food Type’ within the form, it ensures that each recipe falls into both of these filters to maximise its visibility. This enables all users to navigate to the types of recipes they are interested in, whether that is based on ingredient or the continent origin of the cuisine used in the recipe. User 1 is looking for recipes that will be exciting and exotic, User 2 is looking for inspiration and User 3 is looking for recipes that will be quick and easy to prepare. The design of the form enables all users to get exactly what they need from the application.


## Features

### Current Features

Authentication - a simple login system that allows users to login or register an account. This can be viewed on the “Login Page Design” wireframes.

Add Recipe - any user can create their own recipes to the Cookbook by filling in a simple form that stores all of the necessary information. This form can be seen in the “New Recipe Form Design” wireframes. This cannot be saved until all of the necessary information has been added. 

Edit Recipe – a user can edit their own recipes on the system, they cannot edit recipes that were not created by them. This will allow them to resolve any typos, or change the recipe if they have added/removed ingredients or refined the recipe in any way.

View Recipe - any user can view any individual recipe. Each recipe has 2 views that will give different information to help the user. The basic view will give the user an overview of the ingredients and instructions for the recipe, this can be viewed on the “All Recipes Page Design” wireframes and a more detailed view that will give them allergen and cooking times for the recipes. This can be seen in the “Recipe Page Design” wireframes. 

Like Recipe - any user can give positive feedback to any recipe.

Dislike Recipe - any user can give negative feedback to any recipe.

Stats - any user can see an overview of the recipes that have been added to the system.

Add Allergens - any user can add allergens to the system so that the recipes provide accurate allergy information.

User Profile - each user can see the recipes they have added to the system. They can then edit or delete their recipes from this page.

### Features to add

Comments - it would be useful to add a comments system to the application to enable users to interact and give more feedback on recipes.

Email interaction - keep users updated when someone likes or dislikes one of their recipes. This would also help when comments are integrated onto the system.

Image uploads - allowing users to upload images would give a better experience to the application and allow a greater community to be built around sharing recipes and trying dishes that look tasty.

Text Searches - allowing users to search and filter results in a more precise way will help them find specific recipes quicker, especially when more recipes get added to the system. This could be done by allowing multilayered searches that display for example all “chicken recipes” from “Asia” that do not contain “peanuts”.

## Technologies used

This project used Python, Flask, HTML, CSS, JQuery, Pygal, bcrypt, MongoDB and the Materialize library.

Python and Flask: these technologies are used together to provide clean routing within the application. These technologies allow the application to display the required information from the MongoDB backend.

Materialize, HTML and CSS: These help present the application in a clean and responsive way that provides each user with an application that is responsive to their needs.

Pygal: This provides the users with statistical analysis of the recipes that have been uploaded which enables users to see more information about the application.

Bcrypt: This provides the authentication system so that users can login and track their recipes when they have been added to the application.

## Testing

The main method of testing for this application came through manual, “in-browser” testing. From the outset, I was using the browser to test each individual route that was added to the application. This enabled me to quickly identify any issues that arose when navigating through the application. For example, when I was implementing the Home Page (see “Home Page Design” wireframes) I could test that each image was linked properly, and that each page the user navigated reflected a unique styling that would help the user differentiate between one page and another. This was also helpful when I was implementing different features to the application. For example, I could properly test that the pagination was working on each page by testing that the relevant buttons appeared when a certain number of results were present, and that the application would move to the correct page when the buttons were pressed.

Manual testing was also helpful when I was checking that the database was properly connected to the Flask application, and that each process within the application worked as it should. By going through the process of adding a recipe, I could see how this information was represented in the database, which in turn helped me to create the correct views to style the information in a way that was most effective for the different users. I could then see that it had been added to the correct ‘Continent’ and ‘Food Type’ classifications. From this point, I could then test that the view which was displayed, was correct and corresponded to the information shown in MongoDB. From there, I could then test that the ‘Like’ button worked by checking the record in the database, and on the frontend view of the recipe overview. 

When creating the “Stats” page, I discovered that there was an issue with using SVG images when testing the application on IE and Edge. Due to the security protections on both of these browsers, it would not allow the SVG images to load. To rectify this, I had to change the “<embed>” tag to an “<img>” tag. I noticed that this caused a further problem because the application no longer showed the values for each of the bar charts when the cursor hovered over them. To rectify this issue, I manually added in the label for each chart so that it fixed the value to the individual bars of the chart.

Each stage of the Data Driven application was easily tested to ensure that the routes were set up correctly, and the connections to the Database were established to ensure the application was fully operational and easy to use. 

### Mobile testing 

To ensure that the application was effective on as many devices as possible, I tested the app on the mobile versions of Chrome, Mozilla Firefox and Samsung Internet. Across all of these browsers there were no issues as the app is built to be responsive to all screen sizes.

## Deployment

The application has been deployed to Heroku and is found at - http://global-cookbook-application.herokuapp.com/ 

You can login using the following details:

Username: Alex

Password: password

Or feel free to register your own account.

Before attempting to deploy to Heroku I needed to create a requirements.txt file that lets Heroku know which packages it needs to install. A Procfile is also required which lets Heroku understand the environment that it needs to setup. 

Once these documents have been created, they were committed to Github. From here, Heroku could connect to the Github repository and prepare to deploy the application. Before the application could be fully launched, the variables had to be configured within the Heroku dashboard. The following variables were added:

IP 0.0.0.0
PORT 5000
MONGO_URI
SECRET_KEY

## Credits

Recipes
All of the recipes came from sources on a range of sites: The Food Network, BBC Good Food, Jamie Oliver, Delicious.au, Veganuary, Myrecipes

## Media
Home page images Europe, Asia, Africa, South America, North America, Australia

User login via bcrypt tutorial - (1) Creating a User Login System Using Python, Flask and MongoDB - YouTube

