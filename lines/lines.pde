import controlP5.*;

ControlP5 cp5;
ArrayList<LineSprite> lines;
LineSprite ls;
int max, bg, vel, ghost, lineWidth;
float maxVel;
Slider NumberOfLines, Velocity, Ghosting, Background, Size;

void setup()
{
  max = 50;
  maxVel = 10.0;
  bg = 80;
  ghost = 80;
  lineWidth = 10;
  size(1280,800);
  noStroke();

 
   cp5 = new ControlP5(this);
 
 Group g1 = cp5.addGroup("g1")
             .setPosition(width-300,10)
             .setWidth(300)
             .activateEvent(true)
             .setBackgroundColor(color(128,50))
             .setBackgroundHeight(200)
             .setLabel("Lines Controls")
             ;
  NumberOfLines = cp5.addSlider("NumberOfLines")
              .setPosition(10,10)
              .setSize(200,20)
              .setGroup(g1)
              .setLabel(" # of lines")
              .setRange(5,1000)
              .setValue(max)
              ;
              
  
  Velocity = cp5.addSlider("Velocity")
              .setPosition(10,40)
              .setSize(200,20)
              .setGroup(g1)
              .setLabel(" Velocity")
              .setRange(1,50)
              .setValue(maxVel)
              ;

  Ghosting = cp5.addSlider("Ghosting")
              .setPosition(10,70)
              .setSize(200,20)
              .setGroup(g1)
              .setLabel(" Ghosting")
              .setRange(100,1)
              .setValue(ghost)
              ;
              
  Size = cp5.addSlider("Size")
              .setPosition(10,100)
              .setSize(200,20)
              .setGroup(g1)
              .setLabel(" Size Range")
              .setRange(1,25)
              .setValue(lineWidth)
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
            
    fillLineArray();
}


void draw()
{
  noStroke();
  fill(bg,ghost);
  rect(0,0,width,height);
  for (int i = 0; i < max; i++)
  {
    ls = lines.get(i);
    ls.updatePos();
    ls.display();
    checkBounds(ls);
  }
}

public void controlEvent(ControlEvent theEvent)
{
   if (theEvent.getController().getName().equals("Reset"))
   {
      fill(bg);
      rect(0,0,width,height);
      max = (int)NumberOfLines.getValue();
      maxVel = (int)Velocity.getValue();
      ghost = (int)Ghosting.getValue();
      lineWidth = (int)Size.getValue();
      bg = (int)Background.getValue();
      fillLineArray();
      draw(); 
   }
}

void fillLineArray()
{
  lines = new ArrayList<LineSprite>();
  for (int i = 0; i < max; i++)
  {
    boolean hor = randBool();
    float tempPos;
    
    if(hor) { tempPos = random(0,height); }
    else { tempPos = random(0,width); }
    
//    ls = new LineSprite(randBool(),tempPos,random(-maxVel,maxVel),randCol(),int(random(1,4)));
    ls = new LineSprite(randBool(),tempPos,random(-maxVel,maxVel),color(invertGrayScale(bg),50),int(random(1,lineWidth)));
    lines.add(ls);
  }
}

int invertGrayScale(int cti)
{
  if (cti < 118)
  { 
    return ((128 - cti) + 128);
  }
  else if (cti < 128)
  {
    return 255;
  }
  else if (cti > 127)
  {
    return 0;
  }
  else
  {
    return  (128 - (cti - 128));
  }
  
 
}

boolean randBool()
{
  int bol = (int)random(0,10);
  if (bol < 5){ return true; }
  else { return false; }
}

color randCol()
{
  return color(int(random(0,128)),int(random(0,128)),int(random(0,255)),int(random(0,255)));
}


void checkBounds(LineSprite ls)
{
  if (!ls.horizontal)
  {
     if (( ls.position > width-ls.weight) || (ls.position < ls.weight))
    {
      ls.flipV();
    }
  }
  else
  {
    if ((ls.position > height-ls.weight) || (ls.position < ls.weight)) 
    {
      ls.flipV();
    }
  }
}


class LineSprite
{
  boolean horizontal;
  float position;
  float velocity;
  color lineColor;
  int weight;
  
  LineSprite(boolean isHorizontal, float initPos, float initVel)
  {
    horizontal = isHorizontal;
    position = initPos;
    velocity = initVel;
    lineColor = color(0,50);
    weight = 1;
  }
  
  LineSprite(boolean isHorizontal, float initPos, float initVel, color lineColr, int lineWeight)
    {
    horizontal = isHorizontal;
    position = initPos;
    velocity = initVel;
    lineColor = lineColr;
    weight = lineWeight;
  }
  
  
  void flipV()
  {
    velocity *=-1;
  }

  void display()
  {
    if(horizontal)
    {
      stroke(lineColor);
      strokeWeight(weight);
      line(0, position, width, position);
    }
    else
    {
      stroke(lineColor);
      strokeWeight(weight);
      line(position, 0, position, height);
    }      
  }
  
  void updatePos()
  {
    position += velocity;
  }
   
}
