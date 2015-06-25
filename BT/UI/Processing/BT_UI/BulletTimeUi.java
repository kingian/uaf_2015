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
	ImageViewer _viewer;


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
				_p.width * 0.5f, _p.height * 0.9f,
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
	}

	public void draw()
	{

	}
}
