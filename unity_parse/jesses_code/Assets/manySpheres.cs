using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class manySpheres : MonoBehaviour {

	public float scaler = 10000;

	public LinkedList<Vector3> jessesList;

	// Use this for initialization
	void Start () 
	{
		jessesList = new LinkedList<Vector3> ();
		for (int j=0; j <= 10; j++) 
		{
			makeAK();
			
			//			while (j<=100)yield return new WaitForSeconds (5.0f);
		}
	}
	
	// Update is called once per frame
	void Update () 
	{

	
	}

	void makeAK()
	{
		for (int i=0; i <=1000; i++) {
						GameObject sphere = GameObject.CreatePrimitive (PrimitiveType.Sphere);
						sphere.transform.parent = this.transform;
						sphere.transform.position = randomVector();
						sphere.renderer.material.shader = Shader.Find ("Transparent/Diffuse");
						sphere.renderer.material.color = new Color (0, 1.0f, .5f, .25f);
				}
	}

	Vector3 randomVector()
	{
		return new Vector3 ((Random.value - 0.5f) * scaler, 1.0f, (Random.value - 0.5f) * scaler);
	}
}
