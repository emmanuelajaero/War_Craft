# War_Craft

Dimension : The game war craft screen size is 600X800 in dimension
Refresh Rate : The screen refresh rate is 30 frames per seconds

Levels of the game: the level the game can get to depends on the player, the level increases by 1
with every 10 increase in score except from 0-20


The art work used in this game images and sounds where downloaded from one of these websites:
https://www.freepik.com/, https://www.dafont.com/, https://opengameart.org/, freesoundeffects.com/free-sounds/gun-10081/

The game consists basically of 4 different sprites objects and 3 different sprites groups
The “Player” sprite object if the object that will be controlled by the player of the game,
The “Bullet” sprite object is emitted from the top of the Player sprite object when the K_SPACE
event occurs. The Bullet sprite object needs to collide with the “Enemy” sprite object, when the
Bullet sprite objects collides with the Enemy sprite object a point is added to the player, the Enemy
and Bullet sprites objects disappears from from the screen and the “Explosion” sprite object
appears for just a second and disappears. Another time the Explosion sprite objects appears on the
screen is when the Enemy sprite objects collides with the Player sprite object when that occurs the
player loses half life indicated by the half image on the top screen.
To keep track of all the sprites on the screen the “sprites” group exist to keep track of the enemies
the “enemies” group exist and the bullets are tracked by the “bullets” group of sprites.


**CONTROLS:
**

**ARROW LEFT:** moves the Player sprite to the left of the game screen

**ARROR RIGH:** moves the Player sprite to the right of the game screen

**p:** pause the game

**r:** restarts the game when the game is over

**q:** quits the game when the players life is reduces to zero

