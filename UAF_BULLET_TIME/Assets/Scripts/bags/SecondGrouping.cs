using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.Linq;


[System.Serializable]
public class SecondGrouping  {
	public int timestamp;

	public int target_fps;
	public List<CamFrame> frame_list;
	public CamFrame[] normalized_frames;

	public void addFrame(CamFrame frame){
		if(frame_list == null)
			frame_list = new List<CamFrame>();

		frame_list.Add(frame);

	}

	public void normalizeFramesToTargetFPS(int fps){
		target_fps = fps;
		frame_list.OrderBy (c => c.frame_index);

		//int actual_frame_count = frame_list.Count;
		CamFrame[] frame_set = new CamFrame[fps];

		CamFrame current_filler_frame = frame_list.First();
		int i = 0;
		for (; i<fps; i++) {

			if(i>=current_filler_frame.frame_index){
				int potential_next = frame_list.IndexOf(current_filler_frame)+1;
				if( potential_next < frame_list.Count)
					current_filler_frame = frame_list[ potential_next];
			}

			frame_set[i] = current_filler_frame;

		}

		normalized_frames = frame_set;

	}

}
