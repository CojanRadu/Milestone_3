
# MathIsFun

MathIsFun is a simple application for children beginning to learn simple math. There are lots of variations online, but I wanted to make one more relaxed, without  any time limit, more suitable for beginners. So far there are 4 exercise types available, adding, subtracting, multiply and divide.

[Live Version ](http://milestone3-radu.herokuapp.com)


[Github (clone)](https://github.com/CojanRadu/Milestone_3)
Name: **admin** to login on admin part, any other name will create new user if it doesn't exist 
 
## UX
 The website is aimed for children starting to learn simple math, but they will need the help of their parents who can set up the exercise type and difficulty of the exercises. 
 There is no complex login system, and for simplicity there can be only one admin user.
 If a user logs in with "admin" as username he will be redirected to "admin" part, any other name will be redirected to "exercise" part. Admin settings will be used as a template and the new user will have those options, they can be changed later from admin. 
The website is intended for tablets, touch screen is preferred but touchpad or mouse can be used.
Completing exercises grants "unicorn points" than it's up to the parents how to use those.

The goal of the website is to be able to increase difficulty of the exercises, depending on child's progress. As an example:

- level 1 : answer is shown with 3 options, user only have to click (or touch) the already shown one
- level 2: no answer shown, user have 3 retries, with 3 options shown, there will be no wrong answer in the end
- level 3: no answer shown, 5 options with 1 retry, hint enabled, there are 3 wrong answers
- level 4 no answer shown, no options shown, hint enabled, 2 retries, user will use keypad, can use hint if he doesn't get it right
- level 5: no answer shown, no options shown, no hints, no retries, user have to know the answer to get it right


A simple diagram showing user input and flow:![Simplified flow diagram](https://github.com/CojanRadu/Milestone_3/blob/master/static/doc/chart.png?raw=true)

## Features
Admin user can be implemented on future mongoDB using this template:
[admin mongoDB](https://github.com/CojanRadu/Milestone_3/blob/master/static/doc/admin_mongo.json) 

Admin part:
There is also a option to delete users, that will delete all recorded exercise data for that user.
Each exercise type has the same options: 
![admin settings](https://github.com/CojanRadu/Milestone_3/blob/master/static/doc/admin_options.png?raw=true)	

 - Enabled:  used if exercise type will be available for users, if not the top menu link will be disabled:
<img src="https://github.com/CojanRadu/Milestone_3/blob/master/static/doc/01-enabled_02.png?raw=true" alt="Substract option disabled" width="250">
- Show answer:  shows correct answer on exercise, aimed at very beginners to familiarize with new numbers:
<img src="https://github.com/CojanRadu/Milestone_3/blob/master/static/doc/show_answer.png?raw=true"   width="250" alt="Show answer ebabled">

- Can be inverted: for example if available operation numbers is only 5 and inverted = checked, than it can show [5 + (any nr. between 0 an 12)] OR [(any nr. between 0 and 12) + 5], if inverted = NOT checked than it can only show [5 + (any nr. between 0 an 12)]. This option is disabled for subtractions and for division
- Answer type: Input Box (users will use on-site keypad to input answers), 3 Options will show 3 check-boxes, 5 options will show 5 check-boxes
![answer types](https://github.com/CojanRadu/Milestone_3/blob/master/static/doc/input_box.png?raw=true)

- Nr. of retries: 1 - one answer / question, 2 and 3 users can have another (or two more) goes at same question
 <img src="https://github.com/CojanRadu/Milestone_3/blob/master/static/doc/retry.png?raw=true" width="500" alt ="multiple retry">

- Auto-submit answer: user have to use submit button or not:
<img src="https://github.com/CojanRadu/Milestone_3/blob/master/static/doc/autosubmit_off.png?raw=true" width="250" alt="auto off">

- Hit Enabled: clicking on hit will show multiple variants of same exercise:
<img src="https://github.com/CojanRadu/Milestone_3/blob/master/static/doc/hint.png?raw=true" width="250" alt="Hint">

- Nr of exercises: 0 for infinite, anything more than that will show some very simple statistics about the completion of that particular exercise type
<img src="https://github.com/CojanRadu/Milestone_3/blob/master/static/doc/total_nr.png?raw=true" width="500">

### Features Left to Implement
- main feature this application lacks is a clear separation between tasks and exercises, unfortunately implementing tasks was the example on code institute so there was no point to copy-paste for this milestone
- funny images on submitting answers to make it more entertaining for children
- statistics/graphs on admin part to track user progress

## Technologies Used

* The website was built using HTML5 and CSS3. 
* JavaScript was used to build an interactive webpage and to connect to an API.
* Python was used to build the structure and functionality of the back end.
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) was used to display python functions on the website
* [Pymongo](https://pypi.org/project/pymongo/) was used to make the code written in python talk to the database
* [MongoDB](https://www.mongodb.com/) was used as the database host
* [Heroku](https://www.heroku.com/) was used to deploye the live version of the application.
* To make the structure and the site responsive in a simple manner [Material Design Lite](https://getmdl.io/) were used.
* The website as built and developed using VS Code on Linux Mint and Windows 10

* [W3C's HTLM Validator](https://validator.w3.org/) were used to validate the websites HTML code. 
* [W3C's CSS Validator](https://jigsaw.w3.org/css-validator/) were used to validate the websites CSS code. 
* [JSHint](https://jshint.com/) were used to validate the website JavaScript code.


## Testing

Only manual testing was done. Features were implemented mostly one by one than tested, than re-tested after some code refactoring.
User part has one html error "Attribute for not allowed on element ul at this point.", no CSS errors and 51 warnings on javascript.
On admin there is no custom CSS, and only a few lines of javascript.

## Deployment

this project was deployed on Heroku, but I made a clone on github for submission
Deployment on heroku:

Environmental vars: MONGO_URI, IP, PORT
**requirements.txt and procfile**

    sudo pip3 freeze --local > requirements.txt
    echo web: python app.py > Procfile

requirements.txt generate errors on heroku on both linux mint and windows 10, had to delete some lines manually

**bash:**
   
    git init
    heroku git:remote -a milestone3-radu
    git config user.email "cojanradu@yahoo.com"
    git add .
    git commit -m "First Commit"
    git push heroku master

    heroku ps:scale web=1


## Credits 

* [admin template](https://github.com/CreativeIT/material-dashboard-lite)
