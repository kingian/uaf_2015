using UnityEngine;
using UnityEditor;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

[System.Serializable]
public class RPi {

	public int index;
	public int camera_count;
	public List<SonyCam> camera_list;


	public int safe_starting_timestamp;
	public int safe_ending_timestamp;

	public void addCam(SonyCam new_cam){
		if (camera_list == null)
			camera_list = new List<SonyCam> ();

		camera_list.Add (new_cam);
		camera_count = camera_list.Count;
	}


	public List<Texture> getFrameTexturesForNormalizedFPS(int target_fps){

		List<Texture> all_frames = new List<Texture> ();

		//add frames to list
		foreach (SonyCam cam in camera_list) {
			all_frames.AddRange(cam.getRawFrames());
		}

		foreach (Texture texture in all_frames) {
			Debug.Log(texture);
		}

		return all_frames;
	}



	public List<Texture> getFramesFromTargetCamera(int target_camera){

		//camera_list.OrderBy(x => x.index);
		List<Texture> all_frames = camera_list[target_camera].getAllNormalizedFrames();
		return all_frames;
	}

	public List<string> getFrameReferencesFromTargetCamera(int target_camera){
		List<string> all_frames = camera_list[target_camera].getAllNormalizedFrameReferences();
		return all_frames;
	}


	public List<Texture> getFramesFromTargetCameraInRange(int target_camera, int start, int end){

		List<Texture> all_frames = camera_list[target_camera].getNormalizedFramesInRange(start,end);
		return all_frames;
	}

	public List<Texture> getSingleFramePerCameraAtTime(int timestamp){

		List<Texture> frames = new List<Texture> ();
		foreach (SonyCam cam in camera_list) {

			Texture possible_frame = cam.getFirstFrameAtTimestampt(timestamp);
			if(possible_frame != null){
				frames.Add( possible_frame );
			}

		}

		return frames;
	}

	public List<Texture> getSingleFramePerCameraWithOffsets(int second_offset, int frame_offset){

		List<Texture> frames = new List<Texture> ();
		foreach (SonyCam cam in camera_list) {
			
			Texture possible_frame = cam.getFrameAtSecondAndFrameIndex(second_offset, frame_offset);
			if(possible_frame != null){
				frames.Add( possible_frame );
			}
			
		}
		
		return frames;
	}

	public int getNearestRealTimestampForCamera(int camera, int timestamp){

		int nearest_time =camera_list[camera].getNearestTimeAtTimestampt(timestamp);
		return nearest_time;
	}

	public void normalizeFramesToTargetFPS(int target_fps ){
		camera_list.OrderBy(x => x.index);
		foreach (SonyCam cam in camera_list) {
			cam.normalizeFramesToTargetFPS(target_fps);
		}

		int potential_safe_start = 0;
		int potential_safe_end = 999999999;
		foreach (SonyCam cam in camera_list) {
			potential_safe_start = Mathf.Max( cam.starting_time, potential_safe_start);
			potential_safe_end = Mathf.Min( cam.ending_time, potential_safe_end);
		}

		safe_starting_timestamp = potential_safe_start;
		safe_ending_timestamp = potential_safe_end;

	}

	public void truncateToSafeTimestamps(int starting, int ending){

		foreach (SonyCam cam in camera_list) {
			cam.truncateToSafeTimestamps(starting, ending);
		}

	}


}
