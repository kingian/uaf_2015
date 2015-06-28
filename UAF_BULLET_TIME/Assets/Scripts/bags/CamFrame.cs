using UnityEngine;
using System.Collections;
using System.Collections.Generic;


[System.Serializable]
public class CamFrame {

	public Texture image;
	public string name;//just for backup;
	public int timestamp;
	public int frame_index;
	public bool hasImage = false;
	public string file_reference;

}
