// TODO: comment this program

import acm.graphics.*;     // GOval, GRect, etc.
import acm.program.*;      // GraphicsProgram
import acm.util.*;         // RandomGenerator
import java.applet.*;      // AudioClip
import java.awt.*;         // Color
import java.awt.event.*;   // MouseEvent

public class Breakout extends GraphicsProgram implements BreakoutConstants {
	RandomGenerator rgen = new RandomGenerator();
	GRect paddle;
	GOval ball;
	double xBall = 4;
	double yBall = 5;
	int score = 0;
	int howMuch = 0;
	AudioClip bounceClip;
	
	
	//START
	public void run() {
		bounceClip = MediaTools.loadAudioClip("what-are-you-doing-in-my-swamp-.wav");
		
		addMouseListeners();
		
		createBlocks();
		
		addPaddle();
		
		addBall();
		GLabel start = new GLabel("Click to start");
		start.setFont("Arial-40");
		add(start, getWidth() / 2 - start.getWidth() / 2, getHeight() / 2 - start.getHeight() / 2);
		waitForClick();
		remove(start);
		
		movingBall();
		
		waitForClick();
		
		removeAll();
		score = 0;
		howMuch = 0;
		
		run();
	}
	
	//MOUSE MOVE GETTING PADDLE
	public void mouseMoved(MouseEvent e) {
		paddle.setLocation( e.getX(),APPLICATION_HEIGHT - PADDLE_Y_OFFSET);
	}
	
	//Create block
	private void createBlocks() {
		
		// Base value
		int xBrick = BRICK_SEP;
		int yBrick = BRICK_Y_OFFSET;
		
		//Create Blocks
		for(int j = 0; j < NBRICKS_PER_ROW; j++) {	
			for(int i = 0; i < NBRICKS_PER_ROW; i++) {
				GRect rect = new GRect(xBrick, yBrick, BRICK_WIDTH,BRICK_HEIGHT);
				rect.setFilled(true);
				add(rect);
				xBrick += BRICK_SEP + BRICK_WIDTH;
				int colorChooser = rgen.nextInt(0,4);
				
				//Color Choose
				if(colorChooser == 0) {
					rect.setFillColor(Color.RED);
				}
				else if(colorChooser == 1) {
					rect.setFillColor(Color.MAGENTA);
				}
				else if(colorChooser == 2) {
					rect.setFillColor(Color.YELLOW);
				}
				else if(colorChooser == 3) {
					rect.setFillColor(Color.GREEN);
				}
				else {
					rect.setFillColor(Color.BLUE);
				}
			}
			xBrick = BRICK_SEP;
			yBrick += BRICK_SEP + BRICK_HEIGHT;
		}
	}
	
	//add paddle to play
	private void addPaddle() {
		paddle = new GRect(100, APPLICATION_HEIGHT - PADDLE_Y_OFFSET, PADDLE_WIDTH, PADDLE_HEIGHT);
		paddle.setFilled(true);
		paddle.setFillColor(Color.GRAY);
		add(paddle);
		
	}
	
	//add ball to play
	private void addBall() {
		ball = new GOval(200,400, BALL_RADIUS * 2, BALL_RADIUS*2);
		ball.setFilled(true);
		ball.setFillColor(Color.GRAY);
		add(ball);
	}
	//move of the ball
	private void movingBall() {
		boolean ballCheck = false;
		while(true) {
			
			// score is full game over player win
			if (score == 100) {
				GLabel gameOver = new GLabel("You WIN, Score: " + score);
				gameOver.setFont("Arial-32");
				add(gameOver, getWidth() / 2 - gameOver.getWidth() / 2, getHeight() / 2 - gameOver.getHeight() / 2);
				break;
			}
			
			//check where ball hits wall and what to do
			else if(ball.getY() < 0) {
				yBall = -yBall;
			}
			else if(ball.getX() < 0 || ball.getX() + 2 * BALL_RADIUS > APPLICATION_WIDTH) {
				xBall = -xBall;
			}
			
			//hit down wall
			else if(ball.getY() + 2 * BALL_RADIUS > APPLICATION_HEIGHT){
				if(howMuch < 2){
					ball.setLocation(200, 400);
					howMuch++;
					GLabel start = new GLabel("Click to Continue");
					start.setFont("Arial-40");
					add(start, getWidth() / 2 - start.getWidth() / 2, getHeight() / 2 - start.getHeight() / 2);
					waitForClick();
					remove(start);
				}
				//end of the game
				else {
					GLabel gameOver = new GLabel("GAME OVER, Score: " + score);
					gameOver.setFont("Arial-32");
					add(gameOver, getWidth() / 2 - gameOver.getWidth() / 2, getHeight() / 2 - gameOver.getHeight() / 2);
					break;
				}
			}
			//ball movement every while true
			ball.move(xBall, yBall);
			pause(DELAY);

			//Check points
			GObject CheckObjectLU = getElementAt(ball.getX(), ball.getY());
			GObject CheckObjectRU = getElementAt(ball.getX() + 2 * BALL_RADIUS, ball.getY());
			GObject CheckObjectLD = getElementAt(ball.getX(), getY() + 2 * BALL_RADIUS);
			GObject CheckObjectRD = getElementAt(ball.getX() + 2 * BALL_RADIUS, ball.getY() + 2 * BALL_RADIUS);
			
			

			//Paddle check
			if((CheckObjectLD == paddle || CheckObjectRD == paddle) && ballCheck == false) {
				yBall = -yBall;
				ballCheck = true;
				
			}
			
			else if(CheckObjectLD == paddle || CheckObjectRD == paddle || CheckObjectLU == paddle || CheckObjectRU == paddle) {
				//Important
			}
				//BRICK CHECK
			else if(CheckObjectLD != null || CheckObjectRD != null || CheckObjectLU != null || CheckObjectRU != null) {
				bounceClip.play();
				if (CheckObjectLD != null) {
					remove(CheckObjectLD);
				} else if (CheckObjectLU != null) {
					remove(CheckObjectLU);
				} else if (CheckObjectRU != null) {
					remove(CheckObjectRU);
				} else if (CheckObjectRD != null) {
					remove(CheckObjectRD);
				}
				ballCheck = true;
				score++;
				yBall = -yBall;
			}
			else if(CheckObjectLD == null && CheckObjectRD == null && CheckObjectLU == null && CheckObjectRU == null) {
					ballCheck = false;
				}
		}
	}
}
