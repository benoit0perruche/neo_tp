##Introduction
Being electronic music lovers we tried to model relationships betweens Djs, and 4 well known european night clubs : La Belle Electrique (Grenoble), Concrete (Paris), Fabric (London), Berghain/Panorama Bar (Berlin). 

We also added to those data the tracks released by these djs and the Boiler Room videos they may be featured in. Boiler Room is a YouTube channel broadcasting live mix of trendy djs.

We built our csv datasets from Resident Advisor website and through SoundCloud API.

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

##Set up
Before diving in the graph we designed you need to have a running instance of Neo4j, preferably locally on the default port (7474). 
To import our data you can either launch `main.py`, the python script we wrote to build the graph or run the queries.

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
 
 Because we defined uniqueness constraint Neo4j created indexes  on the fields we wanted to be unique.