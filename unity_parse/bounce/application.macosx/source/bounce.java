import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import controlP5.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class bounce extends PApplet {




ControlP5 cp5;
Ball b;
ArrayList<Ball> balls;
int max, vel;
Slider Velocity;
Slider NumberOfBalls;
public void setup()
{
  max = 5000;
  vel = 15;
  size(1200,800);
  noStroke();
  ellipseMode(RADIUS);

 
 cp5 = new ControlP5(this);
 
 Group g1 = cp5.addGroup("g1")
             .setPosition(width-300,10)
             .setWidth(300)
             .activateEvent(true)
             .setBackgroundColor(color(128,50))
             .setBackgroundHeight(100)
             .setLabel("Bounce Controls")
             ;
  NumberOfBalls = cp5.addSlider("NumberOfBalls")
              .setPosition(10,10)
              .setSize(200,20)
              .setGroup(g1)
              .setLabel(" # of balls")
              .setRange(50,10000)
              .setValue(max)
              ;
  
  Velocity = cp5.addSlider("Velocity")
              .setPosition(10,40)
              .setSize(200,20)
              .setGroup(g1)
              .setLabel(" Velocity")
              .setRange(1,50)
              .setValue(vel)
              ;
              
   cp5.addButton("Reset")
              .setPosition(10,70)
              .setSize(100,20)
              .setGroup(g1)
              ;
             
  fillBallArray();
 
}


public void draw()
{
  noStroke();
  fill(200,70);
  rect(0,0,width,height);
  for(int j = 0; j < max; j++)
  {
    b = balls.get(j);
    b.updatePos();
    b.display();
    checkBounds(b);
  }
}

public void controlEvent(ControlEvent theEvent)
{
   if (theEvent.getController().getName().equals("Reset"))
   {
      fill(200);
      rect(0,0,width,height);
      max = (int)NumberOfBalls.getValue();
      vel = (int)Velocity.getValue();
      fillBallArray();
      draw(); 
   }
}



public void fillBallArray()
{
    balls = new ArrayList<Ball>();
    for(int i = 0; i < max; i++)
  {
    PVector l = new PVector((width/2+random(-width/4,width/4)),(height/2+random(-height/4,height/4)));
    PVector v = new PVector(random(-vel,vel),random(-vel,vel));
    b = new Ball(l,v,random(1,10));
    b.setColor(color(random(128,255),0,0));
    balls.add(b);
  }
}

/*
Checks for ball collisions with screen edges.
*/
public void checkBounds(Ball ball)
{
  if (( ball.location.x > width-ball.radius) || (ball.location.x < ball.radius))
  {
    ball.flipDx();
  }
  if ((ball.location.y > height-ball.radius) || (ball.location.y < ball.radius)) 
  {
    ball.flipDy();
  }
}

class Ball
{
  PVector location, velocity;
  float radius,stroke,weight;
  int colr;

  Ball(PVector _loc, float _radius)
  {
    location = _loc;
    radius = _radius;   
  }
  
    Ball(PVector _loc, PVector _vel, float _radius)
  {
    stroke = random(255);
    weight = random(0,3);
    location = _loc;
    velocity = _vel;
    radius = _radius;   
  }
  
  public void setColor(int _colr)
  {
    colr = _colr;
  }
  
  public void display()
  {
//    stroke(stroke);
//    strokeWeight(weight);
    fill(colr,50);
    ellipse(this.location.x,this.location.y,radius,radius);
  }
  
  public void updatePos()
  {
    location.add(velocity);
  }
  
  public void flipDx()
  {
    this.velocity.x *= -1;
    
  }
  
  public void flipDy()
  {
    this.velocity.y *= -1;
  }
  
  public void updatVelocity(float _dx, float _dy)
  {
    velocity.set(_dx,_dy);
  }
  
}
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "bounce" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
