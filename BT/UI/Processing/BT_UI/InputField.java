import processing.core.PApplet;
import processing.event.KeyEvent;

import java.util.regex.Pattern;

/**
 * Created by davidkemker on 6/25/15.
 */
public class InputField
{
	PApplet _p;

	static final String DEFAULT_INPUT = "Email Address";
	static final int INPUT_DELAY_FRAMES = 2;

	String _input = DEFAULT_INPUT;
	String _inputDisplay = DEFAULT_INPUT;

	float _x;
	float _y;
	float _width;
	float _height;

	public InputField(PApplet p, float x, float y, float width, float height)
	{
		this._p = p;

		this._p.registerMethod("draw", this);
		this._p.registerMethod("keyEvent", this);

		this._x = x;
		this._y = y;
		this._width = width;
		this._height = height;
	}

	public String getInput()
	{
		return _input;
	}

	public void draw()
	{
		_p.fill(_p.color(255, 255, 255));
		_p.stroke(0, 0, 0);
		_p.strokeWeight(1.0f);

		_p.rect(_x, _y, _width, _height);

		if(_input != null)
		{
			_p.fill(_p.color(0, 0, 0));

			float textHeight = _height*0.5f;
			_p.textSize(textHeight);

			float textWidth = _p.textWidth(_inputDisplay);
			_p.text(
					_inputDisplay,
					_x + _width*0.5f - textWidth*0.5f,
					_y + _height*0.5f + textHeight*0.4f);
		}
	}

	public void keyEvent(KeyEvent e)
	{
		if(e.getAction() == KeyEvent.RELEASE)
		{
			if(DEFAULT_INPUT.equals(_input))
			{
				// Clear the text entry if the text is the default value.
				_input = "";
			}

			if(e.getKeyCode() == PApplet.BACKSPACE)
			{
				if(_input.length() > 0)
				{
					_input = _input.substring(0, _input.length() - 1);
				}
			}
			else if(e.getKeyCode() >= 32 && e.getKeyCode() <= 254)
			{
				char c = (char) e.getKeyCode();

				if(Character.toString(e.getKey()).equals("@"))
				{
					c = (char) 64;
				}

				_input += Character.toString(c).toLowerCase();
			}

			_inputDisplay = _input;
		}
	}
}
