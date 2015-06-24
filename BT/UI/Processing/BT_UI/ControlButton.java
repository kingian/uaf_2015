import processing.core.PApplet;
import processing.event.MouseEvent;

/**
 * Created by davidkemker on 6/20/15.
 */
public class ControlButton
{
    public enum ButtonType
    {
        Button,
        Play,
        Rewind
    }

    PApplet _p;

    private float _x;
    private float _y;
    private float _width;
    private float _height;
    private ButtonType _type;

    private Point2D _playP1;
    private Point2D _playP2;
    private Point2D _playP3;

    private OnClickListener _onClickListener;


    public void setOnClicked(OnClickListener onClickListener)
    {
        this._onClickListener = onClickListener;
    }

    public ControlButton(PApplet applet, float x, float y, float width, float height, ButtonType type)
    {
        _p = applet;
        _type = type;

        _p.registerMethod("draw", this);
        _p.registerMethod("mouseEvent", this);

        _x = x;
        _y = y;
        _width = width;
        _height = height;

        if(ButtonType.Play.equals(_type))
        {
            float _triScale = 0.5f;
            float _triWidth = _width * _triScale;
            float _triHeight = _height * _triScale;
            float _triOffsetX = _width * 0.06f;

            _playP1 = new Point2D(_triOffsetX + _x - _triWidth * 0.5f, _y + _triHeight * 0.5f);
            _playP2 = new Point2D(_triOffsetX + _x - _triWidth * 0.5f, _y - _triHeight * 0.5f);
            _playP3 = new Point2D(_triOffsetX + _x + _triWidth * 0.5f, _y);
        }
//        else if(ButtonType.Rewind.equals(type))
//        {
//            float _triScale = 0.5f;
//            float _triWidth = _width * _triScale;
//            float _triHeight = _height * _triScale;
//            float _triOffsetX = _width * 0.06f;
//
//            _playP1 = new Point2D(_triOffsetX + _x - _triWidth * 0.5f, _y + _triHeight * 0.5f);
//            _playP2 = new Point2D(_triOffsetX + _x - _triWidth * 0.5f, _y - _triHeight * 0.5f);
//            _playP3 = new Point2D(_triOffsetX + _x + _triWidth * 0.5f, _y);
//        }
        else
        {

        }
    }

    public void draw()
    {
        _p.pushStyle();

        _p.noStroke();

        int buttonColor = _p.color(0, 200, 0);
        _p.fill(buttonColor);
        _p.ellipse(_x, _y, _width, _height);

        if(ButtonType.Play.equals(_type))
        {
            int triColor = _p.color(120, 255, 120);
            _p.fill(triColor);
            _p.triangle(
                    _playP1.getX(), _playP1.getY(),
                    _playP2.getX(), _playP2.getY(),
                    _playP3.getX(), _playP3.getY());
        }

        _p.popStyle();
    }

    public boolean isInside(float x, float y)
    {
        float halfWidth = _width*0.5f;
        float halfHeight = _height*0.5f;
        float testVal = ((x-_x)*(x-_x))/(halfWidth*halfWidth) + ((y-_y)*(y-_y))/(halfHeight*halfHeight);
        return testVal <= 1;
    }

    public void mouseEvent(MouseEvent event)
    {
        if(!isInside(event.getX(), event.getY()))
        {
            return;
        }

        if(event.getAction() == MouseEvent.CLICK)
        {
            if(_onClickListener != null)
            {
                _onClickListener.onClick();
            }
        }
    }

    public interface OnClickListener
    {
        void onClick();
    }
}
