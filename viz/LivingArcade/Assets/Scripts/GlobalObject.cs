using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Reflection;
using System;

public class GlobalObject : MonoBehaviour {
    //Database Variables
    public string OffScreenEffect;
    List<ObjectRecipe> recipes;
    List<ObjectLogic> gameObjs;

    // Use this for initialization
    void Start ()
    {
        //Load from db into dbInfo
        ObjController dbInfo = new ObjController();
        //newLevel();
    }

	// Update is called once per frame
	void Update ()
    {

	}

    void newLevel()
    {
        //Clear map and destroy object instances
        //Init player
        foreach(ObjectRecipe recipe in recipes)
        {
            //Use ObjectRecipe instances to create actual LAObject instances
            //ObjectLogic gameObj = new ObjectLogic(recipe.Shape, recipe.Color, recipe.Opacity, recipe.triggers);
        }
    }
}

[System.Serializable]
public class ObjectRecipe
{
    public string Shape;
    public string Color;
    public string Opacity;
    public string NumActionButtons;
    public string NumObjects;
    public string PlayerSpawns;
    public string Player;
    public string[] minSpawns = new string[12];
    public string[] maxSpawns = new string[12];
    public trigger[] triggers;

	public static ObjectRecipe CreateFromJSON(string jsonString)
	{
		return JsonUtility.FromJson<ObjectRecipe>(jsonString);
	}

    /*Shape: Circle, Triangle, Square, Pentagon, Hexagon, Octagon, more?
    Color: rgb(0, 0, 0) - rgb(255, 255, 255)
    Opacity: 0 - 100
    Spawns: (a 12 length array of ranges, one range for each of 12 regions. The ranges indicated how many of these can spawn in the region at the start of the level, and this should be close to zero.)
    Triggers: (with below attributes)*/
}

public class trigger
{
    public string Pressed;
    public string Held;
    public string Released;
    public string CollideWithAny;
    public string CollideWithObj;
}

