### How to play

#### Start game: 
python game.py

#### Song select:
Choose a song by index of the song and press enter

#### Difficulty select:
After choosing a song, choose a difficulty by index and press enter

#### NOTE: THERE IS NO AUTOFOCUS ON GAME WINDOW, CLICK ON THE GAME WINDOW TO GET FOCUS ON IT!

#### Gameplay:
Hit the falling blocks when they are positioned at the HitLine (red bar)

#### Keyboard input: 
Left(Green): S

Left middle(Blue): D

Right middle(Blue): K

Right(Green): L


### Game mechanics

#### HitRating:
Excellent: Hitting the blocks perfectly on the HitLine results in an "Excellent" hit

Good: Hitting the blocks before of after the "Excellent" zone results in a "Good" hit

Bad: Hitting the blocks before or after the "Good" zone results in a "Bad" hit

Miss: Missing the blocks or Hitting the blocks just outside the "Bad" zone results in a "miss"


#### HitRating visualisation:

![hitrating_visualisation](https://cloud.githubusercontent.com/assets/10066666/25002800/8fe1258c-204c-11e7-8361-14ae4be85e91.png)

#### Combo:
If blocks are hit in succession without missing, the combo will increment 

If the player misses a block, the combo will reset to 0

#### HitPercentage:
The hitPercentage is calculated by the current amount of Excellent, Good, Bad and Miss

Formula: (Amount Excellent*100 + Amount Good*1/3 + Amount Bad*1/6)/Total hits

#### Score:
The score increases using the current combo and hitRating

Excellent: 200

Good: 100

Bad: 50

Miss 0

Formula: Score += Hitrating * combo

#### Grade:
The grade is calculated using the current hitPercentage
S+: 100%

S: >95%

A: 90%-95%

B: 80%-90%

C: 70%-80%

D: <70%
