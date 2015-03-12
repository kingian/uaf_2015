 import controlP5.*;



// Project scoped variables
ControlP5 cp5;
Ball b;
ArrayList<Ball> balls;
int max, vel, ghost, size, bg;
Slider Velocity;
Slider NumberOfBalls;
Slider Ghosting;
Slider Size;
Slider Background;




void setup()
{
  max = 500;
  vel = 15;
  ghost = 80;
  size = 10;
  bg = 200;
  size(1200,800);
  noStroke();
  ellipseMode(RADIUS);

 
 cp5 = new ControlP5(this);
 
 Group g1 = cp5.addGroup("g1")
             .setPosition(width-300,10)
             .setWidth(300)
             .activateEvent(true)
             .setBackgroundColor(color(128,50))
             .setBackgroundHeight(200)
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
              
  Size = cp5.addSlider("Size")
              .setPosition(10,70)
              .setSize(200,20)
              .setGroup(g1)
              .setLabel(" Size Range")
              .setRange(1,25)
              .setValue(size)
              ;

  Ghosting = cp5.addSlider("Ghosting")
              .setPosition(10,100)
              .setSize(200,20)
              .setGroup(g1)
              .setLabel(" Ghosting")
              .setRange(100,1)
              .setValue(ghost)
              ;
              
  Background = cp5.addSlider("Background")
              .setPosition(10,130)
              .setSize(200,20)
              .setGroup(g1)
              .setLabel(" Background Value")
              .setRange(0,255)
              .setValue(bg)
              ;              
              
   cp5.addButton("Reset")
              .setPosition(10,160)
              .setSize(100,20)
              .setGroup(g1)
              ;
             
  fillBallArray();
 
}


void draw()
{
  noStroke();
  fill(bg,ghost);
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
      fill(bg);
      rect(0,0,width,height);
      max = (int)NumberOfBalls.getValue();
      vel = (int)Velocity.getValue();
      ghost = (int)Ghosting.getValue();
      size = (int)Size.getValue();
      bg = (int)Background.getValue();
      fillBallArray();
      draw(); 
   }
}



void fillBallArray()
{
    balls = new ArrayList<Ball>();
    for(int i = 0; i < max; i++)
  {
    PVector l = new PVector((width/2+random(-width/4,width/4)),(height/2+random(-height/4,height/4)));
    PVector v = new PVector(random(-vel,vel),random(-vel,vel));
    b = new Ball(l,v,random(1,size));
    b.setColor(color(random(128,255),0,0));
    balls.add(b);
  }
}

/*
Checks for ball collisions with screen edges.
*/
void checkBounds(Ball ball)
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
  color colr;

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
  
  void setColor(color _colr)
  {
    colr = _colr;
  }
  
  void display()
  {
//    stroke(stroke);
//    strokeWeight(weight);
    fill(colr,50);
    ellipse(this.location.x,this.location.y,radius,radius);
  }
  
  void updatePos()
  {
    location.add(velocity);
  }
  
  void flipDx()
  {
    this.velocity.x *= -1;
    
  }
  
  void flipDy()
  {
    this.velocity.y *= -1;
  }
  
  void updatVelocity(float _dx, float _dy)
  {
    velocity.set(_dx,_dy);
  }
  
}
