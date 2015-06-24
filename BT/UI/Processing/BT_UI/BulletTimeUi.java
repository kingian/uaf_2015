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
        });

        _btButton = new ControlButton(
                _p,
                _p.width * 0.58f, _p.height * 0.86f,
                _p.height * 0.04f, _p.height * 0.04f,
                ControlButton.ButtonType.Button);
        _btButton.setOnClicked(new ControlButton.OnClickListener()
        {
            @Override
            public void onClick()
            {
                _viewer.setBtFrameToCurrentFrame();
            }
        });
    }

    public void draw()
    {

    }
}
