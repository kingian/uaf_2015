using UnityEngine;
using System.Collections;

public class WiggleObject : MonoBehaviour {

	private float circle_diameter = 0.3f;
	private float orbits_per_second = 0.2f;
	private float start_x;
	private float start_z;
	private float current_angle = 0;
	private float rad_factor = Mathf.PI / 180.0f;

	// Use this for initialization
	void Start () {
		this.start_x = transform.position.x;
		this.start_z = transform.position.z;
	}
	
	// Update is called once per frame
	void Update () {
		this.current_angle += (this.circle_diameter * Time.deltaTime);
		if(this.current_angle >= 360){
			this.current_angle = 0;
		}
		//transform.Translate (Mathf.Sin (this.current_angle * this.rad_factor), 1, Mathf.Cos (this.current_angle * this.rad_factor));
	}
}
