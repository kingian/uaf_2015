import processing.core.PApplet;
import processing.core.PImage;

import java.io.File;
import java.io.FileFilter;
import java.io.FilenameFilter;
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.LinkedList;

/**
 * Created by davidkemker on 6/20/15.
 */
public class ImageViewer
{
    public enum ImageViewerState
    {
        Playing,
        Stopped
    }

    private static final String FILE_EXTENSION = ".jpg";
    private static final String PI_FOLDER_PREFIX = "pi";
    private static final String CAM_FOLDER_PREFIX = "cam";

    private PApplet _p;
    private String _rootPath;
    private ImageViewerState _state = ImageViewerState.Stopped;

    private Point2D _center;
    private float _width;
    private float _height;

    private int _maxFrames;
    private int _minFrames = Integer.MAX_VALUE;
    private int _maxCameras = 27;
    private int _btFrame = -1;

    ArrayList<File> _cameraFolders = new ArrayList<File>();
    ArrayList<File[]> _imageFiles = new ArrayList<File[]>();

    private int _currentFrame = 0;
    private int _previousFrame = -1;
    private int _activeCamera = 0;
    private int _activeVirtualCamera = 0;

    public ImageViewer(PApplet applet, String rootImagePath, float centerX, float centerY, float width, float height)
    {
        _p = applet;
        _p.registerMethod("draw", this);

        _center = new Point2D(centerX, centerY);
        _width = width;
        _height = height;

        findFiles(rootImagePath);
    }

    private void findFiles(String rootImagePath)
    {
        _rootPath = rootImagePath;

        // find all the pi folders in the root path.
        File f = new File(_p.sketchPath(_rootPath));
        File[] foldersPi = f.listFiles(new FileFilter() {
            @Override
            public boolean accept(File pathname) {
                return pathname.isDirectory() && pathname.getName().startsWith(PI_FOLDER_PREFIX);
            }
        });

        // For every pi folder, find the camera folders within the pi folders.
        if(foldersPi == null)
        {
            // Done for debugging...
            findFiles("/Users/davidkemker/Dave/Projects/Programming/uaf_2015/BT/UI/Processing/BT_UI/images/batch_1");
            return;
        }
        for(File fPi : foldersPi)
        {
            File[] foldersCams = fPi.listFiles(new FileFilter() {
                @Override
                public boolean accept(File pathname) {
                    return pathname.isDirectory() && pathname.getName().startsWith(CAM_FOLDER_PREFIX);
                }
            });

            // Find all the image files in the camera folders.
            for(File fCam : foldersCams)
            {
                File[] files = fCam.listFiles(new FileFilter() {
                    @Override
                    public boolean accept(File pathname) {
                        return !pathname.isDirectory() && pathname.getName().endsWith(FILE_EXTENSION);
                    }

                });

                // Sort the array of images specifically taking care of the situations when integer values aren't
                // padded with zeros.
                Arrays.sort(files, new Comparator<File>() {
                    @Override
                    public int compare(File o1, File o2) {
                        String token1 = o1.getName().substring(o1.getName().lastIndexOf("_")+1);
                        token1 = token1.substring(0, token1.indexOf("."));
                        String token2 = o2.getName().substring(o2.getName().lastIndexOf("_")+1);
                        token2 = token2.substring(0, token2.indexOf("."));

                        int v1 = PApplet.parseInt(token1);
                        int v2 = PApplet.parseInt(token2);

                        return Integer.compare(v1, v2);
                    }
                });

                _maxFrames = Math.max(_maxFrames, files.length);
                _minFrames = Math.min(_minFrames, files.length);

                _imageFiles.add(files);
            }
        }
    }

    public String getCurrentImagePath()
    {
        return _imageFiles.get(_activeVirtualCamera)[_currentFrame].getAbsolutePath();
    }

    public void setBtFrame(int bulletTimeFrame)
    {
        _btFrame = bulletTimeFrame;
    }

    public void setBtFrameToCurrentFrame()
    {
        _btFrame = _currentFrame;
    }

    public void setState(ImageViewerState newState)
    {
        _state = newState;
    }

    public ImageViewerState getState()
    {
        return _state;
    }

    public void draw()
    {
        // Load the current file. (I know this is slow... but it works alright.)
        PImage img = _p.loadImage(getCurrentImagePath());
        _p.image(img, _center.getX() - _width * 0.5f, _center.getY() - _height * 0.5f, _width, _height);

        if(_state == ImageViewerState.Playing)
        {
            if (_currentFrame == _btFrame)
            {
                if (_activeVirtualCamera >= _maxCameras)
                {
                    _currentFrame++;
                }
                else
                {
                    _activeVirtualCamera++;
                }
            }
            else
            {
                _currentFrame++;
            }

            if (_currentFrame >= _maxFrames)
            {
                _currentFrame = 0;
                _activeVirtualCamera = 0;
            }
        }
    }
}
