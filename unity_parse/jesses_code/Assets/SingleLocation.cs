using Parse;
using System;//<---needed for DateTime, which is code the deals with the complexities of "dates" and "time"

//from parse's example : https://parse.com/docs/unity_guide#subclasses
[ParseClassName("LocationData")]//<---- this is the table refence in the parse.com website
public class SingleLocation : ParseObject {

	//going to center everything on my house
	private float LatOffset = 40.73962f;
	private float LonOffset = -111.872f;

	//example of mapping Parse columns ToString ICustomFormatter "proprties"
	[ParseFieldName("lat")]
	public float Lat{
		get { return (GetProperty<float> ("Lat") - this.LatOffset) * -24000; }
		//no setters - setters are for saving. we wont be
		//set {//save stuff in here}
	}

	[ParseFieldName("lon")]
	public float Lon{
		get { return (GetProperty<float>("Lon") - this.LonOffset) * 24000 ; }
	}

	[ParseFieldName("time")]
	public DateTime Time{
		get { return GetProperty<DateTime>("Time"); }
	}

	//example making custom property that does anything you like
	public string DebugMessage{
		get { return this.Lat + ", " + this.Lon + " -- " + this.Time; }
	}

	public string RawCoordinates{
		get {return "lat:" + GetProperty<float>("Lat") + ", Lon:" + GetProperty<float>("Lon");}
	}

}
