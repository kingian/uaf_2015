using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class manySpheres : MonoBehaviour {

	private float bounds = 100;
	private int total_objects = 10000;

	private LinkedList<GameObject> jessesList;

	// Use this for initialization
	void Start () 
	{
		jessesList = new LinkedList<GameObject> ();
		makeAK();
	}
	
	// Update is called once per frame
	void Update () 
	{
		foreach( var game_object in this.jessesList){
			game_object.transform.Translate(.1f,0,.1f);
		}
	}

	void makeAK()
	{	
		var numTriangles = 0;
		for (int i=0; i <= this.total_objects; i++) {
			GameObject sphere = GameObject.CreatePrimitive (PrimitiveType.Sphere);
			sphere.transform.parent = this.transform;
			sphere.transform.position = randomVector();
			sphere.renderer.material.shader = Shader.Find ("Transparent/Diffuse");
			sphere.renderer.material.color = new Color (1.0f,0, 0, 1.0f);
			this.jessesList.AddLast(sphere);

			numTriangles = sphere.GetComponent<MeshFilter>().mesh.triangles.Length/3;
		}
		Debug.Log (this.jessesList.Count);
		Debug.Log(numTriangles);
		Debug.Log(numTriangles*this.total_objects);
	}

	Vector3 randomVector()
	{
		return new Vector3 (Random.Range(-this.bounds, this.bounds), 1.0f, Random.Range(-this.bounds, this.bounds));
	}
}
