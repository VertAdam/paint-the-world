# Paint the World
![](https://drive.google.com/uc?export=view&id=1N9EbVyUTWVCz8F084CRYY4rErKRPYLt-)
Paint the World is a dynamically updating map that takes users Strava activities and plots their activity locations onto a variety of maps.

It works by dividing the world into cells and then determining all the cells you have walked/biked/frolicked through and colouring those with the colour of your choice.

The available maps are:

- **Full Painting**: A map with all cells travelled through by any user coloured in that users colour 
  - If two or more users have travelled on the same cell, the user whose activity was most recent will colour the cell
- **Your Painting**: A map with all of the cells you have travelled through coloured in your colour
- **You vs The World**: Identical to the Full Painting except it makes ever other users cell coloured black, letting you see more clearly your contribution to the full painting
- **Stats (coming soon)**: This displays a variety of statistics including the number of cells you've painted on the full-painting, your total cells painted and total amount of colour painted on each map
  - I hope to add more advanced statistics when enough activity data has been uploaded (i.e. Rural vs City cells, most commonly visited cells, etc.)
- **Groups (not currently implemented)**: Allow you to select users that you want to create a painting with, this will then create a map equivalent to a Full Painting but only including your friends
    To get started, connect to strava by clicking on the blue button at the top right.

## About
After graduating from University of Waterloo in April me and many of the friends I have made from my time at University were moving onto the next stage of our lives. For many of us, this meant relocating for work. 

In the months following my graduation I spent some time working on a personal project in which I created a website to connect all of our smartwatch activity data and plot it onto an interactive world map. I called the website "Paint the World" with the end objective to see how much of the world we can "paint" with our activities. Each person can select their own colour and whenever an activity is  recorded through Strava , that persons activity data will be uploaded to our shared map. This way, whether we are in different provinces, countries or even continents, we still have a level of connection in this map of our collective travels.




## TODO:

### Short term To do:
- [x] Get Strava API working
- [x] Find GIS map api to overlay info
- [x] Combine api into GIS map 

### Long Term to do:
- [x] Create 'paint' interface including ability to choose time frame, specify colours, etc.
  - Ignoring time frame parsing for now
- [x] Get django running (or consider using streamlit?)
- [ ] add stats page (total amount painted by user, location data, etc.)
- [x] add about me/contact page
- [x] add a "about the project" page
- [x] upload to heroku
- [ ] create a readme file for the project
- [X] create a medium article for the project

### Maybes:
- [ ] Add 'bonus point' locations that cycle every 24 hours
- [ ] Seperate biking/walking/running
- [ ] bar chart race animation by color group (https://12ft.io/proxy?q=https%3A%2F%2Ftowardsdatascience.com%2Fcreate-a-bar-chart-race-animation-app-using-streamlit-and-raceplotly-e44495249f11)
- [X] remove 'odd' routes pathways, potentially needing each individual coordinate to be within a few meters of eachother
- [ ] Make starting area shown on map relevant to users activities
- [ ] Fix database structure, super clunky at the moment
- [X] fix requirements.txt
