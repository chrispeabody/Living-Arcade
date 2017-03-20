using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ObjectLogic : MonoBehaviour {
    public string Shape;
    public string Color;
    public string Opacity;
    public trigger[] trig;


	// Use this for initialization
	void Start ()
    {
		
	}
	
	// Update is called once per frame
	void Update ()
    {
		//Check for triggers
        /*for(through this object's triggers)
        {
            //Check triggers
            if (trigger is button held && unity says button is held)
            {
                //call director(nameofreaction) in order to check which reaction function to call and call it
            }
        }*/
        
	}

    //Reactions
    void DestroySelf()
    {

    }

    void DestroyObj()
    {

    }

    void CreateObj()
    {

    }

    void CreateObjRad()
    {

    }

    void Become()
    {

    }

    void ModScore()
    {

    }

    void ModXSpeed()
    {

    }

    void ModYSpeed()
    {

    }

    void SetXSpeed()
    {

    }

    void SetYSpeed()
    {

    }

    void ModColor()
    {

    }

    void SetColor()
    {

    }

    void ModOpacity()
    {

    }

    void SetOpacity()
    {

    }

    void ChangeShape()
    {

    }

    void ChangeOffscreenEffect()
    {

    }
}