## Long Term Objective:
Make an application where peoples activity locations will show up as "paint" a user should be able to
compete with friends to see who can 'paint' the most of the area within the specified time range.

### Short term To do:
- [x] Get Strava API working
- [x] Find GIS map api to overlay info
- [x] Combine api into GIS map 

### Long Term to do:
- [x] Create 'paint' interface including ability to choose time frame, specify colours, etc.
  - Ignoring time frame parsing for now
- [x] Get django running (or consider using streamlit?)
- [ ] add stats page
- [ ] add about me/contact page
- [ ] add a "about the project" page
- [ ] upload to heroku
- [ ] create a readme file for the project
- [ ] create a medium article for the project

### Maybes:
- [ ] Add 'bonus point' locations that cycle every 24 hours
- [ ] Seperate biking/walking/running
- [ ] bar chart race animation by team (https://12ft.io/proxy?q=https%3A%2F%2Ftowardsdatascience.com%2Fcreate-a-bar-chart-race-animation-app-using-streamlit-and-raceplotly-e44495249f11)
- [X] remove 'odd' routes pathways, potentially needing each individual coordinate to be within a few meters of eachother
- [ ] Make starting area shown on map relevant to users activities