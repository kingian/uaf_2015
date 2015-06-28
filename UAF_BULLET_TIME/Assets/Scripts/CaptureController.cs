using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System;
using System.Linq;

public class CaptureController : MonoBehaviour {

	public string root_directory;
	public string desired_capture_directory;

	public string pi_prefix;
	public string pi_suffix;
	public int pi_starting_index;
	public int pi_count;

	public string camera_prefix;
	public int camera_count;

	public string frame_prefix;
	public int normalizing_fps;

	public int output_fps;


	private string capture_path;

	//public Renderer draw_context;


	private List<Texture> frame_list;


	private bool can_animate = false;

	private int current_frame = 0;

	public string last_image_location;

	MeshRenderer mesh_renderer;

	public int bullet_time_offset = 0;//in seconds from beginning;



	private List<int> all_safe_starts;
	private List<int> all_safe_ends;

	private int safe_start;
	private int safe_end;

	private float frame_delay;
	private float time_since_new_frame;

	public float image_loading_padding = 0f;
	public bool recalculateFrames = false;

	public List<RPi> pi_list;

	// Use this for initialization
	void Start () {

		frame_delay = 1000f / output_fps;
		time_since_new_frame = 0f;

		all_safe_starts = new List<int>();
		all_safe_ends = new List<int>();

		capture_path = root_directory + "/" + desired_capture_directory;
		mesh_renderer = gameObject.GetComponent<MeshRenderer>();


		Debug.Log (Directory.GetCurrentDirectory ());


		//loadimage ();

		if (recalculateFrames == true) {

			buildDataAbstractions ();
			StartCoroutine (getBulletTimeSequence (0, 0));
			//StartCoroutine(getFramesFromPiAndCamera(0,0));

			recalculateFrames = false;
		} else {

			StartCoroutine (getBulletTimeSequence (0, 0));
		}


	}

//	void loadimage(){
//		string url = "file:///Users/Shared/UAF/images/test.jpg";
//		WWW www = new WWW(url);
//		//yield return www;
//		Debug.Log ("IMAGE");
//		mesh_renderer.material.mainTexture = www.texture;
//	}
	
	// Update is called once per frame
	void Update () {

		if (can_animate==true) {

			time_since_new_frame += (Time.deltaTime *1000f);
			//Debug.Log(time_since_new_frame);
			if(time_since_new_frame >= frame_delay){

				//Debug.Log("ANIMATIN");
				//Debug.Log(frame_list[0].name);
				mesh_renderer.material.mainTexture = frame_list[current_frame];
				//Debug.Log(rendy.material.name);
				//gameObject.renderer.material.mainTexture = frame_list[current_frame];
				current_frame++;
				
				if(current_frame >= frame_list.Count)
					current_frame = 0;


				time_since_new_frame = 0;
			}






		}

	
	}




	private List<Texture> getLinearTimeFramesFromCamera(int pi_index, int camera_index, int start, int end){

		List<Texture> frames = new List<Texture> ();

		pi_list.OrderBy(x => x.index);
		RPi target_pi = pi_list [pi_index];
		frames = target_pi.getFramesFromTargetCameraInRange (camera_index, start, end);
		return frames;
	}

	private List<Texture> getBulletTimeFramesForTimeAndCamera(int pi_index, int camera_index, int timestamp){

		List<Texture> bullet_frames = new List<Texture> ();

		//we get first frame from desired camera, then loop through the rest
		foreach (RPi pi in pi_list) {
			List<Texture> frames = pi.getSingleFramePerCameraAtTime(timestamp);
			bullet_frames.AddRange(frames);
		}
		return bullet_frames;
	}

	private int getNearestRealTimestampForPiAndCamera(int pi, int camera, int timestamp){

		return pi_list[pi].getNearestRealTimestampForCamera (camera, timestamp);

	}


	IEnumerator getBulletTimeSequence(int pi_index, int camera_index){

		//sort cameras
		pi_list.OrderBy(x => x.index);

		//wait so www can load iamges
		yield return new WaitForSeconds (image_loading_padding);


		List<Texture> sequence = new List<Texture> ();

		int first_segment_end = ((safe_end - safe_start) / 2) + safe_start;
		first_segment_end += bullet_time_offset;
		Debug.Log ("BULLET:" + first_segment_end);

		first_segment_end = getNearestRealTimestampForPiAndCamera (0, 0, first_segment_end);

		//get first segement

		sequence.AddRange (  getLinearTimeFramesFromCamera(0,0,safe_start,first_segment_end) );
		//get bullet time

		sequence.AddRange (  getBulletTimeFramesForTimeAndCamera(0,0,first_segment_end) );
		//get second segment

		sequence.AddRange (  getLinearTimeFramesFromCamera(0,0,first_segment_end,safe_end) );



		frame_list = sequence;

		Debug.Log (frame_list.Count);


		StartCoroutine (allowAnimation());

	}


	IEnumerator getFramesFromPiAndCamera(int pi_index, int camera_index){


		//sort cameras
		pi_list.OrderBy(x => x.index);



		
		yield return new WaitForSeconds (5f);
		

		RPi target_pi = pi_list [pi_index];
		frame_list = target_pi.getFramesFromTargetCamera (camera_index);
		

		
		Debug.Log (frame_list.Count);
		
		StartCoroutine (allowAnimation());


	}






	IEnumerator getFramesForAnimation(){

		//sort cameras
		pi_list.OrderBy(x => x.index);

		yield return new WaitForSeconds (5f);

		frame_list = new List<Texture> ();

		foreach (RPi pi in pi_list) {
			frame_list.AddRange(pi.getFrameTexturesForNormalizedFPS(normalizing_fps));
		}

		Debug.Log (frame_list.Count);

		StartCoroutine (allowAnimation());
	}

	IEnumerator allowAnimation(){
		Debug.Log ("NOT ALLOWED");
		yield return new WaitForSeconds (.002f);
		Debug.Log ("ALLOWED");
		can_animate = true;
		//CaptureTheGIF.Instance.Capture(30, 320, 240, 10f, "gifs", "gif");

	}


	IEnumerator stopGifCapture(){

		yield return new WaitForSeconds (5f);

	}

	//we'll go ahead and create everything outselves

	void buildDataAbstractions(){

		DirectoryInfo capture_directory = new DirectoryInfo(capture_path);
		DirectoryInfo[] capture_directory_info = capture_directory.GetDirectories();

		foreach (DirectoryInfo pi_folder in capture_directory_info) {

			//strip the gunk
			string pi_name = pi_folder.Name.Replace(pi_prefix, "");
			//Debug.Log(pi_name);
			pi_name = pi_name.Replace(pi_suffix, "");
			//Debug.Log(pi_name);
			//make pi = we'll sort and figure out which cameras exist later
			RPi pi_bag = new RPi();
			pi_bag.index = Convert.ToInt32(pi_name);
			Debug.Log("PI:"+pi_bag.index);

			//each pi has cameras
			DirectoryInfo[] camera_folders = pi_folder.GetDirectories();
			foreach(DirectoryInfo camera_folder in camera_folders){

				//remove gunk
				string camera_name = camera_folder.Name.Replace(camera_prefix,"");
				//make cams
				SonyCam cam = new SonyCam();
				cam.index = Convert.ToInt32(camera_name);
				Debug.Log("CAM:"+cam.index);

				//let the pi deal with it
				pi_bag.addCam(cam);

				//each camera has frames
				FileInfo[] frame_files = camera_folder.GetFiles("*.jpg");
				if(frame_files.Length > 0){

					int i = 0;
					for(;i<frame_files.Length;i++){

						CamFrame frame = new CamFrame();
						frame.name = frame_files[i].Name.Replace(".jpg","");
						frame.name = frame.name.Replace(frame_prefix,"");
						frame.frame_index = Convert.ToInt32( frame.name.Substring(frame.name.LastIndexOf("-")+1));
						frame.timestamp = Convert.ToInt32( frame.name.Substring(0, frame.name.LastIndexOf("-")));
						frame.hasImage = false;
						//Debug.Log(frame_files[i].FullName);

						//this async shit is gonna make things annoying
						StartCoroutine(asyncLoadImage(frame_files[i].FullName, frame));


						cam.addFrame(frame);

					}

				}




			}


			pi_bag.normalizeFramesToTargetFPS(normalizing_fps);
			all_safe_starts.Add(pi_bag.safe_starting_timestamp);
			all_safe_ends.Add(pi_bag.safe_ending_timestamp);
			Debug.Log("SAFES:"+pi_bag.safe_starting_timestamp+":"+pi_bag.safe_ending_timestamp);


			//lets save these
			if(pi_list == null)
				pi_list = new List<RPi>();
			
			pi_list.Add(pi_bag);

		}

		//lets get best sratinga nd ending timtestamp while we're waiting
		safe_start = all_safe_starts.First ();
		safe_end = all_safe_ends.First ();

		foreach (int timestamp in all_safe_starts) {
			safe_start = Mathf.Max(safe_start, timestamp);
		}

		foreach (int timestamp in all_safe_ends) {
			safe_end = Mathf.Min(safe_end, timestamp);
		}


		//and we might as well just pre remove everything thats not valid
		foreach (RPi pi in pi_list) {
			pi.truncateToSafeTimestamps(safe_start, safe_end);
		}




	}

	
	
	IEnumerator asyncLoadImage(string path, CamFrame frame){
		//string url = "file:///Users/Shared/UAF/images/test.jpg";
		//Debug.Log (path);
		last_image_location = "file://"+path;
		WWW file_reference = new WWW("file://"+path);
		yield return file_reference;
		//Debug.Log ("ERROR"+file_reference.url);
		frame.image = file_reference.texture;
		frame.hasImage = true;
		//mesh_renderer.material.mainTexture = file_reference.texture;
		
	}




}
