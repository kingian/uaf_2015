using UnityEngine;
using System.Collections;
//needed for IEnumerable
using System.Collections.Generic;

using Parse;


public class ParseExample : MonoBehaviour {

	// Use this for initialization
	void Start () {
		
		//we created this ourselves in SingleLocation.CS
		//it subclasses parseobject so we can make our code cleaner
		//in this case we map our "SingleLocation" object to the parse "LocationData" table
		ParseObject.RegisterSubclass<SingleLocation>();


		//this coroutine asychronously gets item count, then asynchronously fethces pages (groups of 1k locations)
		//and makes spheres - it currtently errors out above 10k for an unkown reason.
		StartCoroutine ("getDataInPages");//this gets pages, then launches other sub routines


		//the stuff below are simple examples of the basic stuff the coroutine above does
		
		//create ground plane
//		GameObject plane = GameObject.CreatePrimitive(PrimitiveType.Plane);
//		plane.transform.localScale = new Vector3(1000.0F, 0.0001F, 1000.0F);
//		plane.transform.position = new Vector3(-500.0F, 0.0F, -500.0F);


		//saving data example
//		ParseObject testObject = new ParseObject("TestObject222");
//		testObject["foo"] = "bar";
//		testObject.SaveAsync();
//		Debug.Log ("MADE OBJECT");

		//parse maxes out at 1k
//		int items_per_page = 1000;
//		int total_items = 0;//dunno how many yet

		//counting objetcs example -- supposedly inaccurate for alrge datasets like our
//		var count_query = new ParseQuery<SingleLocation>().OrderBy("time");
//		count_query.CountAsync ().ContinueWith (task => {
//			int count = task.Result;
//			Debug.Log(count);
//			total_items = count;
//
//
//		});




		//simplest fetching data example
//		var query = new ParseQuery<SingleLocation>().OrderBy("time").WhereEqualTo("activity", "walking").Limit(10);
//		query.FindAsync().ContinueWith(task =>
//		{
//
//			if(task.IsCompleted){
//
//				Debug.Log("recieved results");
//				IEnumerable<SingleLocation> results = task.Result;
//				//we have objects, go through them
//				foreach (var single_location in results){
//					Debug.Log( single_location.DebugMessage );//<-- "DebugMessage" is a custom thing we made in SingleLocation.CS
//				}
//
//			}else if(task.IsFaulted){
//				Debug.Log("PARSE QUERY ERROR");
//			}else if(task.IsCanceled){
//				Debug.Log("PARSE QUERY CANCELED?");
//			}
//
//
//		});


	}
	
	// Update is called once per frame
	void Update () {
	
	}

	public IEnumerator getDataInPages(){

		//parse maxes out at 1k
		int items_per_page = 1000;
		int total_items = 0;//dunno how many yet

		//counting objetcs example -- supposedly inaccurate for alrge datasets like our
		var count_query = new ParseQuery<SingleLocation>().OrderBy("time");
		var task = count_query.CountAsync ();
		while (!task.IsCompleted)yield return new WaitForSeconds (.1f);
		//should have the final count now
		total_items = task.Result;

		int page_count = total_items / items_per_page;
		for (int i = 0; i < page_count; i++) {
			PagingInfo page = new PagingInfo ();
			page.PageIndex = i;
			page.PageSize = items_per_page;
			yield return StartCoroutine("GetDataAndMakeSpheres", page);
		}

		Debug.Log ("finished fetching all items");
	}

	public IEnumerator GetDataAndMakeSpheres(PagingInfo page){

		//using paging to make fetch delay
		//yield return new WaitForSeconds (2.0f * page.PageIndex);

		Debug.Log("FETCHING DATA:" + page.SkipAmount);
		var query = new ParseQuery<SingleLocation>().OrderBy("time").Limit(page.PageSize).Skip(page.SkipAmount);
		var task = query.FindAsync();
		while(!task.IsCompleted) yield return new WaitForSeconds(500.0f/page.PageSize);
		//if we get here we have data and are in main thread again - so we can make objects

		if (task.IsFaulted) {
			Debug.Log("FAULTED TASK : " + task.Exception);
		}else if(task.IsCanceled){
			Debug.Log("CANCELED TASK");
		}else {

			Debug.Log("MAKING SPHERES");
			IEnumerable<SingleLocation> results = task.Result;
			int count = 0;
			float lat_offset = 0;
			float lon_offset = 0;
			foreach (var single_location in results) {
				count++;
				//Debug.Log(single_location.RawCoordinates);
				//Debug.Log("object:"+(count +page.SkipAmount));
				//Debug.Log(single_location.DebugMessage);
				GameObject sphere = GameObject.CreatePrimitive(PrimitiveType.Sphere);
				sphere.transform.parent = this.transform;
				sphere.transform.position = new Vector3(single_location.Lat,1.0F,single_location.Lon);
				sphere.renderer.material.shader = Shader.Find( "Transparent/Diffuse" );
				sphere.renderer.material.color = new Color(0,1.0f,1.0f,.25f);

				//yield return new WaitForSeconds(0.05f);//helpful if doing tweens or animations on eachobject
			}

		}




	}

}
