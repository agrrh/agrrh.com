Title: MissionBread
Date: 2016-01-23 01:09
Tags: pygame, games, aim

Couple of days ago I finished a simple game. It was inspired by MissionRed reaction-training game, implemented in Flash.

[ [GitHub](https://github.com/agrrh/missionbread) ]
[ [latest executable](https://raw.githubusercontent.com/agrrh/missionbread/master/missionbread) ]

![preview]({filename}/media/missionbread-screenshot.png)

MissionRed was the first reaction game I used to keep my e-sports form up.

Currently I was able to found it available here, but this is not the original project for sure: [MissionRed @ NaVi-Gaming](http://play.navi-gaming.com/games/counter-strike_go/missionred)

About a year or two ago I stated something like "Implement my own MissionRed" as one of the goals, just in case of spreading the knowledge horizons. It took kinda long to start the project, but here it is, at last. To be honest, it was written in just about couple of hours.

So, here it is!

MissionBread:

- Requires Python and PyGame installed
- It doesn't punish player for skipping targets, but adds full target lifespan to the average reaction time
- Game counts click on two crossing targets as 2 hits in 1 shot, yay!
- It is endless, use "q" or "Esc" to stop the madness
