using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.Linq;


[System.Serializable]
public class SonyCam {

	public int index;
	public int frame_count;
	public int target_fps;
	public List<CamFrame> frame_list;
	public List<SecondGrouping> seconds_list;

	public int starting_time;
	public int ending_time;

	public void addFrame(CamFrame new_frame){

		if (frame_list == null)
			frame_list = new List<CamFrame> ();

		frame_list.Add (new_frame);

	}

	public List<Texture> getRawFrames(){

		//need to do some clever shit here
		frame_list.OrderBy (c => c.timestamp).ThenBy (n => n.frame_index);

		List<Texture> frames = new List<Texture> ();
		
		foreach(CamFrame frame_bag in frame_list){
			if(frame_bag.hasImage)
				frames.Add(frame_bag.image);
			//Debug.Log(frame_bag.timestamp+":"+frame_bag.frame_index);
			//Debug.Log(frame_bag.image);
		}

		return frames;

	}

	public List<Texture> getAllNormalizedFrames(){
		List<Texture> frames = new List<Texture> ();
		foreach (SecondGrouping second in seconds_list) {

			CamFrame[] norm_frames = second.normalized_frames;
			foreach(CamFrame frame in norm_frames)
				frames.Add(frame.image);


		}
		return frames;
	}

	public List<Texture> getNormalizedFramesInRange(int start, int end){

		List<Texture> frames = new List<Texture> ();
		foreach (SecondGrouping second in seconds_list) {

			if(second.timestamp >= start && second.timestamp <= end){

				CamFrame[] norm_frames = second.normalized_frames;
				foreach(CamFrame frame in norm_frames)
					frames.Add(frame.image);

			}

		}
		return frames;


	}

	public Texture getFirstFrameAtTimestampt(int timestamp){


		SecondGrouping potential_second = seconds_list.First ();

		foreach (SecondGrouping second in seconds_list) {

			if(second.timestamp < timestamp){
				potential_second = second;

			};

			if(second.timestamp == timestamp){
				return second.normalized_frames[0].image;
			}



		}

		return potential_second.normalized_frames[0].image;

	}

	public int getNearestTimeAtTimestampt(int timestamp){
		
		SecondGrouping potential_second = seconds_list.First ();
		
		foreach (SecondGrouping second in seconds_list) {
			
			if(second.timestamp < timestamp){
				potential_second = second;
				
			};
			
			if(second.timestamp == timestamp){
				return second.timestamp;
			}
			
			
			
		}
		
		return potential_second.timestamp;


	}


	//when done we should have an ordered list of seconds containing padded frames
	public void normalizeFramesToTargetFPS(int fps){
		target_fps = fps;
		//need to do some clever shit here
		frame_list.OrderBy (c => c.timestamp).ThenBy (n => n.frame_index);

		if (seconds_list == null)
			seconds_list = new List<SecondGrouping> ();

		starting_time = frame_list.First ().timestamp;
		ending_time = frame_list.Last ().timestamp;

		SecondGrouping current_second = new SecondGrouping ();
		current_second.timestamp = frame_list.First().timestamp;
		seconds_list.Add (current_second);
		foreach (CamFrame frame in frame_list) {

			if(frame.timestamp != current_second.timestamp){
				current_second.normalizeFramesToTargetFPS(fps);
				current_second = new SecondGrouping ();
				current_second.timestamp = frame.timestamp;
				seconds_list.Add(current_second);
			}

			current_second.addFrame(frame);

		}

		seconds_list.Last ().normalizeFramesToTargetFPS (fps);


	}



	public void truncateToSafeTimestamps(int starting, int ending){

			List<SecondGrouping> remove_list = new List<SecondGrouping> ();
		
			foreach (SecondGrouping second in seconds_list) {

				if(second.timestamp < starting || second.timestamp > ending){
					remove_list.Add(second);
				}

			}

			if (remove_list.Count > 0) {
				foreach(SecondGrouping second in remove_list)
					seconds_list.Remove(second);
			}

	}

}
