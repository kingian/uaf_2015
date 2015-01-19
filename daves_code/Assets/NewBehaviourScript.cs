using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.Threading.Tasks;
using Parse;

public class NewBehaviourScript : MonoBehaviour
{
	private class LocationDataContainer
	{
		public float lat;
		public float lon;
		public float alt;
		public string act;

		public LocationDataContainer()
		{
			this.lat = 0;
			this.lon = 0;
			this.alt = 0;
			this.act = "";
		}

		public LocationDataContainer(float lat, float lon, float alt, string act)
		{
			this.act = act;
			this.alt = alt;
			this.lat = lat;
			this.lon = lon;
		}

		public static LocationDataContainer operator -(LocationDataContainer a, LocationDataContainer b)
		{
			return new LocationDataContainer(a.lat-b.lat, a.lon-b.lon, a.alt-b.alt, a.act);
		}

		public static LocationDataContainer operator *(LocationDataContainer a, float b)
		{
			return new LocationDataContainer(a.lat*b, a.lon*b, a.alt*b, a.act);
		}
	}

	Queue locationDataQueue = new Queue();
	LocationDataContainer zeroPoint = null;

	/**
	 * Connects to the parse server and populates the locationDataQueue with the data points retrieved.
	 * This may be able to become blocking if we use the await keyword.
	 */
	private void populateLocationQueue(int start, int repeatCount)
	{
		int maxRepeat = 3;
		int limit = 1000;

		if (repeatCount >= maxRepeat)
		{
			return;
		}

		// Location data query without filtering on user.
//		ParseQuery<ParseObject> locationQuery = ParseObject.GetQuery ("LocationData")
//			.WhereEqualTo ("activity", "stationary")
//				.Limit (limit)
//				.Skip (start)
//				.OrderBy ("updatedAt");

		// Swicth between Berk and Jesse
//		ParseQuery<ParseUser> userQuery = ParseUser.Query.WhereStartsWith("nickname", "jesse2");
		ParseQuery<ParseUser> userQuery = ParseUser.Query.WhereStartsWith("nickname", "Bercules");

		// Output the user info to the screen.
//		userQuery.FindAsync ().ContinueWith (uResults =>
//		{
//			foreach(ParseObject u in uResults.Result)
//			{
//				Debug.Log ("Users: " + u.Get<string>("nickname"));
//			}
//		});


		ParseQuery<ParseObject> locationQuery = ParseObject.GetQuery ("LocationData")
			.WhereMatchesKeyInQuery("user", "objectId", userQuery)
			.Limit (limit)
			.Skip (start)
			.OrderBy ("updatedAt");

		locationQuery.FindAsync().ContinueWith(t => 
		{
			Debug.Log("Results retrieved from Parse.");
			int count = 0;
			foreach(ParseObject p in t.Result)
			{
				count++;

				LocationDataContainer c = new LocationDataContainer();
				c.lat = p.Get<float>("lat");
				c.lon = p.Get<float>("lon");
				c.alt = p.Get<float>("altitude");
				c.act = p.Get<string>("activity");

				if(zeroPoint == null)
				{
					zeroPoint = c;
				}
				locationDataQueue.Enqueue(c);
			}

			// Did we hit the loop limit?
			if(!(count < limit))
			{
				repeatCount += repeatCount < 0 ? 0 : 1;
				populateLocationQueue(start+limit, repeatCount);
			}
		});
	}

	/**
	 * Drains the locationDataQueue and builds a cube at the location for each element in the queue.
	 */ 
	private void drainLocationQueue()
	{
		while(locationDataQueue.Count != 0)
		{
			LocationDataContainer c = (LocationDataContainer) locationDataQueue.Dequeue();
			
			float pathScale = 100;
			
			GameObject sphere = GameObject.CreatePrimitive(PrimitiveType.Cube);
			LocationDataContainer diff = (c - zeroPoint) * pathScale;
			sphere.transform.position = new Vector3(diff.lat, diff.lon, diff.alt);
			
			float objectScale = 1.0f;
			sphere.transform.localScale = new Vector3(objectScale, objectScale, objectScale);
			
			Color col = new Color(1.0f, 1.0f, 1.0f);
			
			if(c.act.CompareTo("stationary") == 0)
			{
				col = new Color(1.0f, 0.0f, 0.0f);
			}
			
			sphere.renderer.material.color = col;
			
		}
	}


	// Use this for initialization
	void Start ()
	{
		populateLocationQueue (0, 0);
	}
	
	// Update is called once per frame
	void Update ()
	{
		drainLocationQueue();
	}
}
