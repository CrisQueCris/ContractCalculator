How to run the app:

1. run python app.py

2. Open URL (standard: http://127.0.0.1:8050/) shown in Terminal in your browser


Main Module: app.py
Scraping: ModulScrapeWallstreet.py
Database: contrcalc.db

About:
# ContractCalculator
Final project for Ironhack Bootcamp Fulltime March 2022

Projectmanagement: Trello-Jira Board

https://trello.com/b/m4rJHzsW/final-project

Introduction to the topic of Agricultural Commodity Markets:

Farmers are price takers on the global market and need to mitigate their price risk. Commodities such as corn, wheat and barley are sold on global markets and prices are volatile and influenced by a number of factors. Naturaly price is infuenced by demand and supply. Supply is mostly influenced by wheather and climate conditions and can differ strongly around the world. The US might have a wet summer, while Europe suffers under a dry period. In one region grain has to fight pests caused by humid condition, in another region grain can't develop properly due to lack of water supply. Currently we see that politics can influence the market situation.  Wars were always fought with the with the supply of food in mind. 

Next to the market risk a farmer also face their own harvest risk. A late strong weather event is able to distroy a years worth of hard work. If this is a very local event and other farmers around the world have a great harvest the farmer will even face low prices for the little harvest they brought in.

Luckily instruments were developed in order to help farmers to mitigate their risk. This is among others mainly the futures market, an over the counter (meaning not standardised) financial derivate. While the commodity market displays current prices for direct sells and buys, the future market displays a price for a buy or sell in the future. Prices of futures are dependent on the time frame (two month from now, in half a year, in two years) and may differ a lot, as market participants try to anticipate the supply in this period. It has to be said here, that not only suppliers try to mitigate risk over the futures market but also buyers such as mills. While farmers want to make sure they will be able to sell their product for a good price, the mills need to look for low prices and make sure that they will have enough supply to be able to produce. 

A farmer will start looking for a good future price once they have sown their seets and the plants start growing. However they will not sell all their potential harvest at once, because they can never be sure how much harvest they wil eventually end up with. So over the course of the year they will make new contracts in steps. A rule of thumb is to end up with a contraction of 30% percent of the harvest. This is due to the fact that prices can change drastically after harvest depending on the result of the harvest. When it turns out that global harvest was not as good as expected the price might rise 50 percent in a week. A farmer will never forget  the lesson when already contracted all their harvest before hand they will be forced to a much lower price while their neighbour profits of the double.

As has been shown farmers need to anticipate market price and at the same time anticipate their own possible harvest. And of course they need to know how much they actually have already sold. Because selling to much they will have to buy wheat them selves in order to be able to fullfill their contract. 
With this project we are supplying the farmer with a helpfull tool in order to plan their sells. 
The farmer has an ower view over the current market situation on a selected futures market and it's past development. Paralely they enter how many hectares of land they planted and how much harvest they currently expect per hectare. 
Everytime a contract is made the amount and time of sell is entered by the farmer and it is displayed next to the total harvest. Using this tool the farmer can always see how much they have already sold and how much they can anticipate to sell to the current market price. 

As a future addition to the application we want to add price prediction mechanisms as well as geograpic field data with remote sensing in order to have a better overview of their fields and to be able to more precisely anticipate harvest.



## Flask
In a Future Version the app can be deployed using Flask
How to start FLASK server:



1. Start virtual environment contractenv
    MAC: $ . contractenv/bin/activate
    WIN: > contractenv\Scripts\activate


2. Start Server:

Bash: 
$ export FLASK_APP=flaskcontr
$ export FLASK_ENV=development
$ flask run

Powershell: 

> $env:FLASK_APP = "flaskcontr"
> $env:FLASK_ENV = "development"
> flask run

CMD: 
 set FLASK_APP=flaskcontr
 set FLASK_ENV=development
 flask run