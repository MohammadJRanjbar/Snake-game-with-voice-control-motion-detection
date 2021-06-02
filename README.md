# Snake game with voice control motion detection and hand gesture recognition
 
# Snake game : 
I used pygame module to make this game it is a simple snake game that you control the snake with "up" "left" "right" "down" buttons and there is not much to it 
in an infinite loop until the user hits exit the display will get updated and if the button's event happens the snake will change the direction of its movement 

<img src="Pic/Snake.png" width="400" class="center" />

# Voice control: 
I used https://github.com/Picovoice/porcupine for voice control 
first, you should clone their GitHub repository in the assets files then I used their console (https://picovoice.ai/console/) to make my wake words in this case "Snake up " "go left" "go right " "go down" then I used pygui module so one if the wake words have been heard the correspondent button will be pressed 

# Motion detection : 
For this, I used the cv2 module 
the base Method is I detected a color that I wanted in the picture (webcam) using trackbars and a pen for my indicator then if the object or color moved 15 frames toward a direction the snake will change its movement direction
# gesture-recognition : 
It is a simple CNN that I trained with my own data but I didn't have time to improve it and the model became overfit and the result was not good but I included it anyway 
there is a training code and CNN code the CNN code is that I'm using it with a webcam and if I show the right gesture the model will predict the result and with pygui, it will change the snake movement direction
# Store :  
This part is an App Store for games (like Steam) so users can sign up and play whatever games they want, ( however there is only one game available:) ) with this feature every user has their own username and can track their own high score using the leaderboard. 

There is Videos of playing this game in video folder
