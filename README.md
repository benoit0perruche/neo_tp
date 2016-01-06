#Neo4j Homework
**By A. Lafanechere & Benoit Perruche**
##Introduction
Being electronic music lovers we tried to model relationships betweens Djs, and 4 well known european night clubs : La Belle Electrique (Grenoble), Concrete (Paris), Fabric (London), Berghain/Panorama Bar (Berlin). 

We also added to those data the tracks released by these djs and the Boiler Room videos they may be featured in. Boiler Room is a YouTube channel broadcasting live mix of trendy djs. We finally added the Top 100 of best djs according to a poll on Resident Advisor.

Event data are confined to 2015.

We built our csv datasets from [Resident Advisor](http://residentadvisor.net), [SoundCloud API](https://developers.soundcloud.com/docs/api/guide) and [YouTube API](https://developers.google.com/youtube/).
We decided not to provide the scraping code for data retrieval, because we thought it was out of the scope of the homework.

##Data model
<pre><code>       ┌─────────────┐                                  ┌───────────────┐
       │   Top 100   │                                  │    Country    │
       │   * year    │                                  │   * name      │
       └─────────────┘                                  │               │
              ▲                                         └───────────────┘
              │                                                 ▲
              │                                                 │
              │                             LIVES_IN            │             IS_IN
              │                                1-1              │              1-1
              │                 ┌───────────────────────────────┴────────────────────────────┐
              │                 │                                                            │
FEATURED      │                 │                                                            │
  *rank       │                 │                                                            │
   N-N        │                 │                                                            │
              │                 │                                                            │
              │       ┌───────────────────┐              ┌──────────────┐            ┌──────────────┐
              │       │        Dj         │              │     Event    │            │    Venue     │
              │       │                   │              │              │            │              │
              │       │ * id              │  PLAYED_AT   │              │   HOSTED   │ * name       │
              └───────│ * name            │     N-N      │ * event_id   │     1-N    │ * address    │
                      │ * style           ├────────────▶ │              │ ◀──────────│              │
                      │ * soundcloud url  │              │              │            │              │
                      │                   │              │              │            │              │
                      └─────────┬─────────┤              └────────────┬─┘            └──────────────┘
                       PRODUCED │         │                           │
                          N-1   │         │                           │          HAPPENNED
                                │         │                           │             N-1
                                │         └────────────────────────┐  └───────────────────────────┐
                                │                 PLAYED_AT        │                              │
                                │                    N-N           │                              │
                                │                                  │                              │
                                │                                  │                              │
                                │                                  │                      ┌───────▼──────┐
                                ▼                                  ▼                      │     Day      │
                     ┌────────────────────┐              ┌───────────────────┐            │              │
                     │       Track        │              │    BoilerRoom     │            │  * date      │◀─┐
                     │                    │              │                   │            │              │  │
                     │ * title            │              │ * title           │            └───────▲──────┘  │
                     │ * duration         │              │ * view_count      │────────────────────┘         │
                     │ * playback_count   │              │ * like_count      │     HAPPENNED                │
                     │ * permalink        │              │ * permalink       │        N-1                   │
                     │                    │              │                   │                              │
                     │                    │              └───────────────────┘                              │
                     └────────────────────┘                                                                 │
                                │                                                                           │
                                │                                                                           │
                                └───────────────────────────────────────────────────────────────────────────┘
                                                                    RELEASED
	                                                                       N-1</code></pre>

##Instructions
Before diving in the graph we designed you need to have a running instance of Neo4j, preferably locally on the default port (7474). 
To import our data in the graph you have two options :

* run an instance of Neo4j from our dump that you can download [here](https://www.wetransfer.com/downloads/635a6b542f56bfa2932fcf9a3bbe422520160105171050/94e440e4db534287cc494f8db3fbadb520160105171050/2bd279)
	* username : neo4j
	* password : neotp
	
* execute the `main.py` python script. It will parse the csv files and create constraints, indexes, nodes and relationship thanks to `py2neo`. But this option will take a long time ! Do not forget to install this dependency :  `pip install py2neo`.

##Uniqueness constraints
Here are the primary keys we defined for our nodes.

* **Dj.dj_id**
* **Country.name**
* **Club.ra_id**
* **Event.event_id**
* **Track.permalink**
* **Day.date**
* **Top100.year**

##Indexes
We chosed to create indexes for :

* **Day.date**, in order to be able to efficiently query time series
*  **Club.name**, **Dj.name** to quickly retrieve information about the entities like the artists or the nighclubs
* **Track.playback_count** and **BoilerRoom.view_count** to be able to do query related to artists notoriety 
 
 Because we defined uniqueness constraint, Neo4j created indexes  on the fields we wanted to be unique.
 
##Complex queries

**Create a playlist of 10 tracks for La Belle Electrique, ordered by playback_count, avoid long tracks because they are probably mixes, we want only real tracks**
```
MATCH (club {name:"La Belle Électrique"})-[:HOSTED]->(event)<-[:PLAYED_AT]-(dj)-[:PRODUCED]->(t:Track) WHERE t.duration < 600000
RETURN t ORDER BY t.playback_count DESC;
```

**List the Djs featured in the Top100 that played at La Belle Electrique**
```
MATCH (club {name:"La Belle Électrique"})-[:HOSTED]->(event)<-[:PLAYED_AT]-(dj)-[:FEATURED_IN]->(Top100)
RETURN DISTINCT dj.name;
```

**Find the number of Dj that ranked in the Top100 for each nightclub** 
```
MATCH (club)-[:HOSTED]->(event)<-[:PLAYED_AT]-(dj)-[:FEATURED_IN]->(Top100)
RETURN club.name, count(DISTINCT dj.name) AS numberOfDj ORDER BY numberOfDj DESC;
```

**List the Djs that played at la Belle Electrique and did a BoilerRoom**
```
MATCH (club {name:"La Belle Électrique"})-[:HOSTED]->(event)<-[:PLAYED_AT]-(dj)-[:PLAYED_AT]->(BoilerRoom)
RETURN DISTINCT dj.name;
```

**Find the 10 djs with the more playback_count on their tracks and Boiler Room view_count**
```
MATCH (b:BoilerRoom)<-[:PLAYED_AT]-(dj)-[:PRODUCED]->(t:Track)
RETURN dj.name, b.view_count+t.playback_count AS popularity ORDER BY popularity DESC LIMIT 10;
```

**List the Djs that played in the 4 nightclubs in 2015**


**List the Djs that played more than one time, for each nightclub** 
(Pas bon pour l'instant)
```
MATCH (dj)-[:PLAYED_AT]->(b:BoilerRoom)
RETURN b.title, dj.name;
```
**List the 10 most popular track with the Dj name and their top100 rank (optionnal) (and avoiding mixes)
```
MATCH (dj)-[:PRODUCED]->(t:Track)
OPTIONAL MATCH (dj)-[f:FEATURED_IN]->(Top100)
WHERE t.duration < 600000
RETURN dj.name, t.title, t.playback_count, f.rank ORDER BY t.playback_count DESC LIMIT 10;
```

