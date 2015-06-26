import processing.core.PApplet;

/**
 * Created by davidkemker on 6/20/15.
 */
public class BulletTimeUi
{
	PApplet _p;
	private static final String ROOT_IMAGE_FOLDER = "images/batch_1";

	ControlButton _playButton;
	ControlButton _btButton;
	ControlButton _exportButton;
	ControlButton _sendEmailButton;
	ImageViewer _viewer;
	InputField _emailAddressInput;

	boolean _hasExported = false;

	public void setup(PApplet applet)
	{
		_p = applet;
		_p.registerMethod("draw", this);

		_p.frameRate(24.0f);
		_p.size(800, 800);

		_viewer = new ImageViewer(
				_p,
				ROOT_IMAGE_FOLDER,
				_p.width * 0.5f, _p.height * 0.5f,
				_p.height - 10.0f, _p.height - 10.0f);

		_playButton = new ControlButton(
				_p,
				_p.width * 0.5f, _p.height * 0.91f,
				_p.height * 0.1f, _p.height * 0.1f,
				ControlButton.ButtonType.Play);
		_playButton.setOnClicked(new ControlButton.OnClickListener()
		{
			@Override
			public void onClick()
			{
				// Ignore clicks if exporting.
				if(_viewer.getState() != ImageViewer.ImageViewerState.Exporting)
				{
					ImageViewer.ImageViewerState currentState = _viewer.getState();
					if(currentState.equals(ImageViewer.ImageViewerState.Playing))
					{
						_viewer.setState(ImageViewer.ImageViewerState.Stopped);
					}
					else
					{
						_viewer.setState(ImageViewer.ImageViewerState.Playing);
					}
				}
			}
		});

		float btButtonWidth = _p.width * 0.4f;
		float btButtonHeight = _p.height * 0.037f;
		_btButton = new ControlButton(
				_p,
				_p.width*0.575f, _p.height*0.86f,
				btButtonWidth, btButtonHeight,
				ControlButton.ButtonType.Button);
		_btButton.setText("Set Bullet Time Frame");
		_btButton.setOnClicked(new ControlButton.OnClickListener()
		{
			@Override
			public void onClick()
			{
				// Ignore clicks if exporting.
				if(_viewer.getState() != ImageViewer.ImageViewerState.Exporting)
				{
					_viewer.setBtFrameToCurrentFrame();
				}
			}
		});

		_exportButton = new ControlButton(
				_p,
				_p.width * 0.025f, _p.height * 0.86f,
				btButtonWidth, btButtonHeight,
				ControlButton.ButtonType.Button);
		_exportButton.setText("Export Gif");
		_exportButton.setOnClicked(new ControlButton.OnClickListener()
		{
			@Override
			public void onClick()
			{
				// Ignore clicks if exporting.
				if(_viewer.getState() != ImageViewer.ImageViewerState.Exporting)
				{
					_viewer.exportGif();
				}
			}
		});

		_sendEmailButton = new ControlButton(
				_p,
				_p.width*0.025f, _p.height*0.86f + btButtonHeight + _p.height*0.02f,
				btButtonWidth, btButtonHeight,
				ControlButton.ButtonType.Button);
		_sendEmailButton.setText("Email Gif");
		_sendEmailButton.setOnClicked(new ControlButton.OnClickListener()
		{
			@Override
			public void onClick()
			{
				// Ignore clicks if an image hasn't been exported.
				if(!_hasExported)
				{
					try
					{
						Emailer.sendEmail(_emailAddressInput.getInput(), _p.sketchPath(_viewer.getOutputPath()));
					}
					catch(RuntimeException ex)
					{
						System.out.println("Failed to send the email.");
					}
				}
			}
		});

		_emailAddressInput = new InputField(
				_p,
				_p.width*0.575f, _p.height*0.86f + btButtonHeight + _p.height*0.02f,
				btButtonWidth, btButtonHeight);
	}

	public void draw()
	{
		_p.fill(220.0f, 220.0f, 220.0f);
		_p.rect(0.0f, 0.0f, _p.width, _p.height);
	}
}
